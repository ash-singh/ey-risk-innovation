from riskinnovation import settings
from django.core.files.storage import FileSystemStorage

def handle_uploaded_file(file, type):
    file_path = settings.BASE_DIR  + '/data/' + file_name_with_extention(type)
    fs = FileSystemStorage()

    if fs.exists(file_path):
        fs.delete(file_path)

    fs.save(file_path, file)

def file_type_exists(type):
    file_path = settings.BASE_DIR  + '/data/' + file_name_with_extention(type)
    fs = FileSystemStorage()
    return fs.exists(file_path)

def file_name_with_extention(type):
    file_name = ''
    if type == 'mapping':
        file_name = 'mapping.xlsx'
    if type == 'source_dump':
        file_name = 'source_dump.xlsx'
    if type == 'documents':
        file_name = 'documents.zip'
    return file_name
