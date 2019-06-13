import zipfile
from xlrd import open_workbook
import glob
import csv
import xlwt
from ca_automation import lib
from riskinnovation import settings
import PyPDF2 
import textract
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.chunk import conlltags2tree, tree2conlltags
from pprint import pprint



#nltk.download('averaged_perceptron_tagger')
#nltk.download('stopwords')
#nltk.download('punkt')
#nltk.download('maxent_treebank_pos_tagger')
#nltk.download('maxent_ne_chunker')
#nltk.download('words')


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

    def start(self):
        return

    def end(self, doc):
        with open(self.meta_data_file, 'a', newline = '') as csvFile:
            csvWriter = csv.writer(csvFile, delimiter = ',')
            csvWriter.writerow([lib.get_file_name(doc)])
    
    def process_document(self, doc):
        #self.start()
        document_data = self.extract_document_data(doc)
        document_reference_id = lib.get_file_name(doc)
        document_source_data = self.source_data[document_reference_id]
        self.verify_document(document_data, document_source_data)
        
    def verify_document(self, document_data, document_source_data):
        pass
        #self.verify_counter_party_name(document_source_data['COUNTERPARTY_FULLNAME'], document_data)
       
    def verify_counter_party_name(self, counter_party_name, document_source_data):
        for word in counter_party_name.split():
                
            if word in document_source_data:
                print(word + ' found')
            else:
                print(word + ' not found')  
            
    def extract_document_data(self, doc):
        text = self.get_raw_document_content(doc)
        text = text.lower()

        entities = self.extract_entities(text)
        
        return []
    
    def extract_entities(self, text):
        text = nltk.word_tokenize(text)
        text = nltk.pos_tag(text)
        processed_text = nltk.ne_chunk(text)
        
        pattern = 'NP: {<DT>?<JJ>*<NN>}'
        cp = nltk.RegexpParser(pattern)
        cs = cp.parse(processed_text)
        #print(cs)
        iob_tagged = tree2conlltags(cs)
        #pprint(iob_tagged)
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
        
        print(nouns)


    def extract_entities_nltk(self, doc):
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
       
       # Print all entity names
        #print entity_names

        # Print unique entity names
        print(set(entity_names))

    def extract_entity_names(self,t):
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

    def part_of_speech_tagging(self, sentences):
        return [nltk.pos_tag(sent) for sent in sentences]

    def tokenization(self, sentences):
        
        tokens = [nltk.word_tokenize(sent) for sent in sentences]
        """
        punctuations = ['(',')',';',':','[',']',',']
       
        stop_words = stopwords.words('english')
       
        keywords = [word for word in tokens if not word in stop_words and not word in punctuations]
        """
        return tokens

    def sentence_segmentation(self, text):
        sentences = nltk.sent_tokenize(text)
        return sentences

    def get_raw_document_content(self, doc):
        pdf_file_obj = open(doc,'rb')
        pdf_reader = PyPDF2.PdfFileReader(pdf_file_obj)
        
        num_pages = pdf_reader.numPages
        count = 0
        text = ""
        
        while count < num_pages:
            pageObj = pdf_reader.getPage(count)
            count +=1
            text += pageObj.extractText()
        
        if text != "":
            text = text
        else:
            text = textract.process(doc, method='tesseract', language='eng')
        
        return text.decode('utf-8')

bas_path = settings.BASE_DIR  + '/data/'
docs_pdf_extration = DocsPdfExtration(bas_path +'source_dump.xlsx', bas_path + 'documents')
docs_pdf_extration.start_processing()
