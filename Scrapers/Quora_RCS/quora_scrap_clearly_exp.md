This is a guide to how I scrapped quora. 

1. I used Parsehub for scrapping all related questions to Emerging Technologies ("https://www.quora.com/topic/Emerging-Technologies?q=technology%20trends" 11.9.2022 up to-date). Downloaded into json file
"ET_RCS_11DEP22_quora_emerging_tech_ques_url_parsehub"

2. removed all irrelevant urls manually

2. "scrape_answers_to_tech_ques_utrls" is for parsing answers for related questions in url. Features were extracted like "Upvote", and FollowerCount and saved all in a joined table 
in orizon_scanning_lab/Scrapers/Quora_RCS/answers_and_info/ET_RCS_22SEP15_quora_data.csv

 
