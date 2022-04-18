from django.urls import path
from products.apiviews import BoxListView, CreateBox, StaffBoxListView, StaffBoxView


urlpatterns = [
    path("box/<int:pk>", StaffBoxView.as_view(), name="update-delete-box"),
    path("new-box/", CreateBox.as_view(), name="create-new-box"),
    path("available-boxes/", BoxListView.as_view(), name="list-all-boxes-available"),
    path("staff-boxes/", StaffBoxListView.as_view(), name="list-staff-boxes"),
]
