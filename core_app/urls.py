from django.urls import path
from . import views
from . import views_public

urlpatterns = [
    path("parse_resumes/", views.parse_resume_view, name="parse_resumes"),
    path('upload_resume/', views.upload_resume, name='upload_resume'),
    path('view_resume/<str:filename>/', views.view_resume_content, name='view_resume_content'),

     path("public_parse_resume/", views_public.public_parse_resume_view, name="public_parse_resume"),
    path("public_upload_resume/", views_public.public_upload_resume_page, name="public_upload_resume_page"),
]
