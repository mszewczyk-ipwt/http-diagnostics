# http-diagnostics
A simple HTTP server that verboses HTTP request and returns a body with the HTTP session variables like request type, path, etc. The server listens on all interfaces and it is suppose to be used in container environments. The server should support all MDN declared request types.

## env parameters
* `HTTPDIAG_PORT` - port to listen on. Default `8080`.
* `HTTPDIAG_COMMAND_HEADER` - name of the request header to be used to read commands from, see command reference below. Default `cmd`.
* `HTTPDIAG_MASK_REQUEST_HEADERS` - comma separated list of headers to be masked. Default `None`.

## command reference
Command is used to simulate several kinds of server behaviour like return body not imidiatelly but after a time or return particular HTTP code. To have a use of that the request header should be a type of json like:
```
curl localhost:8080 -H 'Diag-Command: {"response-code":200, "sleep": 5}'
```
Reference:
* `response-code` - numerical response code to return, currently there are no limits. Default `200`.
* `sleep` - return response after this amount of seconds. Default `0`.
* `message' - leave a message here. Default `None`.
* `message-type` - return a body in a declared type. Currently supporting `json` and `pretty-json`. Default `pretty-json`.
* `mask-request-headers` - mask 

