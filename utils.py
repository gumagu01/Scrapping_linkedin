import json 
import csv
from datetime import date,datetime
import re
import timeit
from memory_profiler import profile

def json_to_obj(filename):
    obj = None
    with open(filename) as json_file:
        obj = json.loads(json_file.read())
    return obj

@profile
def extraction(api,company):
    profiles = []
    starter = datetime.now()
    diretores = api.search_people(current_company=[company],title='Diretor',start=0,keywords='diretor')
    end= datetime.now()
    print(end - starter)
    directors = api.search_people(current_company=[company],title='Director',start=0)
    diretoras = api.search_people(current_company=[company],title='Diretora',start=0,keywords='diretora')
    vp = api.search_people(current_company=[company],title='vice presidente',start=0)
    head = api.search_people(current_company=[company],title='head of',start=0)
    profiles = diretores + vp + directors + head + diretoras
    return profiles

def read_csv(path):
    with open(path, encoding='utf-8') as f:
        a = [{str(k):str(v) for k, v in row.items()}
            for row in csv.DictReader(f, skipinitialspace=True)]
        return a

def write_csv2(profiles,path,model,status='in'):
    with open('./{}.csv'.format(path), '{}'.format(model), newline='',encoding='utf-8') as f:
                writer = csv.writer(f)
                if model != 'a' :
                    writer.writerow(["Nome", "Cargo","dataMudanca"])
                    for item in profiles:
                        writer.writerow([item["Nome"], item["Cargo"],item["dataMudanca"]])
                else:
                    for item in profiles:
                        writer.writerow([item["Nome"], item["Cargo"],status,item["dataMudanca"]])
def write_csv(profiles,path):
    with open('./results/{}.csv'.format(path), 'w', newline='',encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Nome", "Cargo","dataMudanca"])
                for item in profiles:
                    writer.writerow([item["Nome"], item["Cargo"],date.today()])

def compare(profiles,atual,empresa):
    arquivo = empresa['arquivo']
    profiles = [ x for x in profiles if  (bool(re.search(r"(?i)\bDiretor\b",x["Cargo"])) or bool(re.search(r"(?i)\bDirector\b",x["Cargo"]))or bool(re.search(r"(?i)\bDiretora\b",x["Cargo"])) or
      bool(re.search(r"(?i)\bVP\b",x["Cargo"])) or bool(re.search(r"(?i)\bVice Presidente\b",x["Cargo"])) or 
      bool(re.search(r"(?i)\bVice President\b",x["Cargo"])) or bool(re.search(r"(?i)\bVice-Presidente\b",x["Cargo"]))
      or bool(re.search(r"(?i)\bHead of\b",x["Cargo"])) or bool(re.search(r"(?i)\bCFO\b",x["Cargo"]) or bool(re.search(r"(?i)\bCEO\b",x["Cargo"])) or bool(re.search(r"(?i)\bCOO\b",x["Cargo"])))) ]
    for i in profiles:
        mudancas=[]
        g=0
        if not any(d['Nome'] == i['Nome'] for d in atual):
            i["dataMudanca"]=str(date.today())
            atual.append(i)
            print("Entrou:  " + arquivo)
            g=1
            mudancas.append(i)
            atual.append(i)       
        if g==1:
            write_csv2(atual,'results/{}'.format(arquivo),'w')
            write_csv2(mudancas,'out/{}'.format(arquivo),'a','in')

    for i in atual:
        mudancas=[]
        if not any(d['Nome'] == i['Nome'] for d in profiles):
            i["dataMudanca"]=str(date.today()) 
            atual.remove(i)
            mudancas.append(i)
        if len(mudancas)>0:
            write_csv2(atual,'results/{}'.format(arquivo),'w')
            print("mudanca "+ str(arquivo))
            write_csv2(mudancas,'out/{}'.format(arquivo),'a','out')