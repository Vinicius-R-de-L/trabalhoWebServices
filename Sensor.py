import requests
from random import randint
import time

luminosidade = ['Parcialmente nublado', 'Nublado', 'Ensolarado', 'Chuvoso', 'Tempestade']
i = 0
while True:
    while i < 5: 
        url = "http://127.0.0.1:5000/tempo"
        json = {"temperatura":f"{randint(-5,33)}","umidade":f"{randint(0,100)}%","luminosidade":f"{luminosidade[i]}"}
        response = requests.post(url, json=json)
        i+=1
        time.sleep(10)
        if i == 4:
            i = 0