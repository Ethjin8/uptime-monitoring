import time   # library for built-in clock tools (e.g., stopwatch)
import requests   # library for making HTTP requests

from db.queries import list_targets, save_result    # functions to query database directly


def check_target(url):
  start = time.monotonic()    # start the stopwatch to measure elapsed time
  try:
    resp = requests.get(url, timeout=5)   # make the request
    ms = int((time.monotonic() - start) * 1000)   # find out how much time elapsed
    return {"status_code": resp.status_code, "latency_ms": ms, "error": None}    # return status, ms elapsed, and error (None) as dict

  # requests has predefined error types that we can check for
  except requests.exceptions.Timeout:
    return {"status_code": None, "latency_ms": None, "error": "TIMEOUT"}   # return the above fields, but w/ appropriate error values
  except requests.exceptions.SSLError:    # security ID is invalid, cannot connect due to safety concerns
    return {"status_code": None, "latency_ms": None, "error": "TLS_ERROR"}
  except requests.exceptions.ConnectionError as e:    # ConnectionError can be due to DNS error, or refused connection
    error = str(e)    # convert to string for easy search (print error to see full shape)

    if "Connection refused" in error:    # domain name exists and has IP, but nothing at the port (443 for HTTPS)
      return {"status_code": None, "latency_ms": None, "error": "CONN_REFUSED"}

    elif "NameResolutionError" in error:    # domain name does not exist on Internet
      return {"status_code": None, "latency_ms": None, "error": "DNS"} 

    else:   # handle leftover connection errors that weren't considered
      return {"status_code": None, "latency_ms": None, "error": "UNKNOWN_ERROR"}
    
  except Exception as e:    # handle leftover errors
    return {"status_code": None, "latency_ms": None, "error": "UNKNOWN_ERROR"}


while True:
  for row in list_targets():
    probe_result = check_target(row["url"])
    save_result(row["id"], probe_result)

  time.sleep(30)
  