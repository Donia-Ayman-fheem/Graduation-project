from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, 'accounts/home.html')

@login_required
def body_measurements(request):
    """View for the body measurements form"""
    return render(request, 'accounts/body_measurements_form.html')
