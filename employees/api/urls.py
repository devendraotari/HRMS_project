from django.urls import path
from employees.api.views import EmployeeProfileAPIView, LeaveAPIView

# from rest_framework.routers import DefaultRouter
#
# router = DefaultRouter()
#
# router.register("leave-request",LeaveRequestViewSet,basename="leave-request")
urlpatterns = [
    path("emp-profile/", EmployeeProfileAPIView.as_view()),
    path("emp-profile/<str:pk>", EmployeeProfileAPIView.as_view()),
    path("leave/", LeaveAPIView.as_view()),
    path("leave/<int:pk>", LeaveAPIView.as_view())
]
# urlpatterns+=router.urls

