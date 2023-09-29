import requests
import patoolib
import glob

def _get_file():
    my_headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",  "Accept":"text/html,application/xhtml+xml,application/xml; q=0.9,image/webp,image/apng,*/*;q=0.8"}
    response = requests.get('https://portaldatransparencia.gov.br/download-de-dados/pep/202308', headers=my_headers)

    f = open("data.rar", "wb")
    f. write(response.content)
    f. close()
    patoolib.extract_archive("data.rar", outdir="./")

def _get_data_pep(filename: str) -> list:
    data_pep = []
    with open('202308_PEP.csv') as f:
        lines = f.readlines()
        for line in lines:
            person = line.replace(";", "").replace("\n", '')
            person_list = person.split('""')
            person_list[0].replace('"', '')
            person_list[len(person_list)-1].replace('"', '')
            person_list.append(person_list)
    return data_pep

def _get_filename_csv():
    list_of_files = glob.glob('/path/to/folder/*')
    latest_file = max(list_of_files, key=os.path.getctime)
    print(latest_file)

_get_file()
_get_data_pep()