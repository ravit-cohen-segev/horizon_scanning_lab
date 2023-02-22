# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 13:24:15 2023

@author: Ravit
"""
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.data import load

import spacy
import pandas as pd
import numpy as np
import pytextrank
from tqdm import tqdm

# In[] 
def remove_non_ascii(string):
    return ''.join(char for char in string if ord(char) < 128)

def remove_tabs_spaces(elements):
    '''{input: a list of text elments
    output: list of parsed elements }'''
    return [" ".join(remove_non_ascii(el).replace('\n', ' ').replace('\t', '').split()) for el in elements]

def remove_sparse_features(df, threshold=0.01):
    variance = df.var()
    drop_cols = []
    for col in df.columns:
        if variance[col]<threshold:
            drop_cols.append(col)
    return df.drop(drop_cols, axis=1)

def num_stopwords(text):
    stop_words = set(stopwords.words('english'))  
    word_tokens = word_tokenize(text)
    stopwords_x = [w for w in word_tokens if w in stop_words]
    return len(stopwords_x)


#sentence features functions
def create_pos_df(text_df, tag_rep_df):
    '''{ input: df with text, tag df
         output: pos_df}'''

    #get max sentence length

    title_list = text_df['title'].to_list()
    n_max = np.max([len(word_tokenize(title)) for title in title_list] )

    list_length = len(title_list)

    ordinal_matrix = np.zeros((list_length, n_max))


    ordinal_matrix.fill(-1)

    idx_fix = []

    for i, title in enumerate(title_list):
        tokenized = word_tokenize(title)
        tags = nltk.pos_tag(tokenized)

        for j, tag in enumerate(tags):
           
            tag_id = tag_rep_df[tag_rep_df['TAG_NAME']==tag[1]]['TAG_ID']
            try:
                ordinal_matrix[i,j] = tag_id.iloc[0]
            except:
                idx_fix.append(i)
                print("There is an issue with index {} {} word {}".format(i,j, tag[0]))
                # Hashtags with words will be ignored 

    #sentence with -1 before the end will be cut short
    for i in idx_fix:
        vec = ordinal_matrix[i,:]
        vec = [a for a in vec if a!=-1]
        vec = np.array(vec + [-1]*(ordinal_matrix.shape[1]-len(vec)))  
        ordinal_matrix[i,:] = vec

    pos_df = pd.DataFrame(ordinal_matrix)
    pos_df.index = text_df.index
    return pos_df

# onehot create function-> principle matrix
def create_onehotEncode_titles(text_df, title_col, tag_df):
    '''{input: a list of titles
    output: onehot matrix shape:(list length, list of tags length)}'''

    titles = text_df[title_col].to_list()
    tagdict = load('help/tagsets/upenn_tagset.pickle')
    onehot_labels = list(tagdict.keys()) + ['None']
    
    max_len = np.max([len(title.split()) for i, title in enumerate(titles)])
        
    onehot_matrix = np.empty(shape = (0,max_len*len(tag_df)))

    for title in titles:
        onehot_zeros = np.zeros(shape=(max_len, len(onehot_labels)))
        onehot_zeros[:,-1] = 1 
        #forget about hashtags
        word_tags = [tag[1] for tag in nltk.pos_tag(nltk.word_tokenize(title)) if tag[1]!='#']
        for i, tag in enumerate(word_tags):
            j = onehot_labels.index(tag)
            onehot_zeros[i,j] = 1
            onehot_zeros[i,-1] = 0

        onehot_matrix = np.vstack((onehot_matrix, onehot_zeros.flatten()))

    onehot_df = pd.DataFrame(onehot_matrix)
    onehot_df.index = text_df.index
    return onehot_df


def create_title_tag_features(text_df, title_col, pos_df):
    tagdict = load('help/tagsets/upenn_tagset.pickle')
    
    title_list = text_df[title_col].to_list()
    
    count_chars = []
    count_words = []
    count_capital_words = []
    #count_sent = []
    count_unique_words = []
    count_stopwords = []

    for title in title_list:
        count_chars.append(len(title))
        count_words.append(len(title.split()))
        count_capital_words.append(sum(map(str.isupper,title.split())))
     #   count_sent.append(len(nltk.sent_tokenize(title)))
        count_unique_words.append(len(set(title.split())))
        count_stopwords.append(num_stopwords(title))

        text_df_  = pd.DataFrame([], columns=['text_length', 'word_count', 'capital_words_count', 'count_unique_words', 'count_stopwords'])
        text_df_['text_length'] = count_chars
        text_df_['word_count'] = count_words
        text_df_['capital_words_count'] = count_capital_words
      #  text_df_['count_sentences'] = count_sent
        text_df_['count_unique_words'] = count_unique_words
        text_df_['count_stopwords'] = count_stopwords
    
    
    all_tags = list(tagdict)

    all_verb_tags = [(i,w) for i, w in enumerate(all_tags) if 'VB' in w]
    verb_index = [w[0] for w in all_verb_tags]

    all_noun_tags =  [(i,w) for i, w in enumerate(all_tags) if 'NN' in w]
    noun_index = [w[0] for w in all_noun_tags]

    #gerund (ing)
    verb_vbg = 6

    #VBZ and VBP
    verb_present = [8, 10]

    #create features with combination of words. use sequence of tag indices 
    #1. problem description

    #Ex: need to do ...
    vbp_to_vb = [10,1,36]
    #EX: is required ... 
    vbz_vbn = [8, 2]

    #2. solution
    #EX: may help...

    md_vb = [35,36]

    #EX: for solving ...
    #in_nn = [29,11]

    #EX: for better ...
    #in_jjr = [29,32]

    #3. discoveries/news/innovations
    # EX: researcher/s developed a ...
    nn_vbd = [11,28]
    nns_vbd = [40,28]

    # Ex: study demonstrates a...
    nn_vbz = [11,8]
    nns_vbp = [40,10]
    
    all_noun_count = []
    all_verb_count = []
    all_verb_present = []
    all_vbg = []
    all_word_num = []

    for i, row in pos_df.iterrows():
        row_value_counts = row.value_counts() 
        word_idx = row_value_counts.index
        if -1 in word_idx:
            word_idx = word_idx.drop(-1)
        word_num = np.sum([row_value_counts[j] for j in word_idx])
        all_word_num.append(word_num)
            
        noun_counts = np.sum([row_value_counts[j] for j in noun_index if j in row_value_counts])
        all_noun_count.append(noun_counts)
        
        verb_counts =  np.sum([row_value_counts[j] for j in verb_index if j in row_value_counts]) 
        all_verb_count.append(verb_counts)
        
        v_present  = np.sum([row_value_counts[j] for j in verb_present if j in row_value_counts])
        all_verb_present.append(v_present)
        
        if verb_vbg in row_value_counts.index:
            count_vbg = row_value_counts[verb_vbg]
            all_vbg.append(count_vbg)
        else:
            all_vbg.append(0)

    #add features to array
    df = pd.DataFrame([])


    df['noun_count'] = np.array(all_noun_count) / np.array(all_word_num)
    df['verb_count'] = np.array(all_verb_count) / np.array(all_word_num)
    df['verb_present'] = np.array(all_verb_present) / np.array(all_word_num)


    df['vbg'] = np.array(all_vbg) / np.array(all_word_num)

    eps = 10**(-8)

    df['vbg/total_verbs'] = df['vbg'] / (df['verb_count'] + eps)
    df['verb_present/total_verbs'] = df['verb_present'] / (df['verb_count'] + eps)

    def is_tag_sequence_in_senetence(l1, l2):
        str1 = "".join([str(l) for l in l1])
        str2 = "".join([str(l) for l in l2])
        if str1 in str2:
            return 1
        return 0

    #problem features
    all_vbp_to_vb = [] 
    all_vbz_vbn = []


    #solution
    all_md_vb = []


    #discoveries
    all_nn_vbd = []
    all_nns_vbd = []

    all_nn_vbz = []
    all_nns_vbp = []

    for i, row in pos_df.iterrows():
        row_list = row.astype(int).tolist()
            
        all_vbp_to_vb.append(is_tag_sequence_in_senetence(vbp_to_vb, row_list))
        all_vbz_vbn.append(is_tag_sequence_in_senetence(vbz_vbn, row_list))
        all_md_vb.append(is_tag_sequence_in_senetence(md_vb, row_list))
        all_nn_vbd.append(is_tag_sequence_in_senetence(nn_vbd, row_list))
        all_nns_vbd.append(is_tag_sequence_in_senetence(nns_vbd, row_list))
        all_nn_vbz.append(is_tag_sequence_in_senetence(nn_vbz, row_list))
        all_nns_vbp.append(is_tag_sequence_in_senetence(nns_vbp, row_list))
        
    df['vbp_to_vb'] = all_vbp_to_vb
    df['vbz_vbn'] = all_vbz_vbn
    df['md_vb'] = all_md_vb
    df['nn_vbd'] = all_nn_vbd
    df['nns_vbd'] = all_nns_vbd
    df['nn_vbz'] = all_nn_vbz
    df['nns_vbp'] = all_nns_vbp

    all_fors = []
    for title in title_list:
        if 'for' in title:
            all_fors.append(1)
        else:
            all_fors.append(0)

    df['for'] = all_fors

    # add features with root verbs and their index in a sentence, and if a root verb exists

    nlp = spacy.load("en_core_web_sm")
    root_verbs = []
    root_verbs_exists = [0]*len(df)

    for i, title in enumerate(title_list):
        doc = nlp(title)
        root = [i+1 for i,token in enumerate(doc) if (token.pos_ == 'VERB') and (token.dep_ == 'ROOT')]
        
        if root!= []:
            root_verbs_exists[i] = 1
            root_verbs.append(root[0])
        else:
            root_verbs.append(0)
            
            
    df['root_verb_index'] = root_verbs
    df['root_verb_exists'] = root_verbs_exists
    df.index = text_df.index
    return df


def create_noun_dependency_features(text_df, text_col):
    '''{ input: df and specific text column
         output: two dfs with subject and object dependency features}'''
    texts = text_df[text_col].to_list()
    nlp = spacy.load("en_core_web_sm")
    
    SUBJECTS = ["nsubj", "nsubjpass", "csubj", "csubjpass", "agent", "expl"]

    OBJECTS = ["pobj", "dobj", "dative", "attr", "oprd"]
    
    subjects_features = np.zeros((len(texts),len(SUBJECTS)))
    objects_features = np.zeros((len(texts),len(OBJECTS)))
    
    for i, text in enumerate(texts):
        doc = nlp(text)
        
        for chunk in doc.noun_chunks:
            if  chunk.root.dep_ in SUBJECTS:
                subjects_features[i, SUBJECTS.index( chunk.root.dep_)] += 1
                
                
            if  chunk.root.dep_ in OBJECTS:
                objects_features[i, OBJECTS.index( chunk.root.dep_)] += 1
    
    subj_df = pd.DataFrame(subjects_features, columns=SUBJECTS)
    subj_df.index = text_df.index
    obj_df =pd.DataFrame(objects_features, columns = OBJECTS)
    obj_df.index = text_df.index
    return subj_df, obj_df



def filter_sentence(sent):
    '''{ input: a sentence
        output: word, entity, depencendy, and original word features}'''
    stop_words = set(stopwords.words('english'))
    nlp = spacy.load('en_core_web_lg')
    
    BAD_DEP=["poss","det"]
    ALLOWED_ENT = ["ORG", "PRODUCT", "EVENT", "WORK_OF_ART", "LAW", "CARDINAL"]
    doc = nlp(sent)
    filtered_sentence=[]
    
    for noun_chunk in doc.noun_chunks:
        original_chunk=noun_chunk
        if noun_chunk[0].dep_ in BAD_DEP:
            noun_chunk=noun_chunk[1:]
        
        w=noun_chunk.text.lower()
        ent=noun_chunk.root.ent_type_
        if ent not in ALLOWED_ENT:
            continue
        w=noun_chunk.text.lower()
#         if w not in stop_words:
        # if check(w):
        #     print(w)
        
        filtered_sentence.append({"word":w,
                                      "entity":noun_chunk.root.ent_type_,
                                      "dependency":noun_chunk.root.dep_,
                                     "original_word":original_chunk.text})
            

    return filtered_sentence

def create_abstract_entity_features(text_df, abstract_col):
    
    
    '''{input: text_df, abstract name column
      output: df with entity features }'''
    words_abs = []
    cols = ["word", "entity", "dependency","original_word"]
    df_abs = pd.DataFrame(np.empty((0, 4)), columns = cols) 
    abstract_index = []
    
    for index, row in tqdm(text_df.iterrows()):
        abstract = row[abstract_col]
        filtered = filter_sentence(abstract)

        if filtered == []:
      #     missing_cols = cols
       #     df_abs = pd.concat([df_abs, pd.DataFrame(['UNKNOWN']*len(cols)).T]) 
        #    abstract_index.extend([index]*len(pd.DataFrame(['UNKNOWN']*len(cols)).T))
            continue
        else:
            item_df = pd.DataFrame(filtered)
            
            missing_cols = list(set(cols) - set(item_df.columns))
            for col in missing_cols:
                filtered[col] = ['UNKNOWN']*len(item_df)
            
        item_df = pd.DataFrame(filtered)
        abstract_index.extend([index]*len(item_df))
        '''
        item_df = item_df[cols]'''
 
        df_abs = pd.concat([df_abs, item_df], axis=0) 
    df_abs.index = abstract_index
    return df_abs

def extract_abstract_common_phrases(text_df, text_col):
    texts = text_df[text_col].to_list()
    nlp = spacy.load("en_core_web_sm")
    nlp.add_pipe("textrank")
    dfs_main_phrase = pd.DataFrame([], columns=['text', 'rank', 'count'])
    
    for text in texts:
        doc = nlp(text.lower())
        # examine the top-ranked phrases in the document
        phrase = doc._.phrases[0]
        dfs_main_phrase = pd.concat([dfs_main_phrase, pd.DataFrame([[phrase.text, phrase.rank, phrase.count]], columns = dfs_main_phrase.columns)]) 
    dfs_main_phrase.index = text_df.index
    return dfs_main_phrase
    

    
