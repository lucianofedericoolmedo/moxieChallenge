from django.urls import path
from .views import ServiceListCreate, ServiceRetrieveUpdate,AppointmentList, AppointmentRetrieveUpdate
urlpatterns = [
    path('services/', ServiceListCreate.as_view(), name='service-list-create'),
    path('services/<int:pk>/', ServiceRetrieveUpdate.as_view({'get': 'retrieve', 'patch': 'update'}), name='service-retrieve-update'),
    path('appointments/', AppointmentList.as_view(), name='appointment-list'),  # GET
    path('appointments/<int:pk>/', AppointmentRetrieveUpdate.as_view({'get': 'retrieve', 'patch': 'update'}), name='appointment-retrieve-update'),
]