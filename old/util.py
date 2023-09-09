import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException


def corrigir_formato_data(df, coluna_data):
    df[coluna_data] = pd.to_datetime(df[coluna_data], dayfirst=True, errors='coerce').dt.strftime("%Y-%m-%d")
    df[coluna_data] = df[coluna_data].apply(lambda x: x if pd.notna(x) else None)
    return df