import zipfile
from xlrd import open_workbook
import glob
from ca_automation import lib

class DocsInitialVerification:
    source_dump_file_name = ''
    source_data = {}
    document_directory = ''
    processing_file_pointer = ''
    failed_file_pointer = ''
    processing_file_name = ''
    failed_file_name = ''
    success_file_name = ''
    isFailed = False

    def __init__(self, source_dump_file_name, document_directory):
        self.source_dump_file_name = source_dump_file_name
        self.document_directory = document_directory
        self.source_data = lib.get_source_data(source_dump_file_name)
        self.processing_file_name = 'data/meta-data/processing.txt'
        self.failed_file_name = 'data/meta-data/failed.txt'
        self.success_file_name = 'data/meta-data/success.txt'


    def initial_doc_verification(self):
        # check doc count === source data element count
        # ref id of each doc exists in source data  

        self.start()
        file_list = glob.glob(self.document_directory + '/*.pdf')
        reference_ids = self.source_data.keys()
        if len(file_list) != len(reference_ids):
            pass
            #raise Exception('Record count doesn\' match')
        
        for file in file_list:
            file_name = lib.get_file_name(file)
            if file_name not in reference_ids:
                self.isFailed = True
                self.failedFile.write("Document %s has invalid ref id\r\n" % (file))
        return
    
    def start(self):
       self.processing_file_pointer = open(self.processing_file_name,"w+")
       self.failed_file_pointer = open(self.failed_file_name,"w+")
       

    def end(self):
        self.processing_file_pointer.close()
        self.failed_file_pointer.close()
        if (self.isFailed):
            lib.remove_file(processing_file_name)
        else:
            lib.remove_file(processing_file_name)
            lib.remove_file(failed_file_name)
            success_file_pointer = open(self.success_file_name,"w+")
            success_file_pointer.close()

        

docs_unzip = DocsInitialVerification('data/source_dump.xlsx', 'data/documents')
docs_unzip.initial_doc_verification()
