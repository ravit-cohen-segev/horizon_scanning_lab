# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 13:23:32 2023

@author: Ravit
"""
import os

from datetime import datetime

os.chdir(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\lib\feature_engineering')
from myfunctions import *

os.chdir(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\lib\feature_engineering\tests')

from test_myfunctions import *

# In[]
if __name__=="__main__":

    #bertopic file format: dd_mm_yy_all_domains_with_bertopic_ids
    bert_df = pd.read_csv(r"C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\Scrapers\combined_domains\docs\with_reddit_crunch\features\bertopic\9Feb23_all_domains_with_bertopic_ids.csv").set_index(['Unnamed: 0'])
    tag_rep_df = pd.read_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\lib\feature_engineering\tag_representations.csv') 
    
    # In[]
    
    # test df correct parsing
    try:
        check_if_unnamed_in_cols(bert_df)
    except:
        if 'Unnamed' in bert_df.index.name:
            bert_df.index.name = 'id'
    
    try:
        check_if_nan_in_df(bert_df)
    except:
        bert_df.fillna('UNKNOWN', inplace=True)
        
    #check if text columns are indented abstarct and title columns
    try:
        check_all_unindented(bert_df, 'title')
    except:
        bert_df['title'] = remove_tabs_spaces(bert_df['title'].to_list())
    
    try:
        check_all_unindented(bert_df, 'abstract')
    except:
        bert_df['abstract'] = remove_tabs_spaces(bert_df['abstract'].to_list())
    
    #if index doesn't start from 1. Look at the indices manually and fix it
    check_if_row_id_start_from_one(bert_df)
    
    
    # In[]
    # create feature dfs
    pos_df = create_pos_df(bert_df, tag_rep_df)
    onehot_titles_df = create_onehotEncode_titles(bert_df, 'title', tag_rep_df)
    title_tag_feat_df = create_title_tag_features(bert_df, 'title', pos_df)
    subj_df, obj_df = create_noun_dependency_features(bert_df,'title')
    ent_df, ent_dep_df = create_abstract_entity_features(bert_df, 'abstract')
    df_top_phrase = extract_abstract_common_phrases(bert_df, 'abstract') 
    # In[]
    # combine all sentence features into all_features df
    all_title_features = pd.concat([title_tag_feat_df, subj_df, obj_df], axis=1)

    
    
    # In[]
    check_if_indices_match_main_df(bert_df, [pos_df, onehot_titles_df, title_tag_feat_df, subj_df, obj_df, df_top_phrase])
    # In[]
    # file formats
    #dd_mm_yy_all_features
    #dd_mm_yy_one_hot_features
    #dd_mm_yy_sentence_features
    
    #### external scripts
    #dd_mm_yy_all_domains_onehot_after_lpca_50_true_id 
    #dd_mm_yy_sample_levi_scores_with_index_abs_top_phrase
    
    dd = str(datetime.today().day)
    mm = str(datetime.today().month)
    yy = str(datetime.today().year)
    
    all_features_path = dd + '_' + mm + '_' + yy + '_all_features.csv'
    onehot_feat_path = dd + '_' + mm + '_' + yy + '_one_hot_features.csv'
    sentence_feat_path = dd + '_' + mm + '_' + yy + '_sentence_features.csv'