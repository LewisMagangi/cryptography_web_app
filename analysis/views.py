from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, View
from django.contrib.auth.decorators import login_required

# Local imports
from .models import FileAnalysis
from .forms import AnalysisForm
from .src.time_gen import SymmetricTimeCalculator, AsymmetricTimeCalculator, HashingTimeCalculator
from .src.graph_gen import GraphGenerator

class AnalysisFormView(LoginRequiredMixin, FormView):
    template_name = 'analysis/analysis_form.html'
    form_class = AnalysisForm
    success_url = '/analysis/results/'

    def form_valid(self, form):
        file = self.request.FILES['analysis_file']
        
        analysis = FileAnalysis.objects.create(
            user=self.request.user,
            file_name=file.name,
            file_size=file.size / 1024,  # Convert to KB
            file_type=file.content_type,
            crypto_type=form.cleaned_data['crypto_type'],
            algorithm=form.cleaned_data['algorithm'],
            metric=form.cleaned_data['metric']
        )
        
        # Initialize appropriate calculator based on crypto type
        if analysis.crypto_type == 'symmetric':
            calculator = SymmetricTimeCalculator()
        elif analysis.crypto_type == 'asymmetric':
            calculator = AsymmetricTimeCalculator()
        else:
            calculator = HashingTimeCalculator()

        # Calculate estimated time
        time_result = calculator.calculate_time(
            algorithm=analysis.algorithm,
            file_size_kb=analysis.file_size,
            operation='encryption'
        )
        
        analysis.estimated_time = time_result['estimated_time']
        analysis.save()
        
        self.request.session['analysis_id'] = analysis.id
        return super().form_valid(form)

class ResultsView(LoginRequiredMixin, View):
    def get(self, request):
        analysis_id = request.session.get('analysis_id')
        analysis = FileAnalysis.objects.get(id=analysis_id)
        
        # Initialize appropriate calculator
        if analysis.crypto_type == 'symmetric':
            calculator = SymmetricTimeCalculator()
        elif analysis.crypto_type == 'asymmetric':
            calculator = AsymmetricTimeCalculator()
        else:
            calculator = HashingTimeCalculator()
        
        # Pass actual file size in KB for proper interval calculation
        graph_gen = GraphGenerator(calculator)
        plot_html = graph_gen.generate_graph_data(
            algorithm=analysis.algorithm,
            file_size=analysis.file_size  # Already in KB
        )
        
        return render(request, 'analysis/results.html', {
            'plot_html': plot_html,
            'analysis': analysis
        })

# Remove or comment out the duplicate analysis_results function since ResultsView handles this now
# def analysis_results(request, analysis_id):
#     ...
