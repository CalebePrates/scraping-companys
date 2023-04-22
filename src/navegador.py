from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
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

navegador = webdriver.Chrome(options=options)
navegador.get('https://cadastroempresa.com.br/procura?q=uberlandia')

content = navegador.page_source
links = capture_links_company(content)
capture_data_in_link(links)

sleep(5)
btn_next_is_visible = navegador.find_element(By.PARTIAL_LINK_TEXT, 'Próximo')
while btn_next_is_visible:
  btn_next = navegador.find_element(By.PARTIAL_LINK_TEXT, 'Próximo')
  btn_next.click()
  sleep(0.5)
  content = navegador.page_source
  links = capture_links_company(content)
  capture_data_in_link(links)
  sleep(5)
  btn_next_is_visible = navegador.find_element(By.PARTIAL_LINK_TEXT, 'Próximo')
