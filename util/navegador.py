from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementNotInteractableException


from util.config import * 


class Navegador:
    def __init__(self, chrome_driver_path, logger):
        self.logger = logger

        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        #options.add_experimental_option(f"download.default_directory={diretorio_downloads}")
        options.add_experimental_option("prefs", {"download.default_directory":  diretorio_downloads, 
                                           "download.prompt_for_download": False, 
                                           "download.directory_upgrade": True})


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

    def pegar_valor_elemento_por_xpath(self, xpath):
        try:
            return self.driver.find_element(By.XPATH, xpath).text
        except (NoSuchElementException, TimeoutException):
            self.logger.info(f"Elemento com XPath '{xpath}' não encontrado na página {self.driver.current_url}")
            return None
    
    def pegar_elemento_por_xpath(self, xpath):
        try:
            return self.driver.find_element(By.XPATH, xpath)
        except (NoSuchElementException, TimeoutException):
            self.logger.info(f"Elemento com XPath '{xpath}' não encontrado na página {self.driver.current_url}")
            return None
        
    def pegar_elementos_filhos_por_tag(self, xpathpai, tag):
        try:
            pai = self.driver.find_element(By.XPATH, xpathpai)
            return pai.find_elements(By.TAG_NAME, tag)
        except (NoSuchElementException, TimeoutException):
            self.logger.info(f"Elemento com Tag '{tag}' não encontrado na página {self.driver.current_url}")
            return None

    def pegar_valor_elemento_por_id(self, element_id):
        try:
            return self.driver.find_element(By.ID, element_id).text
        except (NoSuchElementException, TimeoutException):
            self.logger.info(f"Elemento com ID '{element_id}' não encontrado na página {self.driver.current_url}")
            return None   
    
    def pegar_elemento_por_id(self, element_id):
        try:
            return self.driver.find_element(By.ID, element_id)
        except (NoSuchElementException, TimeoutException):
            self.logger.info(f"Elemento com ID '{element_id}' não encontrado na página {self.driver.current_url}")
            return None   
        
    def espere_click_element_xpath(self, xpath):
        try:
            # Aguardar até que o botão esteja visível na página (tempo limite de 10 segundos)
            export_button = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//button[@class="dt-button buttons-excel buttons-html5"]'))
            )
            export_button.click()
        except Exception as e:
            print(e)

    def espere_click_element_xpath(self, xpath):
        try:
            # Aguardar até que o botão esteja visível na página (tempo limite de 10 segundos)
            export_button = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, xpath))
            )
            export_button.click()
        except Exception as e:
            print(e)

    def move_slider(self, element_slidder, offset_percentage):
        try:
            slider_handle = self.pegar_elemento_por_xpath(element_slidder)

            if offset_percentage > 0:
                 current_value = slider_handle.text.replace(",", ".")
                 current_value = float(current_value)
                 increment = current_value * offset_percentage / 100
                 increment += current_value
            else:
                 increment = offset_percentage

            move = ActionChains(self.driver)
            move.click_and_hold(slider_handle).move_by_offset(increment, 0).release().perform()
        except Exception as e:
            self.logger.exception(f"Erro ao alterar o slider: {e}")

    
    def marcar_checkbox(self, checkbox):
        try:
            if not checkbox.is_selected():
                checkbox.click()
        except ElementNotInteractableException as e:
            self.logger.exception(f'Erro ao interagir com o checkbox: {e}')

    def fechar_driver(self):
        self.driver.quit()