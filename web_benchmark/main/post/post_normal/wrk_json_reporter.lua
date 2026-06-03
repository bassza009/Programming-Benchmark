request = function()
   wrk.method = "POST"
   wrk.headers["Content-Type"] = "application/json"
   request = function()
    local random_id = math.random(10000000, 999999999)
    local body_str = '{"name": "Bench User", "email": "user_' .. random_id .. '@example.com"}'
    
    return wrk.format(wrk.method, wrk.path, wrk.headers, body_str)
end

done = function(summary, latency, requests)
   io.write("{\n")
   io.write(string.format('  "requests": %d,\n', summary.requests))
   io.write(string.format('  "requests_per_sec": %f,\n', (summary.requests/summary.duration)*1000000))
   io.write(string.format('  "latency_mean_ms": %f,\n', latency.mean / 1000))
   io.write(string.format('  "latency_max_ms": %f,\n', latency.max / 1000))
   io.write(string.format('  "errors": %d\n', summary.errors.connect + summary.errors.read + summary.errors.write + summary.errors.status))
   io.write("}\n")
end
