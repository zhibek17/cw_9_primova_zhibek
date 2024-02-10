from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('announcement/<int:pk>/', AnnouncementDetailView.as_view(), name='announcement_detail'),
    path('announcement/сreate/', AnnouncementCreateView.as_view(), name='announcement_create'),
    path('announcement/update/<int:pk>/', AnnouncementUpdateView.as_view(), name='announcement_update'),
    path('announcement/<int:pk>/delete/', AnnouncementDeleteView.as_view(), name='announcement_delete'),
    path('announcement/<int:pk>/comment/add/', CommentCreateView.as_view(), name='comment_create'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
]