from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from .constants import CryptoType, MetricType

class FileAnalysis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    file_size = models.FloatField()  # in KB
    file_type = models.CharField(max_length=100)
    crypto_type = models.CharField(
        max_length=20,
        choices=[(t.value, t.name) for t in CryptoType]
    )
    algorithm = models.CharField(max_length=50)
    metric = models.CharField(
        max_length=50,
        choices=[(t.value, t.name) for t in MetricType]
    )
    timestamp = models.DateTimeField(default=timezone.now)
    estimated_time = models.FloatField(null=True)

    def __str__(self):
        return f"{self.algorithm} analysis on {self.file_name}"

    class Meta:
        verbose_name_plural = "File Analyses"
