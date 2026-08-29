from bidcheck.product_api import create_from_tender,attach_response

class Repo:
    def __init__(self): self.items={}
    def save(self,p): self.items[p.project_id]=p
    def get(self,i): return self.items[i]

class Service:
    def __init__(self): self.repository=Repo()
    def create_project(self,p): self.repository.save(p); return {'project_id':p.project_id}
    def get_project(self,i): return self.repository.get(i)

def test_product_flow(tmp_path):
    tender=tmp_path/'t.txt'; tender.write_text('供应商必须具备有效资质',encoding='utf-8')
    response=tmp_path/'r.txt'; response.write_text('我方具备有效资质',encoding='utf-8')
    s=Service(); create_from_tender(s,'p1','demo',tender)
    result=attach_response(s,'p1',response)
    assert result['response_documents']==1
