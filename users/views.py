# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth.forms import  UserCreationForm
from django.contrib import messages
from .form import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from .models import SymmetricAnalysisResult
#import plotly.express as px
import matplotlib.pyplot as plt
import os
import io
import urllib, base64

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!, Login')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method =='POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            username=u_form.cleaned_data.get('username')
            messages.success(request, f'{username} Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form' : u_form,
        'p_from' : p_form
    }
    return render(request, 'users/profile.html', context)

@login_required
def chart(request):
    symmetric_analysis = SymmetricAnalysisResult.objects.filter(user=request.user)

    if not symmetric_analysis.exists():
        messages.warning(request, 'You have not performed any symmetric analysis yet')
        return redirect('profile')

    # Create the plot
    plt.figure(figsize=(10, 6))
    for algo in symmetric_analysis.values_list('algorithm', flat=True).distinct():
        algo_data = symmetric_analysis.filter(algorithm=algo)
        for key_size in algo_data.values_list('key_size', flat=True).distinct():
            key_data = algo_data.filter(key_size=key_size)
            data_sizes = key_data.values_list('file_name', flat=True)
            times = key_data.values_list('time_taken', flat=True)
            plt.plot(data_sizes, times, label=f"{algo} (Key Size: {key_size})")

    plt.title("Symmetric Analysis Time for Different Data Sizes")
    plt.xlabel("Data Size")
    plt.ylabel("Time Taken (seconds)")
    plt.legend()
    plt.grid(True)

    # Save the plot to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)

    return render(request, 'users/chart.html', {'data': uri})