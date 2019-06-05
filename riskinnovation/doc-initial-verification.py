import zipfile
from xlrd import open_workbook
import glob
from ca_automation import lib

class DocsInitialVerification:
    source_dump_file_name = ''
    source_data = {}
    document_directory = ''

    def __init__(self, source_dump_file_name, document_directory):
        self.source_dump_file_name = source_dump_file_name
        self.document_directory = document_directory
        self.source_data = lib.get_source_data(source_dump_file_name)

    def initial_doc_verification(self):
        # check doc count === source data element count
        # ref id of each doc exists in source data  
        file_list = glob.glob(self.document_directory + '/*.pdf')
        reference_ids = self.source_data.keys()
        if len(file_list) != len(reference_ids):
            pass
            #raise Exception('Record count doesn\' match')
        
        for file in file_list:
            file_name = lib.get_file_name(file)
            if file_name not in reference_ids:
                print('Document '+ file + ' has invalid ref id')
        return

docs_unzip = DocsInitialVerification('data/source_dump.xlsx', 'data/documents')
docs_unzip.initial_doc_verification()
