from django.shortcuts import render, redirect
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
            metric=form.cleaned_data['metric'],
            visualization=form.cleaned_data['visualization'],
            bar_type=form.cleaned_data.get('bar_type')
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
        
        calculator = SymmetricTimeCalculator()  # For now, just handling symmetric
        time_results = calculator.calculate_time(
            algorithm=analysis.algorithm,
            file_size_kb=analysis.file_size
        )
        
        graph_gen = GraphGenerator(calculator)
        plot_html = graph_gen.generate_plot(
            file_details={
                'file_name': analysis.file_name,
                'file_size': analysis.file_size,
                'file_type': analysis.file_type,
                'algorithm': analysis.algorithm
            },
            time_results=time_results
        )
        
        return render(request, 'analysis/results.html', {
            'plot_html': plot_html,
            'analysis': analysis
        })
