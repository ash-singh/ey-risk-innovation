from riskinnovation import settings
from django.core.files.storage import FileSystemStorage
import re
from xlrd import open_workbook

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

def get_file_name(file):
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