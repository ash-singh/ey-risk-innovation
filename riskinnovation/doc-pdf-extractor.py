import zipfile
from xlrd import open_workbook
from xlwt import Workbook
import glob
import csv
import xlwt
from ca_automation import lib
from riskinnovation import settings
import PyPDF2 
import textract
import nltk
import csv
from nltk.tag.stanford import StanfordNERTagger

from nltk.corpus import stopwords
stop = stopwords.words('english')

st = StanfordNERTagger('stanford-ner/english.all.3class.distsim.crf.ser.gz',
                       'stanford-ner/stanford-ner.jar')

from difflib import get_close_matches
import openpyxl as op

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.chunk import conlltags2tree, tree2conlltags
from pprint import pprint
import re


# nltk.download('averaged_perceptron_tagger')
# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('maxent_treebank_pos_tagger')
# nltk.download('maxent_ne_chunker')
# nltk.download('words')

class DocsPdfExtraction:
    source_data = {}
    mapping_data = {}
    document_directory = ''
    processing_file_pointer = ''
    isFailed = False

    def __init__(self, source_filepath, mapping_filepath, document_directory):
        self.document_directory = document_directory
        self.meta_data_file = lib.get_file_path('processed_record')
        self.source_data = lib.get_source_data(source_filepath)
        self.mapping_data = lib.get_mapping_data(mapping_filepath)
        self.document_export_file = lib.get_file_path('document_export')
        self.documents_export_file_handler = ''
        self.processed_file_handler = open(self.meta_data_file, "w", newline='')
        self.document_fields = ['ref_id', 'counter_party_name', 'trade_date', 'settlement_date', 'currency', 'amount']

        self.processing_file_name = 'data/meta-data/processing.txt'
        self.failed_file_name = 'data/meta-data/failed.txt'
        self.success_file_name = 'data/meta-data/success.txt'

        self.test_text_file_path = settings.BASE_DIR + '/data/meta-data/test_text.txt'

    def get_document_list(self):
        doc_list = glob.glob(self.document_directory + '/*.pdf')
        return doc_list

    def start_processing(self):
        self.start()
        doc_list = self.get_document_list()
        self.process_documents(doc_list)
        self.end()

        return
    
    def process_documents(self, dock_list):
        for doc in dock_list:
            self.process_document(doc)

    def start(self):

        lib.remove_file(self.success_file_name)
        lib.remove_file(self.document_export_file)
        lib.remove_file(self.failed_file_name)
        lib.remove_file(self.processing_file_name)

        self.processing_file_pointer = open(self.processing_file_name, "w+")

        with open(self.document_export_file, 'a', newline='') as csvFile:
            csv_writer = csv.writer(csvFile, delimiter=',')
            csv_writer.writerow(self.document_fields)

        return

    def end(self):
        self.processing_file_pointer.close()
        lib.remove_file(self.processing_file_name)

        if self.isFailed is False:
            success_file_pointer = open(self.success_file_name, "w+")
            success_file_pointer.close()

    def mark_document_processed(self, doc):
        with open(self.meta_data_file, 'a', newline='') as csvFile:
            csv_writer = csv.writer(csvFile, delimiter=',')
            csv_writer.writerow([lib.get_reference_id_from_file_name(doc)])
    
    def process_document(self, doc):
        document_data = self.extract_document_data(doc)

        self.write_to_document_export_file(document_data)

        document_source_data = self.get_source_data_for_document(doc)
        self.verify_document(document_data, document_source_data)

        self.mark_document_processed(doc)

    def get_source_data_for_document(self, doc):
        document_reference_id = lib.get_reference_id_from_file_name(doc)
        return self.source_data[document_reference_id]

    def write_to_document_export_file(self, data):
        values = [
            data.get('reference_id', ''),
            data.get('counter_party_name', ''),
            data.get('trade_date', ''),
            data.get('settlement_date', ''),
            data.get('currency', ''),
            data.get('amount', ''),
        ]

        with open(self.document_export_file, 'a', newline='') as csvFile:
            csv_writer = csv.writer(csvFile, delimiter=',')
            csv_writer.writerow(values)

    def verify_document(self, document_data, document_source_data):
        pass
        # self.verify_counter_party_name(
        #   document_source_data['COUNTERPARTY_FULLNAME'],
        #   document_data['counter_party_name']
        #   )

    @classmethod
    def verify_counter_party_name(cls, counter_party_name, document_source_data):
        for word in counter_party_name.split():
                
            if word in document_source_data:
                print(word + ' found')
            else:
                print(word + ' not found')  
            
    def extract_document_data(self, doc):
        # text = self.get_raw_document_content(doc)
        # text = text.lower()
        # with open(self.test_text_file_path, 'w+') as fp:
        #     fp.write(text)

        text = []
        with open(self.test_text_file_path, 'r') as fp:
            text = fp.read()

        reference_id = lib.get_reference_id_from_file_name(doc)

        counter_party_name = self.get_company_name(text)
        trade_date = self.get_trade_date(text)
        settlement_date = self.get_settlement_date(text)
        currency = self.get_currency(text)
        amount = self.get_amount(text)

        document_data = {
            'reference_id': reference_id,
            'counter_party_name': counter_party_name if counter_party_name else '-',
            'trade_date': trade_date if trade_date else '-',
            'settlement_date': settlement_date if settlement_date else '-',
            'currency': currency if currency else '-',
            'amount': amount if amount else '-',
        }
        return document_data

    @staticmethod
    def get_trade_date(text):
        pass

    @staticmethod
    def get_settlement_date(text):
        pass

    @staticmethod
    def get_currency(text):
        pass

    @staticmethod
    def get_amount(text):
        pass

    @staticmethod
    def get_company_name(text):
        organization_names = []
        for sent in nltk.sent_tokenize(text):
            tokens = nltk.tokenize.word_tokenize(sent)
            tags = st.tag(tokens)
            for tag in tags:
                if tag[1] is "ORGANIZATION":
                    organization_names.append(tag[0])

        return " ".join(str(name) for name in organization_names)

    @staticmethod
    def extract_entities(text):
        text = nltk.word_tokenize(text)
        text = nltk.pos_tag(text)
        processed_text = nltk.ne_chunk(text)
        
        pattern = 'NP: {<DT>?<JJ>*<NN>}'
        cp = nltk.RegexpParser(pattern)
        cs = cp.parse(processed_text)
        iob_tagged = tree2conlltags(cs)
        nouns = []
        amount = []
        date = []
        for word, pos, ner in iob_tagged:
            if pos == 'NN':
                nouns.append(word)
            
            if pos == 'CD':
                amount.append(word)

            if pos == 'JJ' and ner == 'O':
                date.append(word)
        
        return nouns

    def extract_entities_nltk(self, text):
        sentences = nltk.sent_tokenize(text)
        #sentences = self.tokenization(sentences)
        #tagged_sentences = self.part_of_speech_tagging(sentences)
        
        tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
        tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
        chunked_sentences = nltk.ne_chunk_sents(tagged_sentences, binary=True)
        
        entity_names = []
        for tree in chunked_sentences:
            print(tree)
            entity_names.extend(self.extract_entity_names(tree))

        # Print unique entity names
        print(set(entity_names))

    def extract_entity_names(self, t):
        entity_names = []

        if hasattr(t, 'label') and t.label:
            if t.label() == 'NE':
                entity_names.append(' '.join([child[0] for child in t]))
            else:
                for child in t:
                    entity_names.extend(self.extract_entity_names(child))

        return entity_names

    def chunking(self, sentences):
        pattern = 'NP: {<DT>?<JJ>*<NN>}'
        cp = nltk.RegexpParser(pattern)
        return [cp.parse(sent) for sent in sentences]

    @staticmethod
    def part_of_speech_tagging(sentences):
        return [nltk.pos_tag(sent) for sent in sentences]

    @staticmethod
    def tokenization(sentences):
        
        tokens = [nltk.word_tokenize(sent) for sent in sentences]
        """
        punctuations = ['(',')',';',':','[',']',',']
       
        stop_words = stopwords.words('english')
       
        keywords = [word for word in tokens if not word in stop_words and not word in punctuations]
        """
        return tokens

    @staticmethod
    def sentence_segmentation(text):
        sentences = nltk.sent_tokenize(text)
        return sentences

    @staticmethod
    def get_raw_document_content(doc):
        pdf_file_obj = open(doc, 'rb')
        pdf_reader = PyPDF2.PdfFileReader(pdf_file_obj)
        
        num_pages = pdf_reader.numPages
        count = 0
        text = ""
        
        while count < num_pages:
            page_obj = pdf_reader.getPage(count)
            count += 1
            text += page_obj.extractText()
        
        if text != "":
            text = text
        else:
            text = textract.process(doc, method='tesseract', language='eng')
        
        return text.decode('utf-8')

    def ie_preprocess(self, document):
        document = ' '.join([i for i in document.split() if i not in stop])
        sentences = nltk.sent_tokenize(document)
        sentences = [nltk.word_tokenize(sent) for sent in sentences]
        sentences = [nltk.pos_tag(sent) for sent in sentences]
        return sentences

    def extract_names(self, document):
        names = []
        sentences = self.ie_preprocess(document)

        for tagged_sentence in sentences:
            for chunk in nltk.ne_chunk(tagged_sentence):
                if type(chunk) == nltk.tree.Tree:
                    print(chunk.label())
                    if chunk.label() == 'ORGANIZATION':
                        names.append(' '.join([c[0] for c in chunk]))
        return names


base_path = settings.BASE_DIR + '/data/'
mapping_file_path = base_path + 'mapping.xlsx'
source_file_path = base_path + 'source_dump.xlsx'
documents_path = base_path + 'documents'

docs_pdf_extraction = DocsPdfExtraction(source_file_path, mapping_file_path, documents_path)
docs_pdf_extraction.start_processing()
