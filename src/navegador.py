from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
import threading
from time import sleep
from teste import *

user_agent =  ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
'AppleWebKit/537.36 (KHTML, like Gecko) '
'Chrome/39.0.2171.95 Safari/537.36')

options = Options()
options.add_argument("start-maximized")
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument(f'user-agent={user_agent}')

def capture_data_in_link(links: list):
  for link in links:
    print(capture_data_company('https://cadastroempresa.com.br'+link))
    with open("retorno_24.txt", "a") as file:
      file.write(str(capture_data_company('https://cadastroempresa.com.br'+link))+'\n')

def flow_from_extract_data(city: str):
  navegador = webdriver.Chrome(options=options)
  stealth(navegador,
          languages=["en-US", "en"],
          vendor="Google Inc.",
          platform="Win32",
          webgl_vendor="Intel Inc.",
          renderer="Intel Iris OpenGL Engine",
          fix_hairline=True,
        )
  navegador.get('https://cadastroempresa.com.br/procura?q='+city)
  content = navegador.page_source
  print(content)
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
  navegador.quit()

threading.Thread(target=flow_from_extract_data('araxa')).start()
threading.Thread(target=flow_from_extract_data('uberaba')).start()
