from django.db import models
from django.contrib.postgres.fields import ArrayField

class Education(models.Model):
    institution = models.CharField(max_length=255,null=True,blank=True)
    degree= models.CharField(max_length=255, null= True, blank = True)
    start_date= models.CharField(max_length=50, null=True, blank=True)
    end_date= models.CharField(max_length=50, null=True, blank=True)

class Resume(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    contact_number = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    skills = models.JSONField(default=list, blank=True)
    educations = models.JSONField(default=list, blank=True)
    work_experiences = models.JSONField(default=list, blank=True)
    YoE = models.CharField(max_length=50, null=True, blank=True)
    pdf_file = models.FileField(upload_to="resumes/", null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    

