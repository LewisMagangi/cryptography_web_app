# Create your models here.

from django.contrib import admin
from .models import Profile
from .models import SymmetricAnalysisResult

admin.site.register(SymmetricAnalysisResult)
admin.site.register(Profile)
