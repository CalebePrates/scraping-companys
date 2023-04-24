# scraping-companys
O objetivo é desenvolver uma forma automatizada de extração de dados de todas empresas do Brasil.

Pendências:
- Corrigir limitação de requisições:
https://stackoverflow.com/questions/71885891/urllib3-exceptions-maxretryerror-httpconnectionpoolhost-localhost-port-5958

- Melhorar velocidade de captação dos dados
    Tentar utilizar Thread, subprocesso e diminuir os sleeps

- Capturar dados de contato e localização

- Desenvolver um fluxo de captura multi cidades (Uberlandia e Uberaba)
    Verificar se a quantidade captura bate com o total das cidades

- Pensar e preparar uma estrutura de dados para inserir todos dados capturados em um banco de dados sem necessidade de inserir um por um

- Estudar uma forma de implementar um "esperar" em forma de condicional (while) e retirar sleeps do código

- Testar tirar bloqueio com undetected_chromedriver caso o selenium-stealth não funcione