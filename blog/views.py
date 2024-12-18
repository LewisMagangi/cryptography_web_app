# Creating Views

from django.shortcuts import render
from django.http import HttpResponse


posts = [
    {
        'author':'Lewis',
        'title':'Blog Post 1',
        'content':'This is the first post.',
        'date_posted':'2024-11-12'
    },
    {
        'author':'Mark',
        'title':'Blog Post 2',
        'content':'This is the second post.',
        'date_posted':'2024-11-12'
    }
]

def home(request):
    context = {
        'posts': posts
    }
    return render(request, 'blog/home.html', context)


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})