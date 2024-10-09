from django.db import models

class Patient(models.Model):
    PatientName = models.CharField(max_length=100)
    noteMedical = models.TextField(max_length=500)
    UltrasoundImg = models.ImageField(upload_to='UltrasoundImgs/')
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.PatientName
