done = function(summary, latency, requests)
   io.write("{\n")
   io.write(string.format('  "requests": %d,\n', summary.requests))
   io.write(string.format('  "requests_per_sec": %f,\n', (summary.requests/summary.duration)*1000000))
   io.write(string.format('  "latency_mean_ms": %f,\n', latency.mean / 1000))
   io.write(string.format('  "latency_max_ms": %f,\n', latency.max / 1000))
   io.write(string.format('  "errors": %d\n', summary.errors.connect + summary.errors.read + summary.errors.write + summary.errors.status))
   io.write("}\n")
end
