# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 16:18:59 2023

@author: Ravit
"""

import pandas as pd


# In[]
df = pd.read_excel(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\tech_list\docs\Levi_files\20231023 New Master October 2023.xlsx')

claude_1 = pd.read_excel(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\tech_list\docs\results\20Oct2023_techs_emerging_or_not.xlsx', header=0, sheet_name= 'Tech List 1') 
claude_2 = pd.read_excel(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\tech_list\docs\results\20Oct2023_techs_emerging_or_not.xlsx', header=0, sheet_name= 'Tech List 2') 
claude_3 = pd.read_excel(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\tech_list\docs\results\20Oct2023_techs_emerging_or_not.xlsx', header=0, sheet_name= 'Tech List 3') 

cols = df.columns
# In[]

claude_1.columns = ['Tech Level 1', 'Status Tech Level 1', 'Explanation Tech Level 1']
claude_2.columns = ['Tech Level 2', 'Status Tech Level 2', 'Explanation Tech Level 2']
claude_3.columns = ['Tech Level 3', 'Status Tech Level 3', 'Explanation Tech Level 3']

# In[]

new_df = df.merge(claude_1, on='Tech Level 1')
new_df = new_df.merge(claude_2, on='Tech Level 2')
new_df = new_df.merge(claude_3, on='Tech Level 3')

# In[]
new_df = new_df[['Concept_1', 'Concept_2', 'Tech Level 1', 'Status Tech Level 1', 'Explanation Tech Level 1', 'Tech Level 2', 'Status Tech Level 2', 'Explanation Tech Level 2', 'Derivative Claude', 'Tech Level 3', 'Status Tech Level 3', 'Explanation Tech Level 3', 'Concept synonym', 'Origin Source', 'synonym_1', 'synonym_2', 'synonym_3', 'Description', 'Web of Science category', 'OECD Research Area', 'Derivative Tech', 'LLM']]
new_df.to_excel(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\tech_list\docs\results\25Oct2023_levi_file_merged_with_claude.xlsx')