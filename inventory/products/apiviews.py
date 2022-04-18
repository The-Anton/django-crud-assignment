from xml.dom.minidom import TypeInfo
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework import status

from products.models import Box
from products.permission import BOX_DELETION_ERROR_MSG, IsAuthenticated, StaffPermission, PermissionManager
from products.serializers import BoxCreateSerializer, BoxSerializer, StaffBoxSerializer
from products.utils import BoxFilter, MyCustomExcpetion, is_constraint_valid, parse_body


class FilterClass:
    filter_backends = (DjangoFilterBackend,)
    filterset_class = BoxFilter


class CreateBox(CreateModelMixin, GenericAPIView, PermissionManager):
    serializer_class = BoxCreateSerializer

    def post(self, request, *args, **kwargs):
        body = parse_body(request.body)
        is_constraint_valid(self.request.user, body)
        return self.create(request, *args, **kwargs)


class StaffBoxView(
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    GenericAPIView,
    PermissionManager,
    FilterClass,
):

    queryset = Box.objects.all()
    serializer_class = StaffBoxSerializer

    def get_queryset(self):
        return Box.objects.filter(created_by=self.request.user)

    def get_serializer_context(self):
        """Adds request to the context of serializer"""
        return {"request": self.request}

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, *kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if self.request.user == instance.created_by:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_200_OK)
        else:
            raise MyCustomExcpetion(
                detail=BOX_DELETION_ERROR_MSG, status_code=status.HTTP_403_FORBIDDEN
            )

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class StaffBoxListView(ListModelMixin, GenericAPIView, PermissionManager, FilterClass):

    queryset = Box.objects.all()
    serializer_class = StaffBoxSerializer

    permission_classes = [IsAuthenticated, StaffPermission]

    def get_queryset(self):
        return Box.objects.filter(created_by=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, *kwargs)


class BoxListView(ListModelMixin, GenericAPIView, PermissionManager, FilterClass):
    queryset = Box.objects.all()
    serializer_class = BoxSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, *kwargs)
