from __future__ import annotations
import json
from http.server import BaseHTTPRequestHandler,HTTPServer
from .api import BidCheckService
from .http_api import APIError,create_project,get_project,audit_project,list_projects
from .upload_api import create_project_from_upload,attach_response_from_upload
from .plan_api import current_plan
from .sqlite_store import SQLiteProjectRepository
from .config import load_settings

settings=load_settings()
service=BidCheckService(SQLiteProjectRepository(settings.db_path))

class Handler(BaseHTTPRequestHandler):
    def _send(self,status,payload):
        body=json.dumps(payload,ensure_ascii=False,default=str).encode(); self.send_response(status); self.send_header('Content-Type','application/json; charset=utf-8'); self.send_header('Content-Length',str(len(body))); self.send_header('Cache-Control','no-store'); self.end_headers(); self.wfile.write(body)
    def _body(self):
        try:
            size=int(self.headers.get('Content-Length','0') or 0)
            if size>settings.max_body_bytes: raise APIError(413,'body_too_large','request body too large')
            return json.loads(self.rfile.read(size))
        except APIError: raise
        except (ValueError,json.JSONDecodeError) as exc: raise APIError(400,'invalid_json','request body must be valid JSON') from exc
    def do_GET(self):
        try:
            if self.path=='/health': return self._send(200,{"status":"ok","service":"bidcheck"})
            if self.path=='/api/v1/plan': return self._send(200,current_plan(service))
            if self.path=='/api/v1/projects': return self._send(200,list_projects(service))
            if self.path.startswith('/api/v1/projects/'):
                return self._send(200,get_project(service,self.path.rsplit('/',1)[-1]))
            return self._send(404,{"error":"not_found"})
        except APIError as e:return self._send(e.status,{"error":e.code,"message":e.message})
    def do_POST(self):
        try:
            if self.path=='/api/v1/projects/upload': return self._send(201,create_project_from_upload(service,self._body()))
            if self.path.startswith('/api/v1/projects/') and self.path.endswith('/responses/upload'):
                return self._send(200,attach_response_from_upload(service,self.path.split('/')[4],self._body()))
            if self.path=='/api/v1/projects': return self._send(201,create_project(service,self._body()))
            if self.path.startswith('/api/v1/projects/') and self.path.endswith('/audit'):
                return self._send(200,audit_project(service,self.path.split('/')[4]))
            return self._send(404,{"error":"not_found"})
        except APIError as e:return self._send(e.status,{"error":e.code,"message":e.message})

def run(host=None,port=None):
    host=host or settings.host; port=int(port or settings.port); HTTPServer((host,port),Handler).serve_forever()
