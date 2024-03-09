from . import views
from django.urls import path


urlpatterns = [
    path('', views.ThingList.as_view(), name='home'),
    path('<slug:slug>/', views.ThingDetail.as_view(), name='thing_detail'),
]
