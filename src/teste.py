import requests
from bs4 import BeautifulSoup

def build_json_response(line_data: list) -> dict:
  response = {}
  if line_data[0] == 'CNPJ':
    response['cnpj'] = line_data[1]
  if line_data[0] == 'Inscrição Estadual MG':
    response['state_registration'] = line_data[1]
  if line_data[0] == 'Nome de Fantasia':
    response['trade_name'] = line_data[1]
  if line_data[0] == 'Nome Empresarial':
    response['corporate_name'] = line_data[1]
  if line_data[0] == 'Data da Abertura':
    response['creation_date'] = line_data[1]
  if line_data[0] == 'Capital Social':
    response['capital_social'] = line_data[1]
  if line_data[0] == 'Tipo':
    response['type'] = line_data[1]
  if line_data[0] == 'Situação':
    response['status'] = line_data[1]
  if line_data[0] == 'Natureza Jurídica':
    response['legal_status'] = line_data[1]

  return response


def capture_data_company(url: str) -> dict:
  """
  Função que espera uma URL de detalhes de uma empresa dentro do site cadastroempresa.com.br
  Retorna os dados em forma de JSON
  """
  response = requests.get(url)
  content = response.content
  page_company = BeautifulSoup(content, 'html.parser')

  div_registry = page_company.find('div', attrs={'class': 'bg-white shadow sm:rounded-lg mb-3 mt-3 p-0.5'})
  div_info_registry = div_registry.find('div', attrs={'class': 'mx-auto border-t border-gray-200 p-2 sm:p-4 grid max-w-2xl grid-cols-1 gap-2 sm:gap-4 sm:grid-cols-2 lg:max-w-none lg:grid-cols-3'})
  data = div_info_registry.findAll('dl')

  data_return = {}
  for line in data:
    if line.dt:
      data_return.update({line.dt.text.strip(' ').lower().replace(' ', '_'): line.p.text.strip(' ') if line.p else line.dd.text.strip(' ')})
  return data_return


def capture_links_company(content) -> list:
  """
  Função que espera um content de listagem dentro do site cadastroempresa.com.br
  Retorna links de todas as empresas
  """
  page_company = BeautifulSoup(content, 'html.parser')

  uls_company = page_company.findAll('ul', attrs={'class': 'divide-gray-200'})

  links = []
  for ul_tag in uls_company:
    lis_company = ul_tag.findAll('li')
    for li_tag in lis_company:
      link = li_tag.find('a')
      links.append(link['href'])
  
  return links
