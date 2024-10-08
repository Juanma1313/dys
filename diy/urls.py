from . import views
from django.urls import path


urlpatterns = [
    path('', views.ThingList.as_view(), name='home'),
    path('<slug:slug>/', views.ThingDetail.as_view(), name='thing_detail'),
    path('like/<slug:slug>', views.ThingLike.as_view(), name='thing_like'),
    path('user/<str:form>', views.UserProfile.as_view(), name='user'),
    path('<slug:slug>/edit_comment/<int:comment_id>',
         views.comment_edit, name='comment_edit'),
    path('<slug:slug>/delete_comment/<int:comment_id>',
         views.comment_delete, name='comment_delete'),
]
