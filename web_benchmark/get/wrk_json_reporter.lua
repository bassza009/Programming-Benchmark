done = function(summary, latency, requests)
  local requests_total = summary.requests or 0
  local errors_status = summary.errors and summary.errors.status or 0
  local errors_read = summary.errors and summary.errors.read or 0
  local errors_write = summary.errors and summary.errors.write or 0
  local success = requests_total - errors_status - errors_read - errors_write
  if success < 0 then success = 0 end

  local errors_total = 0
  if summary.errors then
    for _, v in pairs(summary.errors) do
      if type(v) == "number" then
        errors_total = errors_total + v
      end
    end
  end

  local min_ms = latency.min / 1000.0
  local max_ms = latency.max / 1000.0
  local mean_ms = latency.mean / 1000.0
  local stdev_ms = latency.stdev / 1000.0
  local p50_ms = latency:percentile(50) / 1000.0
  local p95_ms = latency:percentile(95) / 1000.0
  local p99_ms = latency:percentile(99) / 1000.0
  local requests_per_sec = 0
  if summary.duration and summary.duration > 0 then
    requests_per_sec = requests_total / (summary.duration / 1000000.0)
  end

  local function fmt_num(value)
    if value ~= value then
      return "null"
    end
    return string.gsub(string.format("%.6f", value), "(%..-)0+$", "%1")
  end

  local json = "{"
    .. string.format("\"requests\":%d,", requests_total)
    .. string.format("\"success\":%d,", success)
    .. string.format("\"errors\":%d,", errors_total)
    .. string.format("\"min_ms\":%s,", fmt_num(min_ms))
    .. string.format("\"max_ms\":%s,", fmt_num(max_ms))
    .. string.format("\"mean_ms\":%s,", fmt_num(mean_ms))
    .. string.format("\"stdev_ms\":%s,", fmt_num(stdev_ms))
    .. string.format("\"p50_ms\":%s,", fmt_num(p50_ms))
    .. string.format("\"p95_ms\":%s,", fmt_num(p95_ms))
    .. string.format("\"p99_ms\":%s,", fmt_num(p99_ms))
    .. string.format("\"requests_per_sec\":%s", fmt_num(requests_per_sec))
    .. "}"

  io.write(json)
end
