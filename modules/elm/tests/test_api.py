import pytest
from datetime import date
from decimal import Decimal
from rest_framework.test import APIClient
from modules.elm.models import LeaveBalance, LeaveRequest
from conftest import make_session

@pytest.fixture
def auth_client(stub_iam):
    client = APIClient()
    session = make_session(
        user_id=101,
        modules=("elm",),
        permissions=("elm.leave.view_self", "elm.leave.apply", "elm.leave.review"),
        kind="faculty",
        roles=("faculty",),
    )
    stub_iam(session=session)
    client.credentials(HTTP_AUTHORIZATION="Token abc")
    return client

@pytest.mark.django_db
def test_api_catalog(auth_client):
    res = auth_client.get("/api/v1/elm/catalog")
    assert res.status_code == 200
    assert "CL" in res.data["entitlements"]

@pytest.mark.django_db
def test_api_leave_balances(auth_client):
    LeaveBalance.objects.create(
        user_id=101, category="CL", year=date.today().year,
        credited=Decimal("8.00"), availed=Decimal("0.00"), balance=Decimal("8.00")
    )
    res = auth_client.get("/api/v1/elm/balances")
    assert res.status_code == 200
    assert len(res.data) == 1
    assert res.data[0]["category"] == "CL"

@pytest.mark.django_db
def test_api_apply_and_withdraw_leave(auth_client):
    LeaveBalance.objects.create(
        user_id=101, category="CL", year=2026,
        credited=Decimal("8.00"), availed=Decimal("0.00"), balance=Decimal("8.00")
    )
    payload = {
        "category": "CL",
        "start_date": "2026-11-02",
        "end_date": "2026-11-02",
        "purpose": "Personal errand",
    }
    res = auth_client.post("/api/v1/elm/requests", payload, format="json")
    assert res.status_code == 201
    req_id = res.data["id"]
    assert res.data["status"] == "under_review"

    # Withdraw
    res_w = auth_client.post(f"/api/v1/elm/requests/{req_id}/withdraw")
    assert res_w.status_code == 200
    assert res_w.data["status"] == "withdrawn"
