import json
from datetime import timedelta
from pickle import TRUE

from django.utils import timezone
from django_filters.rest_framework import FilterSet, NumberFilter
from rest_framework import status
from rest_framework.exceptions import PermissionDenied

from products.models import (
    MAX_AVG_AREA,
    MAX_AVG_VOLUME,
    MAX_STAFF_WEEK_BOXES,
    MAX_TOTAL_WEEK_BOXES,
    Box,
)

MAX_COUNT_ERROR = {
    "status": status.HTTP_400_BAD_REQUEST,
    "message": "Total box count exceding!",
}
MAX_STAFF_COUNT_ERROR = {
    "status": status.HTTP_400_BAD_REQUEST,
    "message": "Total staff's box count exceding!",
}
MAX_AREA_ERROR = {
    "status": status.HTTP_400_BAD_REQUEST,
    "message": "Total average box area exceding!",
}
MAX_VOLUME_ERROR = {
    "status": status.HTTP_400_BAD_REQUEST,
    "message": "Total average box volume exceding!",
}


class MyCustomExcpetion(PermissionDenied):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Custom Exception Message"
    default_code = "invalid"

    def __init__(self, detail, status_code=None):
        self.detail = detail
        if status_code is not None:
            self.status_code = status_code


def is_constraint_valid(user, data):
    totalArea = data["length"] * data["width"]
    totalVolume = data["length"] * data["width"] * data["height"]
    lastWeekDay = timezone.now().date() - timedelta(days=7)
    totalStaffBoxCount = Box.objects.filter(
        created_by=user, created_at__gte=lastWeekDay
    ).count()
    totalWeekBoxCount = Box.objects.filter(created_at__gte=lastWeekDay).count()
    BoxData = Box.objects.values_list("area", "volume")
    totalBoxCount = len(BoxData)

    for box in BoxData:
        totalArea += box[0]
        totalVolume += box[1]

    averageArea = totalArea / totalBoxCount
    averageVolume = totalVolume / totalBoxCount

    if totalWeekBoxCount > MAX_TOTAL_WEEK_BOXES:
        raise MyCustomExcpetion(
            detail=MAX_COUNT_ERROR, status_code=status.MAX_COUNT_ERROR["status"]
        )
    elif totalStaffBoxCount > MAX_STAFF_WEEK_BOXES:
        raise MyCustomExcpetion(
            detail=MAX_STAFF_COUNT_ERROR, status_code=MAX_STAFF_COUNT_ERROR["status"]
        )
    elif averageArea > MAX_AVG_AREA:
        raise MyCustomExcpetion(
            detail=MAX_AREA_ERROR, status_code=MAX_AREA_ERROR["status"]
        )
    elif averageVolume > MAX_AVG_VOLUME:
        raise MyCustomExcpetion(
            detail=MAX_VOLUME_ERROR, status_code=MAX_VOLUME_ERROR["status"]
        )

    return TRUE


class BoxFilter(FilterSet):
    length_gt = NumberFilter(field_name="length", lookup_expr="gt")
    length_lt = NumberFilter(field_name="length", lookup_expr="lt")
    widht_gt = NumberFilter(field_name="width", lookup_expr="gt")
    width_lt = NumberFilter(field_name="width", lookup_expr="lt")
    height_gt = NumberFilter(field_name="height", lookup_expr="gt")
    height_lt = NumberFilter(field_name="height", lookup_expr="lt")
    area_gt = NumberFilter(field_name="area", lookup_expr="gt")
    area_lt = NumberFilter(field_name="area", lookup_expr="lt")
    volume_gt = NumberFilter(field_name="volume", lookup_expr="gt")
    volume_lt = NumberFilter(field_name="volume", lookup_expr="lt")


def parse_body(body):
    body_unicode = body.decode("utf-8")
    return json.loads(body_unicode)
