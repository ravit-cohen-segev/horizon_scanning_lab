# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 12:10:40 2023

@author: Ravit
"""

import pandas as pd
from PyPDF2 import PdfReader
import os
import json
# In[]
folder = r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\feature_scripts\output_pdfs'
files = os.listdir(folder)
# In[]
# creating a pdf reader object
def read_pdf_to_txt(path):
    reader = PdfReader(path)
    
    i = 0 
    cont_flag = True
    
    parts = []
    while cont_flag:
    
        try:
            page = reader.pages[i]
        except:
            cont_flag=False
            break
    
        def visitor_body(text, cm, tm, fontDict, fontSize):
            y = tm[5]
            if y > 50 and y < 720:
                parts.append(text)
    
    
        page.extract_text(visitor_text=visitor_body)
        
        i +=1
        
    text_body = "".join(parts)
    
    return text_body

# In[]
d = {}

for file in files:
    path = os.path.join(folder, file)
    d[file.strip('.pdf')] = read_pdf_to_txt(path=path)
    
# In[]
f = open(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\feature_scripts\output_pdfs\13Feb23_arxiv_pdf_text.json', 'w')

f.write(json.dumps(d))