import zipfile
from xlrd import open_workbook
import glob
import re

class DocsInitialVerification:
    source_dump_file_name = ''
    source_data = {}
    document_directory = ''

    def __init__(self, source_dump_file_name, document_directory):
        self.source_dump_file_name = source_dump_file_name
        self.document_directory = document_directory
        self.get_source_data()

    def get_source_data(self):
        wb = open_workbook(self.source_dump_file_name)
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
                       
                self.source_data[reference_id] = values
        return self.source_data

    def initial_doc_verification(self):
        # check doc count === source data element count
        # ref id of each doc exists in source data  
        file_list = glob.glob(self.document_directory + '/*.pdf')
        reference_ids = self.source_data.keys()

        if len(file_list) != len(reference_ids):
            pass
            #raise Exception('Record count doesn\' match')
        
        for file in file_list:
            file_name = DocsInitialVerification.get_file_name(file)
            if file_name not in reference_ids:
                print('Document '+ file + ' has invalid ref id')
        return

    @staticmethod 
    def get_file_name(file):
        try:
            file_name = re.search('documents/(.+?).pdf', file).group(1)
        except AttributeError:
            file_name = '' 
        return file_name   

docs_unzip = DocsInitialVerification('data/source_dump.xlsx', 'data/documents')
docs_unzip.initial_doc_verification()
