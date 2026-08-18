wrk.method = "POST"
wrk.headers["Content-Type"] = "application/json"
wrk.body = "{}"

done = function(summary, latency, requests)
   local duration_sec = (summary.duration or 0) / 1000000
   local requests_per_sec = duration_sec > 0 and ((summary.requests or 0) / duration_sec) or 0
   local latency_mean_ms = (latency and latency.mean and latency.mean == latency.mean and latency.mean > 0) and (latency.mean / 1000) or 0
   local latency_max_ms = (latency and latency.max and latency.max == latency.max and latency.max > 0) and (latency.max / 1000) or 0
   local errors = 0
   if summary and summary.errors then
      errors = (summary.errors.connect or 0) + (summary.errors.read or 0) + (summary.errors.write or 0) + (summary.errors.status or 0) + (summary.errors.timeout or 0)
   end

   io.write(string.format([[{
  "requests_per_sec": %.2f,
  "latency_mean_ms": %.2f,
  "latency_max_ms": %.2f,
  "errors": %d
}]], requests_per_sec, latency_mean_ms, latency_max_ms, errors))
end
