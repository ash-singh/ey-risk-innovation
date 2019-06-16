import zipfile
from riskinnovation import settings


class DocsUnzip:
    zip_file_name = ''
    document_directory = ''

    def __init__(self, zip_file_name, document_directory):
        self.zip_file_name = zip_file_name
        self.document_directory = document_directory

    def extract_docs(self):
        zip_ref = zipfile.ZipFile(self.zip_file_name, 'r')
        zip_ref.extractall(self.document_directory)
        zip_ref.close()
        return


bas_path = settings.BASE_DIR + '/data/'
docs_unzip = DocsUnzip(bas_path + 'documents.zip', bas_path + 'documents')
docs_unzip.extract_docs()
