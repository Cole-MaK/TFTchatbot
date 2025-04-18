import google
from google import genai

import numpy as np
import pandas as pd
import pickle

from dotenv import load_dotenv
import os
import json
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

from functions.functions import get_rag_file, get_filters

prompt = str(input("Questions: "))

filter_list = get_filters(prompt)
print(filter_list)
if filter_list:
    path = "/Users/colemak/Documents/projects/tftchatbot/chromedriver"
    service = Service(path)
    chrome_options = Options()
    driver = webdriver.Chrome(service = service, options=chrome_options)
    # url = "https://tactics.tools/explorer-advanced/"
    url = "https://tactics.tools/explorer"
    driver.get(url)


    try:
        for i, champion in enumerate(filter_list):

            dropdown_trigger = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.XPATH, f"//input[contains(@class, 'MuiInputBase-input MuiInput-input font-montserrat font-medium MuiInputBase-inputAdornedStart MuiInputBase-inputAdornedEnd MuiAutocomplete-input MuiAutocomplete-inputFocused css-1jhxu0') and contains(@placeholder, 'Filter #{i+1}')]"))
            )
            dropdown_trigger.click()

            dropdown_options = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.XPATH, f"//span[contains(@class, 'font-montserrat leading-tight font-medium inline text-base pl-[6px]') and normalize-space(text()) = '{champion}']"))
            )
            dropdown_options.click()

        time.sleep(1)

        WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.pl-\\[6px\\].truncate"))
        )

        # get name column
        elements = driver.find_elements(
        By.XPATH, "//div[contains(@class, 'pl-[6px') and contains(@class, 'truncate')]")

        names = [e.text for e in elements if e.text.strip()]

        # games, play-rate, top4
        table = driver.find_elements(
            By.XPATH, "//div[contains(@class, 'flex items-center justify-end  px-[14px] css-1wb4h96 tbl-cell-right-border')]"
        )
        
        table_ele = [e.text for e in table if e.text.strip()]

        # place and delta
        table_2 = driver.find_elements(
            By.XPATH, "//div[contains(@class, 'flex items-center justify-end  px-[14px] css-1xzb52b tbl-cell-right-border')]"
        )

        table_ele_2 = [e.text for e in table_2 if e.text.strip()]

        # win percentage
        table_3 = driver.find_elements(
            By.XPATH, "//div[contains(@class, 'flex items-center justify-end  px-[14px] css-14lx2h1 tbl-cell-right-border')]"
        )

        table_ele_3 = [e.text for e in table_3 if e.text.strip()]


        games_list = []
        playrate_list = []
        top4_list = []
        place_list = []
        delta_list = []
        winP_list = []

        for i in range(0, len(table_ele), 3):
            games_list.append(table_ele[i])
        for i in range(1, len(table_ele), 3):
            playrate_list.append(table_ele[i])
        for i in range(2, len(table_ele), 3):
            top4_list.append(table_ele[i])
        for i in range(0, len(table_ele_2), 2):
            place_list.append(table_ele_2[i])
        for i in range(1, len(table_ele_2), 2):
            delta_list.append(table_ele_2[i])
        for i in range(0, len(table_ele_3)):
            winP_list.append(table_ele_3[i])

        datatable = pd.DataFrame(list(zip(names[0:len(games_list)],games_list, playrate_list, place_list, delta_list, top4_list, winP_list)),
        columns=['Champion','# of games','play rate','place','delta','top4','winP'])
        print(datatable)


    except Exception as e:
        print(f"An Error Occured: {e}")
    finally:
        driver.quit()
else:
    print('No Valid Filter')
