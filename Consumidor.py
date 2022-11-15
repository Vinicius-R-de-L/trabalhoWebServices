import requests
import json
import PySimpleGUI as sg
from threading import Thread
import sys
import time

sg.theme("LightGreen")

border_size = 2


temperatura = '0°'
umidade = '0%'
luminosidade = '-'
data = '-'
hora = '-'

stringPrevisoes = ""
qntd_previsoes = 0
qntd = ''

stringPrevisao = ""

stopThread = False

Home = [
    [sg.Text("")],
    [sg.Text("")],
    [sg.Text("", size=10)],
    [sg.Text("", key="temperatura", background_color="grey")],
    [sg.Text("Umidade:"), sg.Text("", key="umidade")],
    [sg.Text("", key="luminosidade")],
    [sg.Text("", key="data"), sg.Text("", key="hora")],
    [sg.Text("")]
]

Criar = [ 
    [sg.Text("", size=10)],
    [sg.Text("Temperatura")],
    [sg.InputText(do_not_clear=False, key='temp', size=20)],
    [sg.Text("Umidade")],
    [sg.InputText(do_not_clear=False, key='umi', size=20)],
    [sg.Text("Luminosidade")],
    [sg.InputText(do_not_clear=False, key='lumi', size=20)],
    [sg.Button("Criar")],
    [sg.Text("")]
]

Deletar = [
    [sg.Text("", size=(10,4))],
    [sg.Text("Id")],
    [sg.InputText(do_not_clear=False, key="id", size=20)],
    [sg.Button("Deletar")],
    [sg.Text("")]
]

Filtrar = [ 
    [sg.Text("Data"), sg.InputText(do_not_clear=False, key="dahtah", size=15), sg.Button("Filtrar")],
    [sg.Text(key="qntd")],
    [sg.Button("<<<"),sg.Button(">>>")],
    [sg.Text("")],
    [sg.Text(key="showPrevisoes")]
]

Buscar = [ 
    [sg.Text("Id"), sg.InputText(do_not_clear=False, key="idkey", size=15), sg.Button("Buscar")],
    [sg.Text("")],
    [sg.Text(key="showPrevisao")]
]

Atualizar = [ 
    [sg.Text("", size=10)],
    [sg.Text("Id")], 
    [sg.InputText(do_not_clear=False, key="keyId", size=15)],
    [sg.Text("Temperatura")],
    [sg.InputText(do_not_clear=False, key='_temp', size=20)],
    [sg.Text("Umidade")],
    [sg.InputText(do_not_clear=False, key='_umi', size=20)],
    [sg.Text("Luminosidade")],
    [sg.InputText(do_not_clear=False, key='_lumi', size=20)],
    [sg.Button("Atualizar")],
    [sg.Text("")]
]

Telas = [
    [
        sg.TabGroup(
            [
                [
                    sg.Tab('Home', Home, title_color = 'White', border_width = border_size, element_justification = 'center'),
                    sg.Tab('Criar', Criar, title_color = 'White', border_width = border_size, element_justification = 'center'),
                    sg.Tab('Deletar', Deletar, title_color = 'White', border_width = border_size, element_justification = 'center'),
                    sg.Tab('Filtrar', Filtrar, title_color = 'White', border_width = border_size, element_justification = 'center'),
                    sg.Tab('Buscar', Buscar, title_color = 'White', border_width = border_size, element_justification = 'center'),
                    sg.Tab('Atualizar', Atualizar, title_color = 'White', border_width = border_size , element_justification = 'center'),
                ]
            ]
        )
    ]
]

#json = {"temperatura":f"{randint(-5,33)}","umidade":f"{randint(0,100)}%","luminosidade":f"{luminosidade[i]}","data":f"{currentDateAndTime.day}/{currentDateAndTime.month}/{currentDateAndTime.year}","hora":f"{currentDateAndTime.hour}:{currentDateAndTime.minute}"}

app = sg.Window("Tempo", Telas, finalize=True, margins=(0,0))

def ultima_leitura():

    while True:
        global stopThread

        if stopThread:
            sys.exit()

        url = "http://127.0.0.1:5000/tempo/ultimo"
        response = requests.get(url)
        response = response.content.decode()
        data = json.loads(response)
        
        if int(data['temperatura']) > 24:
            app['temperatura'].update((data['temperatura'])+'°', text_color="red")
        if int(data['temperatura']) > 10 and int(data['temperatura']) <= 24:
            app['temperatura'].update((data['temperatura'])+'°', text_color="yellow")
        if int(data['temperatura']) <= 10:
            app['temperatura'].update((data['temperatura'])+'°', text_color="blue")
        app['umidade'].update(data['umidade'])
        app['luminosidade'].update(data['luminosidade'])
        app['data'].update(data['data'])
        app['hora'].update(data['hora'])

        time.sleep(3)

thread = Thread(target=ultima_leitura)
thread.start()

class Previsao:
  def __init__(self, id, temperatura, umidade, luminosidade, data, hora):
    self.id = id
    self.temperatura = temperatura
    self.umidade = umidade
    self.luminosidade = luminosidade
    self.data = data
    self.hora = hora


while True:

    event,values = app.read()

    if event == sg.WIN_CLOSED:
        stopThread = True
        break
    
    if event == "Criar":
        url = "http://127.0.0.1:5000/tempo"
        jerson = {"temperatura":f"{values['temp']}","umidade":f"{values['umi']}%","luminosidade":f"{values['lumi']}"}
        response = requests.post(url, json=jerson)
    
    if event == "Deletar":
        url = f"http://127.0.0.1:5000/tempo/{values['id']}"
        response = requests.delete(url)
    
    if event == "Filtrar" and values['dahtah'] != '':
        url = f"http://127.0.0.1:5000/tempo/{values['dahtah']}"
        response = requests.get(url)
        response = response.content.decode()
        data2 = json.loads(response)

        lista_previsoes = []
        #print(data2)
        if str(data2) == "{'erro': 'Recurso Nao encontrado'}":
            stringPrevisoes = "Erro: Recurso Nao encontrado"
            app['showPrevisoes'].update(stringPrevisoes)
        else:
            for each in data2['previsoes']:
                i = each['id']
                t = each['temperatura']
                u = each['umidade']
                l = each['luminosidade']
                d = each['data']
                h = each['hora']
                previsao = Previsao(id=i,temperatura=t,umidade=u,luminosidade=l,data=d,hora=h)
                lista_previsoes.append(previsao)

            qntd_previsoes = len(lista_previsoes)-1

            stringPrevisoes = ''
            stringPrevisoes += f"Id: {lista_previsoes[0].id}\n"
            stringPrevisoes += f"Temperatura: {lista_previsoes[0].temperatura}°\n"
            stringPrevisoes += f"Umidade: {lista_previsoes[0].umidade}\n"
            stringPrevisoes += f"Luminosidade: {lista_previsoes[0].luminosidade}\n"
            stringPrevisoes += f"Data: {lista_previsoes[0].data}\n"
            stringPrevisoes += f"Hora: {lista_previsoes[0].hora}\n"

            app['showPrevisoes'].update(stringPrevisoes)

        qntd = f"1/{qntd_previsoes+1}"
        app['qntd'].update(qntd)
        previsao_atual = 0

    if event == "<<<" and previsao_atual != 0:
        previsao_atual -= 1
        stringPrevisoes = ''
        stringPrevisoes += f"Id: {lista_previsoes[previsao_atual].id}\n"
        stringPrevisoes += f"Temperatura: {lista_previsoes[previsao_atual].temperatura}°\n"
        stringPrevisoes += f"Umidade: {lista_previsoes[previsao_atual].umidade}\n"
        stringPrevisoes += f"Luminosidade: {lista_previsoes[previsao_atual].luminosidade}\n"
        stringPrevisoes += f"Data: {lista_previsoes[previsao_atual].data}\n"
        stringPrevisoes += f"Hora: {lista_previsoes[previsao_atual].hora}\n"

        app['showPrevisoes'].update(stringPrevisoes)
        qntd = f"{previsao_atual+1}/{qntd_previsoes+1}"
        app['qntd'].update(qntd)
    if event == ">>>" and qntd_previsoes != previsao_atual:
        previsao_atual += 1
        stringPrevisoes = ''
        stringPrevisoes += f"Id: {lista_previsoes[previsao_atual].id}\n"
        stringPrevisoes += f"Temperatura: {lista_previsoes[previsao_atual].temperatura}°\n"
        stringPrevisoes += f"Umidade: {lista_previsoes[previsao_atual].umidade}\n"
        stringPrevisoes += f"Luminosidade: {lista_previsoes[previsao_atual].luminosidade}\n"
        stringPrevisoes += f"Data: {lista_previsoes[previsao_atual].data}\n"
        stringPrevisoes += f"Hora: {lista_previsoes[previsao_atual].hora}\n"
        
        app['showPrevisoes'].update(stringPrevisoes)
        qntd = f"{previsao_atual+1}/{qntd_previsoes+1}"
        app['qntd'].update(qntd)

    if event == "Buscar":
        url = f"http://127.0.0.1:5000/tempo/{values['idkey']}"
        response = requests.get(url)
        response = response.content.decode()
        data3 = json.loads(response)
        stringPrevisao = ''
        stringPrevisao += f"Id: {data3['id']}\n"
        stringPrevisao += f"Temperatura: {data3['temperatura']}°\n"
        stringPrevisao += f"Umidade: {data3['umidade']}\n"
        stringPrevisao += f"Luminosidade: {data3['luminosidade']}\n"
        stringPrevisao += f"Data: {data3['data']}\n"
        stringPrevisao += f"Hora: {data3['hora']}\n"
        app['showPrevisao'].update(stringPrevisao)

    if event == "Atualizar":
        url = f"http://127.0.0.1:5000/tempo/{values['keyId']}"
        jsom = {"temperatura":f"{values['_temp']}","umidade":f"{values['_umi']}%","luminosidade":f"{values['_lumi']}"}
        response = requests.put(url, json=jsom)
