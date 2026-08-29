from __future__ import annotations
from .health import health

def health_response()->dict:
    return health()

def upload_limits()->dict:
    from .upload import ALLOWED_SUFFIXES,DEFAULT_MAX_BYTES
    return {'allowed_types':sorted(ALLOWED_SUFFIXES),'max_bytes':DEFAULT_MAX_BYTES}
