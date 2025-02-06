from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, TemplateView
from django.urls import reverse_lazy

from .models import FileAnalysis
from .forms import AnalysisForm
from .src.time_gen import SymmetricTimeCalculator, AsymmetricTimeCalculator, HashingTimeCalculator
from .src.graph_gen import GraphGenerator
from .utils import format_processing_data

class AnalysisFormView(LoginRequiredMixin, FormView):
    template_name = 'analysis/analysis_form.html'
    form_class = AnalysisForm

    def get_success_url(self):
        crypto_type = self.request.session.get('crypto_type')
        analysis_type = self.request.session.get('analysis_type')
        
        # Always redirect hash algorithms to filesize view
        if crypto_type == 'hash':
            return reverse_lazy('analysis:filesize_results')
            
        if analysis_type == 'keysize':
            return reverse_lazy('analysis:keysize_results')
        return reverse_lazy('analysis:filesize_results')

    def form_valid(self, form):
        if 'analysis_file' not in self.request.FILES:
            form.add_error(None, "File is required for analysis")
            return self.form_invalid(form)

        file = self.request.FILES['analysis_file']

        # Force filesize analysis for hash algorithms
        if form.cleaned_data['crypto_type'] == 'hash':
            analysis_type = 'filesize'
        else:
            analysis_type = form.cleaned_data['analysis_type']

        analysis = FileAnalysis.objects.create(
            user=self.request.user,
            file_name=file.name,
            file_size=file.size / 1024,  # Convert to KB
            file_type=file.content_type,
            crypto_type=form.cleaned_data['crypto_type'],
            algorithm=form.cleaned_data['algorithm'],
            analysis_type=analysis_type
        )
        
        self.request.session['analysis_id'] = analysis.id
        self.request.session['analysis_type'] = analysis_type
        self.request.session['crypto_type'] = form.cleaned_data['crypto_type']
        return super().form_valid(form)

class KeySizeAnalysisView(TemplateView):
    template_name = 'analysis/keysize_results.html'

    def dispatch(self, request, *args, **kwargs):
        # Redirect hash analysis to filesize view
        if request.session.get('crypto_type') == 'hash':
            return redirect('analysis:filesize_results')
        return super().dispatch(request, *args, **kwargs)

    def get_calculator(self, crypto_type):
        if crypto_type == 'symmetric':
            return SymmetricTimeCalculator()
        elif crypto_type == 'asymmetric':
            return AsymmetricTimeCalculator()
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        analysis_id = self.request.session.get('analysis_id')
        
        if not analysis_id:
            return context

        analysis = get_object_or_404(FileAnalysis, id=analysis_id)
        calculator = self.get_calculator(analysis.crypto_type)
        if calculator:
            graph_gen = GraphGenerator(calculator)
            plot_html = graph_gen.generate_keysize_analysis(
                algorithm=analysis.algorithm,
                file_size=analysis.file_size
            )
            
            context['analysis'] = {
                'algorithm': analysis.algorithm,
                'crypto_type': analysis.crypto_type,
                'file_size': analysis.file_size,
                'file_name': analysis.file_name,
                'analysis_type': 'keysize'
            }
            context['plot_html'] = plot_html
        return context

class FileSizeAnalysisView(TemplateView):
    template_name = 'analysis/filesize_analysis.html'  # Update template path

    def get_calculator(self, crypto_type):
        if crypto_type == 'symmetric':
            return SymmetricTimeCalculator()
        elif crypto_type == 'asymmetric':
            return AsymmetricTimeCalculator()
        return HashingTimeCalculator()

    def _get_comparison_label(self, factor):
        """Get readable label for size comparison."""
        if factor == 1.0:
            return "Base Size (100%)"
        percentage = factor * 100
        return f"{'Smaller' if factor < 1 else 'Larger'} Size ({percentage:.0f}%)"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        analysis_id = self.request.session.get('analysis_id')
        
        if not analysis_id:
            return context

        analysis = get_object_or_404(FileAnalysis, id=analysis_id)
        calculator = self.get_calculator(analysis.crypto_type)
        
        if calculator:
            is_asymmetric = isinstance(calculator, AsymmetricTimeCalculator)
            file_size_bytes = analysis.file_size * 1024
            
            context['analysis'] = {
                'algorithm': analysis.algorithm,
                'crypto_type': analysis.crypto_type,
                'file_name': analysis.file_name,
                'file_size_bytes': file_size_bytes,
                'file_size_kb': analysis.file_size,
                'file_size_mb': analysis.file_size / 1024,
            }
            
            # Get results and prepare intervals
            results = calculator.get_time_results(analysis.algorithm, analysis.file_size)
            factors = [0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6]
            interval_rows = []
            
            for op, result in results.items():
                if isinstance(result, dict):
                    rate = result.get('rate', 0)
                    file_size_mb = analysis.file_size / 1024
                    
                    for factor in factors:
                        size_mb = file_size_mb * factor
                        if rate > 0:
                            estimated_time = (size_mb * 1024 * 1024) / rate if is_asymmetric else size_mb / rate
                        else:
                            estimated_time = 0
                            
                        interval_rows.append({
                            'operation': op,
                            'comparison_label': self._get_comparison_label(factor),
                            'size_mb': size_mb,
                            'estimated_time': estimated_time,
                            'rate': rate / (1024 * 1024) if is_asymmetric else rate,
                            'is_base_size': factor == 1.0
                        })
            
            context['intervals'] = sorted(interval_rows, key=lambda x: (x['operation'], x['size_mb']))
            
        return context