# ds-hack

#End goal
Classify a range of text documents into types (accounts, reports etc.) 

#Pipeline
Seperate branch for each pipeline element as follows:

1. Prepare - Convert PDF to JPG and JPG to text (both handwritten and printed text) via Azure Computer Vision OCR API
2. Extraction - Extract text from HTML.
3. Process - Entity extraction, stopword removal, lemmatization etc. 
4. Modeling (Unsupervised) - Cluster on TFIDF, Word2Vec, Doc2Vec. Fitted with both a local model and famous pre-trained models such as Glove
5. Modeling (Supervised)- Create features using regular expressions and feed into Logisitc regression, SVM etc.




