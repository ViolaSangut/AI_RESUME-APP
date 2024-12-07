from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.resume_upload, name='resume_upload'),
       path('analysis/<int:resume_id>/', views.resume_analysis, name='resume_analysis'),
    path('analysis/', views.resume_analysis, name='resume_analysis'),
path('resumes/matches-overview/', views.resume_matches_overview, name='resume_matches_overview'),
]
