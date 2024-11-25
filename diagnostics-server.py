#!/usr/bin/python3

from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from json import dumps, loads
from os import environ
from time import sleep
from urllib.parse import urlparse

import logging

http_diagnostics_port = int(environ.get("HTTPDIAG_PORT", "8080"))
http_diagnostics_command_header = str(environ.get("HTTPDIAG_COMMAND_HEADER", "Diag-Command"))
http_diagnostics_mask_request_headers = str(environ.get("HTTPDIAG_MASK_REQUEST_HEADERS", "").lower().split(","))

class DiagnosticsHTTPServer(BaseHTTPRequestHandler):

  def log_message(self, format: str, *args) -> None:
    message = format % args
    logging.info(f"{self.log_date_time_string()} - {self.address_string()} - {message.translate(self._control_char_table)}")

  def parse_command(self, command):
    parsed_cmd = None
    try:
      parsed_cmd = loads(command) if (
        len(command) > 0
      ) else {}
    except Exception as e:
      parsed_cmd = {"message": f"error in parsing json in Diag-Command: {str(e.args[0])}"}
    return parsed_cmd
  
  def parse_query(self, query):
    results = {}
    for parameter in query.split("&"):
      parsed_parameter = parameter.split("=")
      if len(parsed_parameter) > 1:
        results.update(
          {
            parsed_parameter[0]: parsed_parameter[1]
          }
        )
    return results
  
  def generate_response(self,request_type):
    diag_command = self.parse_command(self.headers.get(http_diagnostics_command_header, ""))
    self.send_response(int(diag_command.get("response-code", 200)))
    self.send_header("Content-Type", "application/json")
    self.end_headers()
    try:
      sleep_time = int(diag_command.get("sleep", 0))
      if sleep_time > 0:
        sleep(sleep_time)
    except:
      pass

    parsed_path = urlparse(self.path)
    request_headers = {}
    for name in self.headers:
      request_headers.update(
        {
          name: self.headers.get(name) if (
            name.lower() not in http_diagnostics_mask_request_headers
          ) else "http-diagnostics masked header."
        }
      )
    body = {
      "request-type": request_type,
      "url-path": parsed_path.path,
      "request-headers": request_headers,
    }

    parsed_query = self.parse_query(parsed_path.query)
    if len(parsed_query) > 0:
      body.update(
        {
          "query-params": parsed_query,
        }
      )

    if diag_command.get("message", None) is not None:
      body.update(
        {
          "message": diag_command.get("message", None)
        }
      )

    if diag_command.get("message-type", "pretty-json") == "json":
      self.wfile.write(
        dumps(body).encode()
      )
    else: 
      self.wfile.write(
        dumps(body, indent=2).encode()
      )

  def do_GET(self):
    self.generate_response("GET")
  
  def do_HEAD(self):
    self.generate_response("HEAD")

  def do_POST(self):
    self.generate_response("POST")

  def do_PUT(self):
    self.generate_response("PUT")

  def do_DELETE(self):
    self.generate_response("DELETE")

  def do_OPTIONS(self):
    self.generate_response("OPTIONS")

  def do_PATCH(self):
    self.generate_response("PATCH")

  def do_CONNECT(self):
    self.generate_response("CONNECT")

  def do_TRACE(self):
    self.generate_response("TRACE")

if __name__ == "__main__":
  logging.basicConfig(
    format='%(levelname)s: %(message)s',
    encoding='utf-8',
    level=logging.INFO
  )
  logging.info(f"Starting diagnostics server on port {http_diagnostics_port}")
  server_address = ("0.0.0.0", http_diagnostics_port)
  httpd = ThreadingHTTPServer(
      server_address,
      DiagnosticsHTTPServer
  )
  try:
    httpd.serve_forever()
  except KeyboardInterrupt:
    logging.info("exitting")
