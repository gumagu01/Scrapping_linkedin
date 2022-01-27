from Api.linkedin import Linkedin
import csv
import json
import re

filename = "credentialslk.json"

def json_to_obj(filename):
    obj = None
    with open(filename) as json_file:
        obj = json.loads(json_file.read())
    return obj  


def write_csv(profiles):
    with open('./Linkedin/results/NotreDame2.csv', 'w', newline='',encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Nome do executivo", "Cargo","Cidade"])
                for item in profiles:
                    writer.writerow([item["Nome"], item["Cargo"],item["city"]])


credentials =  json_to_obj(filename)
api = Linkedin(credentials["torkuser"], credentials["torkpass"])

profiles = api.search_people(current_company=["68907"],title='Diretor',start=0,keywords='diretor')
profiles2 = [ x for x in profiles if  (bool(re.search(r"(?i)\bDiretor\b",x["Cargo"])) or bool(re.search(r"(?i)\bDirector\b",x["Cargo"])))  ]

write_csv(profiles2)       

