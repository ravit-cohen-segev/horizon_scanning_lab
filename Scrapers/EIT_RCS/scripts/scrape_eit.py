# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 08:51:36 2022

@author: Ravit
"""

# In[0]
from bs4 import BeautifulSoup
import pandas as pd
import ssl
import re
import sys


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
# In[1]
#For ignoring SSL ceritficate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# In[2]
class infine_scroll(object): 
  def __init__(self, last):
    self.last = last

  def __call__(self, driver):
    new = driver.execute_script('return document.body.scrollHeight')  
    if new > self.last:
        return new
    else:
        return False
# In[3]
def get_html_from_url(url):
  chrome_options = Options()
  chrome_options.add_argument("--headless")
  chrome_options.add_argument("start-maximized")
  browser = webdriver.Chrome('C:\Program Files\chromedriver_win32 (1)\chromedriver', service=Service(ChromeDriverManager().install()), options=chrome_options) 
  browser.set_page_load_timeout(30) 
  browser.get(url)
   
  last_height = browser.execute_script('return document.body.scrollHeight')

  flag=1

  while flag==1:
    
    try:
       browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
       wait = WebDriverWait(browser, 10)

       new_height = wait.until(infine_scroll(last_height))
       last_height = new_height

    except:
        flag = 0
  html = browser.page_source
  return html

# In[4]
def extract_summary_links_titles_from_page(url):
    html_page = get_html_from_url(url)
    soup = BeautifulSoup(html_page, features="lxml")
    article_boxes =  soup.find_all('li', {'class':'box'})
    summary_links = ['https://eit.europa.eu/' + box.find('a')['href'] for box in article_boxes]
    titles = [box.find('a').text for box in article_boxes]

    #clean titles
    '''
    for i, title in enumerate(titles):
        title = title.replace('\n\n\n\n\n\n\n\n\n\n\n\n\n\n        News\n    \n\n\n', '')
        title = title.replace('\n', '')
        title = title.replace('  ', '')
        regex = re.compile('[^a-zA-Z]')
        title = regex.sub(' ', title)
        titles[i] = title'''
    return summary_links, titles

# In[5]

def extract_summaries_and_more_links(all_links):
    all_first_texts = []

    additional_links = []
    
    for i, link in enumerate(all_links):
        html_link = get_html_from_url(link)
        soup = BeautifulSoup(html_link, features="lxml")
        body_field = soup.find('div', {'class':'body field'})
        try:
            all_other_links = body_field.find('h2').find_all('a')
            all_other_links = [link['href'] for link in all_other_links]
        except:
            all_other_links = []
        additional_links.append(all_other_links)
        
        
        #get summary from first link
        try:
            first_all_ps = body_field.find_all('p')
            first_text = " ".join([p.text for p in first_all_ps])
        except:
            first_text = 'UNKNOWN'
        
        all_first_texts.append(first_text)   

        '''
        regex = re.compile('^[\.a-zA-Z0-9,!? ]*$')
        text = regex.sub(' ', text)
        text = text.replace('\n', '')
        text = text.replace('  ', '')
        text = re.sub(r'[^\x00-\x7F]+',' ', text)
        all_texts.append(text)'''
    return all_first_texts, additional_links


# In[4]
#example
url_start = "https://eit.europa.eu/news-events/news?page="
n_pages = 59

urls = [url_start + str(i) for i in range(1,n_pages+1)]

# In[5]

df_out = pd.DataFrame([], columns = ['links', 'titles', 'summary', 'more_links'])

start = int(sys.argv[1])
end = int(sys.argv[2])



csv_num = sys.argv[3]

for url in urls[start:end]:
    summary_links, titles = extract_summary_links_titles_from_page(url)
    all_summaries, more_links = extract_summaries_and_more_links(summary_links)
    
    temp_df = pd.DataFrame(zip(summary_links, titles, all_summaries, more_links), columns=['links', 'titles', 'summary', 'more_links'])
    df_out = pd.concat([df_out, temp_df], axis=0)


# In[7]
#save to file
df_out.to_csv(r"C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\Scrapers\EIT_RCS\scrapped_articles\eit_stories" + str(csv_num) + ".csv")



