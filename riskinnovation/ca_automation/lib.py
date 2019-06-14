from riskinnovation import settings
from django.core.files.storage import FileSystemStorage
import re
from xlrd import open_workbook
import os


def handle_uploaded_file(file, type):
    file_path = settings.BASE_DIR  + '/data/' + file_name_with_extension(type)
    fs = FileSystemStorage()

    if fs.exists(file_path):
        fs.delete(file_path)

    fs.save(file_path, file)


def file_type_exists(type):
    file_path = settings.BASE_DIR + '/data/' + file_name_with_extension(type)
    fs = FileSystemStorage()
    return fs.exists(file_path)


def file_name_with_extension(type):

    file_type_mapping = {
        'mapping': 'mapping.xlsx',
        'source_dump': 'source_dump.xlsx',
        'documents': 'documents.zip',
        'processing': 'meta-data/processing.txt',
        'failed': 'meta-data/failed.txt',
        'success': 'meta-data/success.txt'
    }
        
    return file_type_mapping.get(type, '')


def get_reference_id_from_file_name(file):
    try:
        file_name = re.search('documents/(.+?).pdf', file).group(1)
    except AttributeError:
        file_name = ''
    return file_name


def get_source_data(source_file_name):
    source_data = {}
    wb = open_workbook(source_file_name)
    for sheet in wb.sheets():
        number_of_rows = sheet.nrows
        number_of_columns = sheet.ncols
        rows = []
        #reading headers
        # For row 0 and column 0
        sheet.cell_value(0, 0)
        headers = []
        for i in range(sheet.ncols):
            headers.append(sheet.cell_value(0, i))

        for row in range(1, number_of_rows):
            values = {}
            reference_id = 0
            for col in range(number_of_columns):
                value  = (sheet.cell(row,col).value)
                try:
                    value = str(int(value))
                except ValueError:
                    pass
                finally:
                    if col == 1:
                        reference_id = value
                    values[headers[col]] = value

            source_data[reference_id] = values
    return source_data


def remove_file(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)
    else:
        print("The file does not exist")
