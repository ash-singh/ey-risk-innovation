import glob
from ca_automation import lib


class DocsInitialVerification:
    source_dump_file_name = ''
    source_data = {}
    document_directory = ''
    processing_file_pointer = ''
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

    def process(self):
        self.start()
        self.initial_doc_verification()
        self.end()

    def initial_doc_verification(self):
        failed_doc_ref_id = []
        doc_list = glob.glob(self.document_directory + '/*.pdf')
        reference_ids = self.source_data.keys()

        if len(doc_list) != len(reference_ids):
            self.isFailed = True
            failed_file_pointer = open(self.failed_file_name, "w+")
            failed_file_pointer.write('Records count dont match\n')
            failed_file_pointer.close()
            return

        for doc in doc_list:
            doc_reference_id = lib.get_reference_id_from_file_name(doc)
            if doc_reference_id not in reference_ids:
                self.isFailed = True
                failed_doc_ref_id.append(doc_reference_id)
            
        if self.isFailed:
            failed_file_pointer = open(self.failed_file_name, "w+")
            failed_file_pointer.write("Following Documents has invalid ref \n")
            for invalid_ref_id in failed_doc_ref_id:
                failed_file_pointer.write(" %s \r\n" % invalid_ref_id)
            failed_file_pointer.close()

    def start(self):
        self.processing_file_pointer = open(self.processing_file_name, "w+")
        lib.remove_file(self.failed_file_name)
        lib.remove_file(self.success_file_name)
       
    def end(self):
        self.processing_file_pointer.close()
        lib.remove_file(self.processing_file_name)

        if self.isFailed is False:
            success_file_pointer = open(self.success_file_name, "w+")
            success_file_pointer.close()


docs_unzip = DocsInitialVerification('data/source_dump.xlsx', 'data/documents')
docs_unzip.process()
