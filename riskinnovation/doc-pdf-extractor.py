import zipfile
from xlrd import open_workbook
import glob
import csv
import xlwt
from ca_automation import lib
from riskinnovation import settings

class DocsPdfExtration:
    source_file_name = ''
    source_data = {}
    document_directory = ''

    def __init__(self, source_file_name, document_directory):
        self.source_file_name = source_file_name
        self.document_directory = document_directory
        self.meta_data_file = 'data/meta-data/processed-record.csv'
        self.source_data = lib.get_source_data(source_file_name)

    def get_document_list(self):
        doc_list = glob.glob(self.document_directory + '/*.pdf')
        return doc_list

    def start_processing(self):
        dock_list = self.get_document_list()
        self.process_documents(dock_list)
        return
    
    def process_documents(self, dock_list):
        for doc in dock_list:
            self.process_document(doc)

    def process_document(self, doc):
        self.start()

        self.end(doc)
    
    def start(self):
        return

    def end(self, doc):
        with open(self.meta_data_file, 'a', newline = '') as csvFile:
            csvWriter = csv.writer(csvFile, delimiter = ',')
            csvWriter.writerow([lib.get_file_name(doc)])

bas_path = settings.BASE_DIR  + '/data/'
docs_pdf_extration = DocsPdfExtration(bas_path +'source_dump.xlsx', bas_path + 'documents')
docs_pdf_extration.start_processing()
