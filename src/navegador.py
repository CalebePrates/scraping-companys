from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from time import sleep
from teste import *

user_agent = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/39.0.2171.95 Safari/537.36"
)

options = Options()
options.add_argument("--headless")
options.add_argument("start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.add_argument("window-size=1920,1080")
options.add_argument(f"user-agent={user_agent}")
options.add_argument("--remote-debugging-port=9222")
options.add_argument("--disable-dev-shm-using")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("disable-infobars")
options.add_argument("--no-sandbox")
options.add_argument("--disable-setuid-sandbox")


def capture_data_in_link(links: list):
    for link in links:
        print(capture_data_company("https://cadastroempresa.com.br" + link))
        with open("retorno_24.txt", "a") as file:
            file.write(
                str(capture_data_company("https://cadastroempresa.com.br" + link))
                + "\n"
            )


navegador = webdriver.Chrome(
    service=ChromeService(ChromeDriverManager().install()), options=options
)
navegador.get("https://cadastroempresa.com.br/procura?q=abaete")

content = navegador.page_source
links = capture_links_company(content)
capture_data_in_link(links)
