import pytest
from bidcheck.api import BidCheckService
from bidcheck.http_api import APIError,create_project,get_project
from bidcheck.store import MemoryProjectRepository

def test_create_requires_core_fields():
    with pytest.raises(APIError) as exc: create_project(BidCheckService(MemoryProjectRepository()),{})
    assert exc.value.status==400 and exc.value.code=='invalid_project'

def test_get_missing_project_maps_to_404():
    with pytest.raises(APIError) as exc: get_project(BidCheckService(MemoryProjectRepository()),'missing')
    assert exc.value.status==404
