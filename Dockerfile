FROM python:3.9.20-alpine3.20
WORKDIR /app
COPY diagnostics-server.py /app/diagnostics-server.py
CMD chmod +x /app/diagnostics-server.py
ENTRYPOINT ["/usr/local/bin/python", "/app/diagnostics-server.py"]