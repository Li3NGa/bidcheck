from __future__ import annotations
import json
from http.server import BaseHTTPRequestHandler,HTTPServer
from pathlib import Path
from .api import BidCheckService
from .http_api import APIError,create_project,get_project,audit_project,list_projects
from .upload_api import create_project_from_upload,attach_response_from_upload
from .plan_api import current_plan
from .commerce import CommerceService,SQLiteOrderRepository
from .commerce_api import pricing,create_order,checkout,confirm,entitlement
from .payment import DisabledPaymentProvider
from .rate_limit import FixedWindowLimiter
from .sqlite_store import SQLiteProjectRepository
from .config import load_settings

settings=load_settings()
service=BidCheckService(SQLiteProjectRepository(settings.db_path))
commerce=CommerceService(SQLiteOrderRepository(settings.db_path),DisabledPaymentProvider())
WEB_INDEX=Path(__file__).resolve().parent.parent/'web'/'index.html'
limiter=FixedWindowLimiter(limit=120,window_seconds=60)

class Handler(BaseHTTPRequestHandler):
    def _guard(self):
        if not limiter.allow(self.client_address[0]): raise APIError(429,'rate_limited','too many requests')
    def _send(self,status,payload):
        body=json.dumps(payload,ensure_ascii=False,default=str).encode(); self.send_response(status); self.send_header('Content-Type','application/json; charset=utf-8'); self.send_header('Content-Length',str(len(body))); self.send_header('Cache-Control','no-store');
        if status==429:self.send_header('Retry-After','60')
        self.end_headers(); self.wfile.write(body)
    def _body(self):
        try:
            size=int(self.headers.get('Content-Length','0') or 0)
            if size>settings.max_body_bytes: raise APIError(413,'body_too_large','request body too large')
            return json.loads(self.rfile.read(size))
        except APIError: raise
        except (ValueError,json.JSONDecodeError) as exc: raise APIError(400,'invalid_json','request body must be valid JSON') from exc
    def _web(self):
        body=WEB_INDEX.read_bytes(); self.send_response(200); self.send_header('Content-Type','text/html; charset=utf-8'); self.send_header('Content-Length',str(len(body))); self.end_headers(); self.wfile.write(body)
    def do_GET(self):
        try:
            self._guard()
            if self.path=='/': return self._web()
            if self.path=='/health': return self._send(200,{"status":"ok","service":"bidcheck"})
            if self.path=='/api/v1/plan': return self._send(200,current_plan(service))
            if self.path=='/api/v1/pricing': return self._send(200,pricing())
            if self.path.startswith('/api/v1/users/') and self.path.endswith('/entitlement'): return self._send(200,entitlement(commerce,self.path.split('/')[4]))
            if self.path=='/api/v1/projects': return self._send(200,list_projects(service))
            if self.path.startswith('/api/v1/projects/'): return self._send(200,get_project(service,self.path.rsplit('/',1)[-1]))
            return self._send(404,{"error":"not_found"})
        except APIError as e:return self._send(e.status,{"error":e.code,"message":e.message})
        except (KeyError,ValueError) as e:return self._send(400,{"error":"invalid_request","message":str(e)})
    def do_POST(self):
        try:
            self._guard()
            if self.path=='/api/v1/orders': return self._send(201,create_order(commerce,self._body()))
            if self.path.startswith('/api/v1/orders/') and self.path.endswith('/checkout'):
                body=self._body(); return self._send(200,checkout(commerce,self.path.split('/')[4],str(body.get('notify_url',''))))
            if self.path.startswith('/api/v1/orders/') and self.path.endswith('/confirm'):
                body=self._body(); return self._send(200,confirm(commerce,self.path.split('/')[4],str(body.get('payload','')).encode(),str(body.get('signature',''))))
            if self.path=='/api/v1/projects/upload': return self._send(201,create_project_from_upload(service,self._body()))
            if self.path.startswith('/api/v1/projects/') and self.path.endswith('/responses/upload'): return self._send(200,attach_response_from_upload(service,self.path.split('/')[4],self._body()))
            if self.path=='/api/v1/projects': return self._send(201,create_project(service,self._body()))
            if self.path.startswith('/api/v1/projects/') and self.path.endswith('/audit'): return self._send(200,audit_project(service,self.path.split('/')[4]))
            return self._send(404,{"error":"not_found"})
        except APIError as e:return self._send(e.status,{"error":e.code,"message":e.message})
        except RuntimeError as e:return self._send(503,{"error":"service_unavailable","message":str(e)})
        except (KeyError,ValueError) as e:return self._send(400,{"error":"invalid_request","message":str(e)})

def run(host=None,port=None):
    host=host or settings.host; port=int(port or settings.port); HTTPServer((host,port),Handler).serve_forever()
