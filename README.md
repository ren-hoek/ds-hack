# ds-hack

![Process](https://github.com/ren-hoek/ds-hack/blob/master/Process.png)

# End goal

Take a variety of document types, process into text and surface a front end with a search facility, classification report and geomapping.

# Pipeline

Pipeline was as follows:

1. Convert Inputs to text <br/>
1a. Image to text - Convert image to text (handwritten and printed text) via Azure Computer Vision OCR API <br/>
1b. XHTML to text - Extract text from XHTML using Beautiful Soup <br/>
1c. PDF to text - Use Pytesseract to convert PDF to text <br/>
2. Text to Database - send text to CosmosDB using pymongo Azures sdk
3. Enhance Database - Entity recogniton, NLP preprocessing (e.g. lemmatization, stopwords) and geocoding.
4. Modelling - Peform TFIDF and Word2Vec and produce clusters and document similarity
5. Surfacing - Front end in Flask, hosted on Azure. Can search and return modelling results.
 




