# FX Document Infomation Exctrator and Verifier (FX-DIEV)

Web application (django pyhon) to exracted the structed data from unstructed data (pdf documents) and verify it as per the system data.
As soon as all the relevant documents are uploaded a background process will execute python scripts to perform preliminary verification of FX document.


# How it works!
  - Upload the system dump, data mapping file and FX documents zip
  - As soon as all the relevant documents are uploaded a background process will execute python scripts to perform preliminary verification of FX document.
     - unzip FX documents zip to /documents folder
     - total number of document updated are equal to total transaction in system.
     - each FX document’s reference number matched with system dump
  - User is redirected to dashboard where he/she can see the result of preliminary verification. Once user clicks on process document button complete FX document verification process starts.
  - A single document is picked from uploaded FX document (/documents folder) and  Following steps are perform by python scripts automatically for information extraction.
    - extract raw text from pdf file.
    - using python’s nltk module process raw text.
        - Sentence segmentation 
        - Tokenization
        - Part of speech tagging
        - Entity detection using Non phrase (NP) chunking, Tag patterns and Regular Expressions
        - Relations detection
    - save the exacted data to an excel sheet (extracted_data.xlsx) with reference id as primary attribute.
            *we can should save this to database (easy retrieval, scalable) but for prototype we will save to an excel sheet.  
- When python scripts has processed all the document then data verification script loads the system dump file (system_dump.xlsx) and extracted data file (extracted_data.xlsx)  and starts comparing each FX document entry  of extracted data file with the corresponding entry in system source dump. 
If entry in extracted data file and source dump file match then mark this entry as verified ( add entry to verified document excel sheet) else add to exception excel sheet.
Report Page. Vist report page on Django web app.  Report page will display the result of the Fx document verification. User can download the various excel sheets. 
    - Extracted data sheet
    - Verified document sheet
    - Exception document sheet




### Tech

FX-DIEV uses a number of open source projects to work properly:

* [Django] - Python web application framework!
* [NLTK] - python natural language tool kit package for natual language processing


### Installation

Dillinger requires python 3 to run.

Install the dependencies and devDependencies and start the server.

```sh
$ git clone https://github.com/AshSingh4888/ey-risk-innovation.git ey-risk-innovation
$ cd ey-risk-innovation
$ python riskinnovation/manage.py runserver
open browser at http://127.0.0.1:8000
```

### Todos

 - Use database instead of excel sheet
 - Add test cases
 - impove the accuracy of information extrated from FX documents

License
----

MIT


**Free Software, Hell Yeah!**

