from __future__ import annotations

from datetime import date
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from fusion_auth.permissions import HasModuleGrant, HasPermission
from modules.elm.api.serializers import (
    LeaveBalanceSerializer,
    LeaveRequestSerializer,
    ApplyLeaveInputSerializer,
    SubstituteActionInputSerializer,
    ReviewActionInputSerializer,
)
from modules.elm.domain.rules import ENTITLEMENTS
from modules.elm.models import LeaveBalance, LeaveRequest, SubstituteAssignment
from modules.elm.services.leave import (
    apply_for_leave,
    respond_substitute,
    review_leave_request,
    withdraw_leave_request,
    cancel_approved_leave,
)


class LeaveCatalogView(APIView):
    permission_classes = [HasModuleGrant("elm"), HasPermission("elm.leave.view_self")]

    def get(self, request):
        return Response({
            "entitlements": {key: str(value) for key, value in ENTITLEMENTS.items()}
        })


class MyLeaveBalancesView(APIView):
    permission_classes = [HasModuleGrant("elm"), HasPermission("elm.leave.view_self")]

    def get(self, request):
        user_id = request.principal.user_id
        current_year = timezone.now().year
        balances = LeaveBalance.objects.filter(user_id=user_id, year=current_year)
        serializer = LeaveBalanceSerializer(balances, many=True)
        return Response(serializer.data)


class MyLeaveRequestsView(APIView):
    permission_classes = [HasModuleGrant("elm"), HasPermission("elm.leave.view_self")]

    def get(self, request):
        user_id = request.principal.user_id
        requests = LeaveRequest.objects.filter(user_id=user_id).order_by("-created_at")
        serializer = LeaveRequestSerializer(requests, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ApplyLeaveInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        leave_req = apply_for_leave(
            user_id=request.principal.user_id,
            category=data["category"],
            start_date=data["start_date"],
            end_date=data["end_date"],
            half_day=data.get("half_day"),
            purpose=data["purpose"],
            is_station_leave=data.get("is_station_leave", False),
            destination=data.get("destination", ""),
            emergency_contact=data.get("emergency_contact", ""),
            substitute_id=data.get("substitute_id"),
        )
        return Response(LeaveRequestSerializer(leave_req).data, status=status.HTTP_201_CREATED)


class LeaveRequestDetailView(APIView):
    permission_classes = [HasModuleGrant("elm"), HasPermission("elm.leave.view_self")]

    def get(self, request, pk: int):
        leave_req = LeaveRequest.objects.filter(id=pk, user_id=request.principal.user_id).first()
        if not leave_req:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(LeaveRequestSerializer(leave_req).data)


class WithdrawLeaveView(APIView):
    permission_classes = [HasModuleGrant("elm"), HasPermission("elm.leave.apply")]

    def post(self, request, pk: int):
        leave_req = withdraw_leave_request(user_id=request.principal.user_id, request_id=pk)
        return Response(LeaveRequestSerializer(leave_req).data)


class CancelLeaveView(APIView):
    permission_classes = [HasModuleGrant("elm"), HasPermission("elm.leave.apply")]

    def post(self, request, pk: int):
        today = timezone.now().date()
        leave_req = cancel_approved_leave(user_id=request.principal.user_id, request_id=pk, today_date=today)
        return Response(LeaveRequestSerializer(leave_req).data)


class SubstituteTasksView(APIView):
    permission_classes = [HasModuleGrant("elm"), HasPermission("elm.leave.view_self")]

    def get(self, request):
        user_id = request.principal.user_id
        pending_assignments = SubstituteAssignment.objects.filter(
            substitute_id=user_id, status="pending"
        ).select_related("leave_request")
        requests = [a.leave_request for a in pending_assignments]
        return Response(LeaveRequestSerializer(requests, many=True).data)


class RespondSubstituteView(APIView):
    permission_classes = [HasModuleGrant("elm"), HasPermission("elm.leave.view_self")]

    def post(self, request, pk: int):
        serializer = SubstituteActionInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        assignment = respond_substitute(
            substitute_id=request.principal.user_id,
            request_id=pk,
            action=serializer.validated_data["action"],
            remarks=serializer.validated_data.get("remarks", ""),
        )
        return Response({"status": assignment.status})


class ReviewTasksView(APIView):
    permission_classes = [HasModuleGrant("elm"), HasPermission("elm.leave.review")]

    def get(self, request):
        pending_requests = LeaveRequest.objects.filter(
            status__in=["under_review", "recommended"]
        ).order_by("-created_at")
        return Response(LeaveRequestSerializer(pending_requests, many=True).data)


class ReviewDecisionView(APIView):
    permission_classes = [HasModuleGrant("elm"), HasPermission("elm.leave.review")]

    def post(self, request, pk: int):
        serializer = ReviewActionInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        leave_req = review_leave_request(
            reviewer_id=request.principal.user_id,
            request_id=pk,
            action=serializer.validated_data["action"],
            reason=serializer.validated_data.get("reason", ""),
        )
        return Response(LeaveRequestSerializer(leave_req).data)
