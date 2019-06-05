import zipfile

class DocsUnzip:
    zip_file_name = ''
    document_directory = ''

    def __init__(self, zip_file_name, document_directory):
        self.zip_file_name = zip_file_name
        self.document_directory = document_directory

    def extract_docs(self):
        zip_ref = zipfile.ZipFile(self.zip_file_name, 'r')
        result = zip_ref.extractall(self.document_directory)
        zip_ref.close()
        return

docs_unzip = DocsUnzip('data/documents.zip', 'data/documents')
docs_unzip.extract_docs()
