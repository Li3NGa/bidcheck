from __future__ import annotations
import json
from http.server import BaseHTTPRequestHandler
from .http_api import APIError, create_project, audit_project

class JSONAPIHandler(BaseHTTPRequestHandler):
    service = None
    def _send(self,status,payload):
        body=json.dumps(payload,ensure_ascii=False,default=str).encode(); self.send_response(status); self.send_header('Content-Type','application/json; charset=utf-8'); self.send_header('Content-Length',str(len(body))); self.end_headers(); self.wfile.write(body)
    def _body(self):
        try: return json.loads(self.rfile.read(int(self.headers.get('Content-Length','0')) or 0))
        except (ValueError, json.JSONDecodeError): raise APIError(400,'invalid_json','request body must be valid JSON')
    def do_POST(self):
        try:
            if self.path=='/api/v1/projects': return self._send(201,create_project(self.service,self._body()))
            if self.path.startswith('/api/v1/projects/') and self.path.endswith('/audit'): return self._send(200,audit_project(self.service,self.path.split('/')[4]))
            return self._send(404,{"error":"not_found"})
        except APIError as e: return self._send(e.status,{"error":e.code,"message":e.message})
