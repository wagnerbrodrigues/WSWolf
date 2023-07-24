from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

class Navegador:
    def __init__(self, chrome_driver_path, logger):
        self.logger = logger

        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")

        service = Service(chrome_driver_path)  # Insira o caminho para o chromedriver
        self.driver= webdriver.Chrome(service=service, options=options)  

    def pagina_ativa(self, xpath):
        try:
            WebDriverWait(self.driver, 0.25).until(EC.presence_of_element_located((By.XPATH, xpath)))
            return True
        except (NoSuchElementException, TimeoutException) as e:
            print(e)
            self.logger.info(f"Pagina {self.driver.current_url} não existe")
            return False

    def pegar_elemento_por_xpath(self, xpath):
        try:
            return self.driver.find_element(By.XPATH, xpath).text
        except (NoSuchElementException, TimeoutException):
            self.logger.info(f"Elemento com XPath '{xpath}' não encontrado na página {self.driver.current_url}")
            return None

    def pegar_elemento_por_id(self, element_id):
        try:
            return self.driver.find_element(By.ID, element_id)
        except (NoSuchElementException, TimeoutException):
            self.logger.info(f"Elemento com ID '{element_id}' não encontrado na página {self.driver.current_url}")
            return None   

    def fechar_driver(self):
        self.driver.quit()