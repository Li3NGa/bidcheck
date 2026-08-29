from __future__ import annotations
import json
from http.server import BaseHTTPRequestHandler,HTTPServer
from .api import BidCheckService
from .http_api import APIError,create_project,get_project,audit_project
from .service_factory import create_service

service=create_service()

class Handler(BaseHTTPRequestHandler):
    def _send(self,status,payload):
        body=json.dumps(payload,ensure_ascii=False,default=str).encode(); self.send_response(status); self.send_header('Content-Type','application/json; charset=utf-8'); self.send_header('Content-Length',str(len(body))); self.send_header('Cache-Control','no-store'); self.end_headers(); self.wfile.write(body)
    def _body(self):
        try:return json.loads(self.rfile.read(int(self.headers.get('Content-Length','0')) or 0))
        except (ValueError,json.JSONDecodeError):raise APIError(400,'invalid_json','request body must be valid JSON')
    def do_GET(self):
        try:
            if self.path=='/health':return self._send(200,{"status":"ok","service":"bidcheck"})
            if self.path.startswith('/api/v1/projects/'):return self._send(200,get_project(service,self.path.rsplit('/',1)[-1]))
            return self._send(404,{"error":"not_found"})
        except APIError as e:return self._send(e.status,{"error":e.code,"message":e.message})
    def do_POST(self):
        try:
            if self.path=='/api/v1/projects':return self._send(201,create_project(service,self._body()))
            if self.path.startswith('/api/v1/projects/') and self.path.endswith('/audit'):return self._send(200,audit_project(service,self.path.split('/')[4],))
            return self._send(404,{"error":"not_found"})
        except APIError as e:return self._send(e.status,{"error":e.code,"message":e.message})

def run(host=None,port=None):HTTPServer((host or '127.0.0.1',int(port or 8000)),Handler).serve_forever()
