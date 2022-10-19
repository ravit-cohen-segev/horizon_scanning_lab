This is a guide to how I scrapped quora. 

1. Use quora_scrape_urls_with_bertopic_sentences.py for retrieving a list of urls.

2. Use scrape_answers_to_tech_ques_utrls_selenium.py with the list of urls retrieved from stage 1., to extract features from posts,

Note to self (Ravit) Initially, I used Parsehub for scrapping all related questions to Emerging Technologies ("https://www.quora.com/topic/Emerging-Technologies?q=technology%20trends" 11.9.2022 up to-date). Downloaded into json file
"ET_RCS_11DEP22_quora_emerging_tech_ques_url_parsehub"

after that I used bertopic for extracting key words and clustering topics with hdbscan. And repeated the whole process again, using key words from bertopic clusters -> This was done to improve the search in Quora with more focused vocab of key words.