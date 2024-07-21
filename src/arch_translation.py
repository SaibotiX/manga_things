#Make it so that if there is no link attached to a vocabulary to skip it and not to let the program crash!
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
from selenium.common.exceptions import NoSuchElementException

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

def is_element_empty(element):
    try:
        # Check if the inner HTML is empty or contains only whitespace
        inner_html = element.get_attribute('innerHTML').strip()
        return inner_html == ''
    except NoSuchElementException:
        # Handle the case where the element does not exist
        return True
    
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


        count = 0

        full_dict = {}
        
        Curr_Iteration = {
        }

        Japanese_Word = driver.find_elements(By.CLASS_NAME, "japanese_word")

        for voc in Japanese_Word:
            voc.click()
            time.sleep(0.5)
            count = 0
            
            try:
                driver.implicitly_wait(0)
                no_matches = WebDriverWait(driver, 0.1).until(
                    EC.presence_of_element_located((By.ID, "no-matches"))
                )
                driver.implicitly_wait(10)

                print("Didnt find word")
                continue
            except TimeoutException:
                pass

                element_test = driver.find_element(By.CLASS_NAME, "large-8")

                if is_element_empty(element_test):
                    print("The element is empty.")
                    continue
                else:
                    pass
            
            try:
                WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable(voc))
            except TimeoutException:
                print("Not clicked")
                continue

            japanese_word_n_furigana = None
            japanese_word_y_furigana = None
            try:
                driver.implicitly_wait(0)
# I change here the ...word_n_... to ...word_y_... !!!!
                japanese_word_y_furigana = WebDriverWait(driver, 0.1).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "japanese_word__text_with_furigana"))).text
                driver.implicitly_wait(10)
            except TimeoutException:
                print("japanese_word_y_furigana TimeoutException")
                continue
            
            try:
                driver.implicitly_wait(0)
# I change here the ...word_y_... to ...word_n_... for bug checking!!!              
                japanese_word_n_furigana = WebDriverWait(driver, 0.1).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "japanese_word__furigana"))).text
                driver.implicitly_wait(10)
            except TimeoutException:
                print("japanese_word_n_furigana TimeoutException")
                continue

            Curr_Iteration[japanese_word_n_furigana] = {} 
            Curr_Iteration[japanese_word_n_furigana]["Furigana"] = japanese_word_y_furigana

            linkable = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, "//li[@class='clearfix japanese_word']")))
            
            large_eight = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "large-8")))

            concept_light = large_eight.find_elements(By.CLASS_NAME, "concept_light")
            concept_light = concept_light[:3]
            count = 0

            for element in concept_light:
                concept_light_wrapper = element.find_element(By.CLASS_NAME, "concept_light-wrapper")
                furigana_text = concept_light_wrapper.find_element(By.CLASS_NAME, "furigana").text
                text_text = concept_light_wrapper.find_element(By.CLASS_NAME, "text").text

                main_iteration = f"Translation_{count}"

                Curr_Iteration[japanese_word_n_furigana][main_iteration] = {}
                Curr_Iteration[japanese_word_n_furigana][main_iteration]["Furigana"] = furigana_text
                Curr_Iteration[japanese_word_n_furigana][main_iteration]["Kanji"] = text_text

                if os.path.getsize("/home/zuckram/Desktop/shit/Japanese/src/manga.json") != 0:
                    with open('manga.json', 'r') as file:
                        data = json.load(file)


                        for item in data:
                            json.dumps(item, indent=4)

                concept_light_meanings = element.find_element(By.CLASS_NAME, "concept_light-meanings")

                meaning_wrapper = concept_light_meanings.find_elements(By.CLASS_NAME, "meaning-wrapper")
                meaning_tags = concept_light_meanings.find_elements(By.CLASS_NAME, "meaning-tags")
                inner_count = 0
                for wrapper, tag in zip(meaning_wrapper, meaning_tags):
                    if tag.text == "Notes":
                        print("Notes found -- skipped")
                        continue
                    
                    Found_Translation = f"Translation{inner_count}"
                    Curr_Iteration[japanese_word_n_furigana][Found_Translation] = {}
                    inner_count = inner_count + 1
                    
                    meaning_meaning_text = wrapper.find_element(By.CLASS_NAME, "meaning-meaning").text

                    Curr_Iteration[japanese_word_n_furigana][Found_Translation]["Vocabulary"] = meaning_meaning_text

            count = count + 1
                    
        json_data = read_json_file("manga.json")

        json_data.append(Curr_Iteration)
        
        write_json_file(json_data, "manga.json")
        
        clear = driver.find_element(By.CLASS_NAME, "search-form_clear-button_js").click()
    else:
        time_c = os.path.getctime(path)
        mod_file = time.ctime(time_c)

        json_data = read_json_file("manga.json")

        time.sleep(0.5)
