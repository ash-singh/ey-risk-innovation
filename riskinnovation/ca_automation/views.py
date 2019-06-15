from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from riskinnovation import settings
from .forms import CAAutomation
from . import lib
import subprocess
import os


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
        'mapping': lib.file_type_exists('mapping'),
        'source_dump': lib.file_type_exists('source_dump'),
        'documents': lib.file_type_exists('documents'),
        'processing': lib.file_type_exists('processing'),
        'failed': lib.file_type_exists('failed'),
        'success': lib.file_type_exists('success'),
    }
    if context['documents']:
        context['documents_count'] = lib.get_docs_count('data/documents')
    if context['source_dump']:
        context['source_dump_count'] = lib.get_source_dump_record_count()

    return render(request, 'ca_automation/dashboard.html', context)


def start_initial_processing(request):
    subprocess.call(["python", settings.BASE_DIR+"/doc-initial-verification.py"])
    return HttpResponseRedirect('dashboard')


def start_initial_complete_processing(request):
    subprocess.call(["python", settings.BASE_DIR+"/doc-complete-verification.py"])
    return HttpResponseRedirect('dashboard')


def download(request, file_type):
    file_path = lib.get_file_path(file_type)
    print(file_path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


def report(request):
    context = {}
    return render(request, 'ca_automation/report.html', context)
