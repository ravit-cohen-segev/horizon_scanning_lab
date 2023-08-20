# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 14:23:01 2023

@author: Ravit
"""
import os
import pandas as pd
os.chdir(path = r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\sagem\scripts')


from completions_endpoints import *

#model = 'TheBloke/Wizard-Vicuna-30B-Uncensored-fp16'

model = 'tiiuae/falcon-40b-instruct'
def gen_with_LLM(prompts):
    parameters = {"min_new_tokens": 1, "max_new_tokens": 500, "temperature": 0.2, "repetition_penalty": 1.2,
                  "top_p": 0.95, "encoder_repetition_penalty": 1.0, "top_k": 25, "no_repeat_ngram_size": 0,
                  "typical_p": 0.99, "num_beams": 1, "do_sample": False, "return_full_text": False}
    predictor = HuggingFacePredictor(model, 'ml.g5.12xlarge', 4)
    completions = predictor.generate_completions(prompts, parameters)
    return [c[0]['generated_text'] for c in completions]

def create_prompts(tech_list):
    prompts = [f'''Please provide descriptions for the emerging technology "{tech_name}" in YAML format. Additionally, include the names of the predecessor (whether potential or real) and successor technologies for "{tech_name}".\
               For example:\
                   Emerging Technology: Hypersonic weapon\
                       Description: A hypersonic weapon is a weapon capable of travelling at hypersonic speed, defined as between 5 and 25 times the speed of sound or about 1 to 5 miles per second (1.6 to 8.0 km/s).\
                           Potential or Real Predecessor Technology: DART ammunition\
                               Successor Technology: Compact Kinetic Energy Missile\ 
                                   Please use yaml format for your response.'\n'''
                                   for tech_name in tech_list]
    return prompts

# In[]
if __name__=="__main__":
    
  #  df = pd.read_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\SQL_database\docs\Levi_tech_list\output\9Aug2023_Levi_filtered_techs.csv')
  #  prompts = create_prompts(df['Emerging Tech'].to_list())
  #  output = gen_with_LLM(prompts)

# In[]
  
  df = pd.read_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\UN_gaols\docs\17Aug23_UN_targets_questions_3D_bioprinting.csv')
  prompts = df['Questions'].to_list()
  output = gen_with_LLM(prompts)
  
            
# In[]
  df = pd.read_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\UN_gaols\docs\17Aug23_UN_targets_questions_3D_bioprinting.csv') 
  df['answers'] = output
  df.to_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\UN_gaols\docs\17Aug23_UN_targets_questions_3D_bioprinting_with_answers.csv')