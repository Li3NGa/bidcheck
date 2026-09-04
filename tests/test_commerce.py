from bidcheck.commerce import CommerceService,SQLiteOrderRepository
from bidcheck.payment import PaymentSession

class FakeProvider:
    name='fake'
    def create_payment(self,request):
        return PaymentSession(self.name,request.order_id,f'https://pay.test/{request.order_id}')
    def verify_callback(self,payload,signature):
        assert signature=='ok'
        return payload.decode()

def test_paid_order_activates_entitlement(tmp_path):
    service=CommerceService(SQLiteOrderRepository(str(tmp_path/'commerce.db')),FakeProvider())
    order=service.create_order('u1','pro')
    session=service.checkout(order.order_id,'https://example.test/callback')
    assert session.order_id==order.order_id
    result=service.confirm(order.order_id,b'trade-1','ok')
    assert result['status']=='paid'
    assert service.entitlement('u1')['plan']=='pro'
    assert service.confirm(order.order_id,b'trade-1','bad')['idempotent'] is True
