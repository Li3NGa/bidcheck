from __future__ import annotations
import json
from http.server import BaseHTTPRequestHandler,HTTPServer
from .api import BidCheckService
from .http_api import APIError
from .store import MemoryProjectRepository

service=BidCheckService(MemoryProjectRepository())

class Handler(BaseHTTPRequestHandler):
    def _send(self,status,payload):
        body=json.dumps(payload,ensure_ascii=False,default=str).encode()
        self.send_response(status); self.send_header('Content-Type','application/json; charset=utf-8'); self.send_header('Content-Length',str(len(body))); self.end_headers(); self.wfile.write(body)
    def do_GET(self):
        if self.path=='/health': return self._send(200,{"status":"ok","service":"bidcheck"})
        if self.path.startswith('/api/v1/projects/'):
            try: return self._send(200,__import__('bidcheck.http_api',fromlist=['get_project']).get_project(service,self.path.rsplit('/',1)[-1]))
            except APIError as e: return self._send(e.status,{"error":e.code,"message":e.message})
        return self._send(404,{"error":"not_found"})

def run(host='127.0.0.1',port=8000): HTTPServer((host,port),Handler).serve_forever()
