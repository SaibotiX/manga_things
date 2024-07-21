import deepl
from pathlib import Path
import os
import time
from voicevox import Client
import asyncio
from playsound import playsound
import json
import keyboard

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

running = True

async def wav(var):
    async with Client() as client:
        audio_query = await client.create_audio_query(var, speaker=1)
        with open("../tools/voice.wav", "wb") as f:
            f.write(await audio_query.synthesis(speaker=1))

        playsound('../tools/voice.wav')

def read_json_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

# Function to write data to a JSON file
def write_json_file(data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

# Function to check if new data set already exists based on "Kana" and "Kana_Kanji" value pairs
def is_data_already_saved(data, new_kana, new_kana_kanji):
    for data_instance in data:
        if data_instance.get("Kana") == new_kana and data_instance.get("Kana_Kanji") == new_kana_kanji:
            return True
    return False

def verify_data(data):
    for data_instance in data:
        if data_instance.get("Verify") == "N":
            print("Verify: ")
            print(json.dumps(data_instance, indent=4))

            user_input = input("(C)orrect or (D)elete: ")

            if user_input.upper() == "C":
                data_instance["Verify"] = "Y"
            else:
                data.remove(data_instance)
                
    return data

def on_hotkey(driver):
    global running
    running = False

    driver.quit()

path = '../tools/sentences.txt'

auth_key = "c1c893eb-38dd-4296-9a0e-1e9993662069:fx"
            
translator = deepl.Translator(auth_key)

open(path, 'w').close()

time_c = os.path.getctime(path)

mod_file = time.ctime(time_c)
mod_time = time.ctime(time_c)

vocabulary = ""

options = Options()

#options.add_argument("-headless")
service = Service(executable_path="/snap/bin/geckodriver")
profile = FirefoxProfile()

#  profile.set_preference("javascript.enabled", False)

options.profile = "/home/zuckram/snap/firefox/common/.cache/mozilla/firefox/mrkq3e7p.test"

driver = webdriver.Firefox(options=options, service=service)
#driver.set_window_size(1920, 1080)
driver.maximize_window()
driver.implicitly_wait(10)

driver.get("https://jisho.org")

keyboard.add_hotkey('ctrl+shift+a', lambda: on_hotkey(driver))

voc_count = 0
print("RDY")

while running:
    if mod_time != mod_file:
        time.sleep(0.2)
        if os.path.getsize(path) > 0:
            with open(path, 'r') as line:
                vocabulary = line.readlines()[-1]
                
        asyncio.run(wav(vocabulary))

        result = translator.translate_text(vocabulary, target_lang="EN-US")

        print(vocabulary.strip() + "  -  " + result.text, end="\n")
        open(path, 'w').close()        
        time_c = os.path.getctime(path)
        mod_file = time.ctime(time_c)
        mod_time = mod_file

        scrape_keyword = driver.find_element(By.NAME, "keyword")
        scrape_keyword.send_keys(vocabulary)

        mag_glass = driver.find_element(By.CLASS_NAME, "submit")
        mag_glass.click()

        time.sleep(0.5)
        iterate_vocab = driver.find_elements(By.CLASS_NAME, "japanese_word__text_wrapper")

        count = 0

        main_dict = {
            "Kana" : None,
            "Kanji" : None,
            "English" : {},
            "Other Meanings" : {}
        }
        
        Curr_Vocab = {
            "Kana": None,
            "Kana_Kanji": None,
            "English": {
            }
        }

        

        for voc in iterate_vocab:

            voc.click()

            time.sleep(0.5)

            try:
                driver.implicitly_wait(0)
                no_matches = WebDriverWait(driver, 0.1).until(
                    EC.presence_of_element_located((By.ID, "no-matches"))
                    )
                driver.implicitly_wait(10)
                continue
            except TimeoutException:
                pass

            linkable = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, "//li[@class='clearfix japanese_word']")))
            
            large_eight = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "large-8")))

            concept_light = large_eight.find_elements(By.CLASS_NAME, "concept_light")
            concept_light = concept_light[:3]
            count = 0

            main_fur = concept_light[0].find_elements(By.CLASS_NAME, "furigana")
            main_text = concept_light[0].find_elements(By.CLASS_NAME, "text")
            main_meaning_meaning = concept_light[0].find_elements(By.CLASS_NAME, "meaning-meaning")
            main_meaning_tags = concept_light[0].find_elements(By.CLASS_NAME, "meaning-tags")

            main_dict["Kana"] = main_fur[0].text
            main_dict["Kanji"] = main_text[0].text

            
            for element in concept_light:
                Curr_Vocab = {
                    "Kana": None,
                    "Kana_Kanji": None,
                    "English": {
                    }
                }

                furigana = element.find_elements(By.CLASS_NAME, "furigana")
                text = element.find_elements(By.CLASS_NAME, "text")
                
                meaning_meaning = element.find_elements(By.CLASS_NAME, "meaning-meaning")
                meaning_tags = element.find_elements(By.CLASS_NAME, "meaning-tags")

                meaning_meaning = meaning_meaning[:3]
                meaning_tags = meaning_tags[:3]
                
                if os.path.getsize("/home/zuckram/Desktop/Japanese/src/manga.json") != 0:
                    with open('manga.json', 'r') as file:
                        data = json.load(file)

                for fur, tex in zip(furigana, text):
                    Curr_Vocab["Kana"] = fur.text
                    Curr_Vocab["Kana_Kanji"] = tex.text

                    Curr_Vocab["English"].clear
                    count = 0
                    for meaning_m, meaning_t in zip(meaning_meaning, meaning_tags):
                        meaning_t_text = meaning_t.text
                        meaning_m_text = meaning_m.text

                        Vocab_Iteration = f"Vocab{count}"
                        Curr_Vocab["English"][Vocab_Iteration] = {}

                        Curr_Vocab["English"][Vocab_Iteration]["Value"] = meaning_t_text
                        Curr_Vocab["English"][Vocab_Iteration]["Vocab"] = meaning_m_text

                        count = count + 1

                    json_data = read_json_file("manga.json")

                    #Redo the json shit because even if a word has multiple meanings you store the first vocab lsited in jisho as a master vocab and then order the next vocabs under that and when then rehirse the vocabs you ask the main vocab and then show the other meanings as well.
                    
#                    print(json.dumps(Curr_Vocab, indent=4))
                          
                    if not is_data_already_saved(json_data, Curr_Vocab["Kana"], Curr_Vocab["Kana_Kanji"]):
                        json_data.append(Curr_Vocab)


                        write_json_file(json_data, "manga.json")
        clear = driver.find_element(By.CLASS_NAME, "search-form_clear-button_js").click()
    else:
        time_c = os.path.getctime(path)
        mod_file = time.ctime(time_c)

        json_data = read_json_file("manga.json")

        time.sleep(0.5)



