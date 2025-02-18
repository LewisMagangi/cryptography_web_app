from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class FileAnalysis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    file_size = models.FloatField()  # in KB
    file_type = models.CharField(max_length=100)
    crypto_type = models.CharField(max_length=20)
    algorithm = models.CharField(max_length=50)
    metric = models.CharField(max_length=50)
    visualization = models.CharField(max_length=20)
    bar_type = models.CharField(max_length=20, null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    estimated_time = models.FloatField(null=True)

    def __str__(self):
        return f"{self.algorithm} analysis on {self.file_name}"

    class Meta:
        verbose_name_plural = "File Analyses"
        db_table = 'analysis_fileanalysis'
