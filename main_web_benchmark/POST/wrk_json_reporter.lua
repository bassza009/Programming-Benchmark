wrk.method = "POST"
wrk.headers["Content-Type"] = "application/json"
wrk.body = "{}"

done = function(summary, latency, requests)
   local requests_per_sec = summary.duration > 0 and (summary.requests / (summary.duration / 1000000)) or 0
   local latency_mean_ms = latency.mean / 1000
   local latency_max_ms = latency.max / 1000
   local errors = summary.errors.connect + summary.errors.read + summary.errors.write + summary.errors.status + summary.errors.timeout

   io.write(string.format([[{
  "requests_per_sec": %.2f,
  "latency_mean_ms": %.2f,
  "latency_max_ms": %.2f,
  "errors": %d
}]], requests_per_sec, latency_mean_ms, latency_max_ms, errors))
end
