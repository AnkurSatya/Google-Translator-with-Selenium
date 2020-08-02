from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
import nltk
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from nltk.tokenize import sent_tokenize, word_tokenize
from tqdm import tqdm
import pickle


max_allowed_length=4900
batch_size = 50
driver = None

def setup():
    # chrome_path = '/Users/sukhmansingh/Downloads/chromedriver'
    # driver = webdriver.Chrome(chrome_path)
    global driver
    driver = webdriver.Firefox()

    # Maximize the browser window
    driver.maximize_window()

    #navigate to google translate page 
    driver.get("https://translate.google.co.in/")

#select languages yourself

def translate(data_list):
    try:
        text_field = driver.find_element_by_xpath("""//*[@id="source"]""")
        text_field.send_keys(data_list)
        time.sleep(3)

        sinhala_trans = driver.find_elements_by_xpath("""//*[@class="result-shield-container tlid-copy-target"]""")
        data = sinhala_trans[0].text
        
        text_field.clear()          
        return True, data
    except Exception as e:
        print("Exception in translate(): ",e)
        return False, ""

def paragraph_to_sentences(para):
    return sent_tokenize(para)


def bulk_translate(df, data_save_file, failures_save_file):

    input("Select source and target languages. Then, press Enter:")

    original_index_column_present = "original_index" in list(df.columns)

    complete_translated_list=[]
    failures = []

    start_idx = list(df.index)[0]
    print("start idx: ", start_idx)

    for k,val in tqdm(df.iterrows(), total = df.shape[0]):
        try:
            if original_index_column_present:
                row_translated_list = [int(val["original_index"])]
            else:
                row_translated_list=[k]
            for col in val[0:3]:
                col_translated_list = []
                sentences = paragraph_to_sentences(col)
                i = 0
                while(i < len(sentences)):
                    total_len = len(sentences[i])
                    sent_to_be_translated = sentences[i] 
                    for j in range(i+1, len(sentences)):
                        total_len += len(sentences[j])

                        if total_len >= max_allowed_length:
                            break
                        else:
                            sent_to_be_translated += " "
                            sent_to_be_translated += sentences[j]

                    status, translated = translate(sent_to_be_translated)
                    if not status and k != start_idx + len(df)-1:
                        raise Exception("Exception raised in bulk translate due to translate()")
                    
                    col_translated_list.append(translated)

                    if i == len(sentences)-1:
                        i += 1
                    else:
                        i = j

                row_translated_list.append(' '.join(col_translated_list))

            complete_translated_list.append(row_translated_list)


            if (k != 0 and k%batch_size == 0) or k == start_idx + len(df)-1:
                new_df = pd.DataFrame(complete_translated_list,
                                    columns=['original_index', 'context_translated','question_translated','text_translated'])
                
                with open(data_save_file, 'wb') as f:
                    pickle.dump(new_df, f)
                    
        except Exception as e:
            print(e)
            if original_index_column_present:
                failures.append(int(val["original_index"]))
            else:
                failures.append(k)
    
    with open(failures_save_file,'w') as f:
        f.write('\n'.join([str(i) for i in failures]))
    
