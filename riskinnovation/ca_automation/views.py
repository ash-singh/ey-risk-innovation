from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from riskinnovation import settings
from .forms import CAAutomation
from . import lib
import subprocess


def index(request):
    if request.method == 'POST':
        form = CAAutomation(request.POST, request.FILES)
        if form.is_valid():
            mapping_file = request.FILES['mapping_file']
            source_dump = request.FILES['system_dump']
            docs = request.FILES['documents']
            lib.handle_uploaded_file(mapping_file, 'mapping')
            lib.handle_uploaded_file(source_dump, 'source_dump')
            lib.handle_uploaded_file(docs, 'documents')
            
            subprocess.call(["python", settings.BASE_DIR+"/doc-unzip.py"])
            
            return HttpResponseRedirect('dashboard')
        return HttpResponse(form.errors)
    context = {
        'app_name': 'CA Automation',
        'form': CAAutomation()
    }
    return render(request, 'ca_automation/index.html', context)


def dashboard(request):
    context = {
        'mapping_file': lib.file_type_exists('mapping_file'),
        'source_dump': lib.file_type_exists('source_dump'),
        'documents': lib.file_type_exists('documents'),
        'processing': lib.file_type_exists('processing'),
        'failed': lib.file_type_exists('failed'),
        'success': lib.file_type_exists('success'),
    }
    
    return render(request, 'ca_automation/dashboard.html', context)


def start_processing(request):
    subprocess.call(["python", settings.BASE_DIR+"/doc-initial-verification.py"])
    return HttpResponseRedirect('dashboard')


def report(request):
    context = {}
    return render(request, 'ca_automation/report.html', context)
