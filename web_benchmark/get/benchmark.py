#!/usr/bin/env python3
"""
GET Request Benchmarking Script
Benchmarks different web servers using concurrent requests
"""

import concurrent.futures
import requests
import time
import json
import sys
import os
from datetime import datetime
from urllib.parse import urljoin

class GetBenchmark:
    def __init__(self, servers, duration=30, threads=4, connection_pool=100):
        """
        Initialize benchmark configuration
        
        Args:
            servers: List of tuples (name, url)
            duration: Benchmark duration in seconds
            threads: Number of concurrent threads
            connection_pool: Max connections in pool
        """
        self.servers = servers
        self.duration = duration
        self.threads = threads
        self.connection_pool = connection_pool
        self.results_dir = "results"
        os.makedirs(self.results_dir, exist_ok=True)
        
    def check_server_health(self, url, timeout=5):
        """Check if server is responding"""
        try:
            response = requests.get(
                urljoin(url, '/health'),
                timeout=timeout
            )
            return response.status_code == 200
        except Exception as e:
            print(f"  ✗ Health check failed: {e}")
            return False
    
    def benchmark_endpoint(self, url, endpoint, max_requests=None):
        """
        Benchmark a single endpoint
        
        Returns:
            dict with benchmark results
        """
        endpoint_url = urljoin(url, endpoint)
        
        times = []
        errors = 0
        success = 0
        
        def make_request():
            try:
                start = time.time()
                response = requests.get(endpoint_url, timeout=10)
                elapsed = (time.time() - start) * 1000  # Convert to ms
                
                if response.status_code == 200:
                    return elapsed, None
                else:
                    return None, f"HTTP {response.status_code}"
            except Exception as e:
                return None, str(e)
        
        start_time = time.time()
        request_count = 0
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = []
            
            while time.time() - start_time < self.duration:
                # Submit new requests up to max concurrent
                while len(futures) < self.threads * 2:
                    future = executor.submit(make_request)
                    futures.append(future)
                
                # Check completed futures
                done, futures = concurrent.futures.wait(
                    futures,
                    timeout=0.1,
                    return_when=concurrent.futures.FIRST_COMPLETED
                )
                
                for future in done:
                    elapsed, error = future.result()
                    request_count += 1
                    
                    if error:
                        errors += 1
                    else:
                        times.append(elapsed)
                        success += 1
            
            # Wait for remaining requests
            for future in concurrent.futures.as_completed(futures, timeout=5):
                elapsed, error = future.result()
                request_count += 1
                
                if error:
                    errors += 1
                else:
                    times.append(elapsed)
                    success += 1
        
        # Calculate statistics
        if times:
            times.sort()
            min_time = min(times)
            max_time = max(times)
            mean_time = sum(times) / len(times)
            median_time = times[len(times) // 2]
            p95_time = times[int(len(times) * 0.95)]
            p99_time = times[int(len(times) * 0.99)]
            
            # Calculate stddev
            variance = sum((x - mean_time) ** 2 for x in times) / len(times)
            stddev = variance ** 0.5
        else:
            min_time = max_time = mean_time = median_time = p95_time = p99_time = stddev = 0
        
        return {
            'endpoint': endpoint,
            'requests': request_count,
            'success': success,
            'errors': errors,
            'min_ms': round(min_time, 2),
            'max_ms': round(max_time, 2),
            'mean_ms': round(mean_time, 2),
            'median_ms': round(median_time, 2),
            'stddev_ms': round(stddev, 2),
            'p95_ms': round(p95_time, 2),
            'p99_ms': round(p99_time, 2),
            'requests_per_sec': round(success / self.duration, 2),
            'error_rate': round((errors / request_count * 100) if request_count > 0 else 0, 2)
        }
    
    def run(self):
        """Run benchmarks on all servers"""
        timestamp = int(time.time())
        endpoints = ['/', '/health', '/api/data']
        
        print("=" * 60)
        print("GET Request Benchmarking Suite")
        print("=" * 60)
        print(f"Timestamp: {timestamp}")
        print(f"Duration per endpoint: {self.duration}s")
        print(f"Threads: {self.threads}")
        print(f"Endpoints: {', '.join(endpoints)}")
        print("")
        
        all_results = {}
        
        for server_name, server_url in self.servers:
            print(f"\n{'='*60}")
            print(f"Testing: {server_name}")
            print(f"URL: {server_url}")
            print(f"{'='*60}")
            
            # Check server health
            print("Checking server health...", end=" ", flush=True)
            if not self.check_server_health(server_url):
                print("✗ Server not responding - Skipping")
                continue
            print("✓ Server is healthy")
            
            server_results = {
                'server': server_name,
                'url': server_url,
                'timestamp': timestamp,
                'endpoints': {}
            }
            
            # Benchmark each endpoint
            for endpoint in endpoints:
                print(f"\n  Benchmarking {endpoint}...", end=" ", flush=True)
                result = self.benchmark_endpoint(server_url, endpoint)
                server_results['endpoints'][endpoint] = result
                print(f"✓ Complete")
                
                # Print summary
                print(f"    Requests: {result['requests']} "
                      f"(Success: {result['success']}, Errors: {result['errors']})")
                print(f"    Requests/sec: {result['requests_per_sec']}")
                print(f"    Mean: {result['mean_ms']}ms | "
                      f"Median: {result['median_ms']}ms | "
                      f"Std Dev: {result['stddev_ms']}ms")
                print(f"    Min: {result['min_ms']}ms | "
                      f"Max: {result['max_ms']}ms | "
                      f"P95: {result['p95_ms']}ms | "
                      f"P99: {result['p99_ms']}ms")
            
            all_results[server_name] = server_results
        
        # Save results
        results_file = os.path.join(
            self.results_dir,
            f'get_benchmark_{timestamp}.json'
        )
        with open(results_file, 'w') as f:
            json.dump(all_results, f, indent=2)
        
        print(f"\n{'='*60}")
        print("Benchmark Complete!")
        print(f"Results saved to: {results_file}")
        print(f"{'='*60}\n")
        
        return all_results


if __name__ == '__main__':
    # Default servers
    servers = [
        ('Python', 'http://localhost:8001'),
        ('Node.js', 'http://localhost:8002'),
        ('PHP', 'http://localhost:8003'),
        ('Go', 'http://localhost:8004'),
        ('Java', 'http://localhost:8005'),
    ]
    
    # Parse command line arguments
    duration = 30
    threads = 4
    
    if len(sys.argv) > 1:
        duration = int(sys.argv[1])
    if len(sys.argv) > 2:
        threads = int(sys.argv[2])
    
    benchmark = GetBenchmark(servers, duration=duration, threads=threads)
    benchmark.run()
