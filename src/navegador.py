from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
from teste import *


def capture_data_in_link(links: list):
  for link in links:
    print(capture_data_company('https://cadastroempresa.com.br'+link))
    with open("retorno1.txt", "a") as file:
      file.write(str(capture_data_company('https://cadastroempresa.com.br'+link))+'\n')


options = Options()
options.add_argument('--headless')
options.add_argument('window-size=1920,1080')

navegador = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
navegador.get('https://cadastroempresa.com.br/procura?q=abaete')

content = navegador.page_source
links = capture_links_company(content)
capture_data_in_link(links)