from __future__ import annotations
from .billing import Subscription
from .usage import Usage,consume_audit

def charge_audit(subscription:Subscription,usage:Usage)->Usage:
    limit=__import__('bidcheck.billing',fromlist=['LIMITS']).LIMITS[subscription.plan]['audits']
    if not subscription.allows('audits',usage.audits):
        raise PermissionError('subscription does not allow another audit')
    return consume_audit(usage,limit)
