from django.urls import path
from .views import AnalysisFormView, ResultsView

urlpatterns = [
    path('', AnalysisFormView.as_view(), name='analysis-form'),
    path('results/', ResultsView.as_view(), name='analysis-results'),
]