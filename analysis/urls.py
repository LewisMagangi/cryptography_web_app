from django.urls import path
from .views import (
    AnalysisFormView, 
    KeySizeAnalysisView,
    FileSizeAnalysisView
)

app_name = 'analysis'

urlpatterns = [
    path('', AnalysisFormView.as_view(), name='form'),
    path('keysize/', KeySizeAnalysisView.as_view(), name='keysize_results'),
    path('filesize/', FileSizeAnalysisView.as_view(), name='filesize_results'),
]