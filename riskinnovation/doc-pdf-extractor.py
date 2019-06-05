import zipfile
from xlrd import open_workbook
import glob
import re
import csv
import xlwt

class DocsPdfExtration:
    sourceFileName = ''
    sourceData = {}
    documentsDirector = ''

    def __init__(self, sourceFileName, documentDirectory):
        self.sourceFileName = sourceFileName
        self.documentDirectory = documentDirectory
        self.metaDataFile = 'meta-data/processed-record.csv'

    def getDocumentList(self):
        docList = glob.glob(self.documentDirectory + '/*.pdf')
        return docList

    def getSourceData(self):
        wb = open_workbook(self.sourceFileName)
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
                       
                self.sourceData[reference_id] = values
        return self.sourceData

    @staticmethod 
    def getFileName(file):
        try:
            filename = re.search('/(.+?).pdf', file).group(1)
        except AttributeError:
            filename = '' 
        return filename   


    def startProcessing(self):
        self.getSourceData()
       
        dockList = self.getDocumentList()
        self.processDocuments(dockList)
        return
    
    def processDocuments(self, docList):
        for doc in docList:
            self.processDocument(doc)

    def processDocument(self, doc):
        self.start()

        self.end(doc)
    
    def start(self):
        return

    def end(self, doc):
        with open(self.metaDataFile, 'a', newline = '') as csvFile:
            csvWriter = csv.writer(csvFile, delimiter = ',')
            csvWriter.writerow([self.getFileName(doc)])


docsPdfExtration = DocsPdfExtration('System Dump.xlsx', 'documents')
docsPdfExtration.startProcessing()
