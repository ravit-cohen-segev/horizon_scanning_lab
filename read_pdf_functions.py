# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 15:56:42 2023

@author: Ravit
"""

from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

import spacy
from PyPDF2 import PdfReader


import re


# In[]
# load a spaCy model, depending on language, scale, etc.
nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("textrank", )

stop_words =  stopwords.words("english")
lemmatizer = WordNetLemmatizer()




# In[]
def pdf_into_chunks(file_path):
    reader = PdfReader(file_path)
    
    
    i = 0 

    cont_flag = True

    texts = []

    while cont_flag:
        try:
            page = reader.pages[i]
        except:
            cont_flag=False
            break
        texts.append(re.sub(r'\s+', ' ', page.extract_text()))
        i+=1
    return texts
# In[]
if __name__=="__main__":

    texts = pdf_into_chunks(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\agriculture_data\docs\out_pdfs\s10152-014-0406-3.pdf')