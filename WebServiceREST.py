import json
from flask import Flask
from flask import current_app, flash, jsonify, make_response, redirect, request, url_for, abort
from flask_httpauth import HTTPBasicAuth
from datetime import datetime

auth = HTTPBasicAuth()

app = Flask(__name__)

previsoesDoTempo = [
        {
            'id' : 1,
            'temperatura' : '15',
            'umidade' : '90%',
            'luminosidade': 'Parcialmente nublado',
            'data': '05-10-2022',
            'hora': '20:50',
        },
        {
            'id' : 2,
            'temperatura' : '27',
            'umidade' : '50%',
            'luminosidade': 'Ensolarado',
            'data': '23-11-2022',
            'hora': '11:52',
        },
        {
            'id' : 3,
            'temperatura' : '7',
            'umidade' : '30%',
            'luminosidade': 'Nublado',
            'data': '23-11-2022',
            'hora': '22:51',
        }

]

# curl -i http://127.0.0.1:5000/tempo

# get em http://127.0.0.1:5000/tempo para pegar todas as previsoes
@app.route('/tempo', methods=['GET'])
def retornaPrevisoes():
    return jsonify({'previsoes': previsoesDoTempo})


# curl -i http://127.0.0.1:5000/tempo/1
# get em http://127.0.0.1:5000/tempo/idPrevisao para pegar uma previsao em especifico
@app.route('/tempo/<int:idPrevisao>', methods=['GET'])
def weather_detail(idPrevisao):
    for r in previsoesDoTempo:
        if r['id'] == idPrevisao:
            resultado = r
    if len(resultado) == 0:
        abort(404)
    #return jsonify({'previsoes': resultado})
    return resultado

@app.route('/tempo/<string:data>', methods=['GET'])
def weather_detailFromDate(data):
    resultado = []
    tam = 0
    for r in previsoesDoTempo:
        if r['data'] == data:
            resultado.append(r)
            tam+=1
    if len(resultado) == 0:
        abort(404)
    return jsonify({'previsoes': resultado, 'tam': tam})

# pegar ultima previsao adicionada a previsoesDoTempo
@app.route('/tempo/ultimo', methods=['GET'])
def retornaUltimaPrevisao():
    resultado = previsoesDoTempo[-1]
        
    if len(resultado) == 0:
        abort(404)
    #return jsonify({'previsoes': resultado})
    return resultado

# curl -i -X DELETE http://127.0.0.1:5000/tempo/2
# deletar uma previsao do tempo
@app.route('/tempo/<int:idPrevisao>', methods=['DELETE'])
def excluir_previsao(idPrevisao):
    resultado = [
        resultado for resultado in previsoesDoTempo if resultado['id'] == idPrevisao
    ]
    if len(resultado) == 0:
        abort(404)
    previsoesDoTempo.remove(resultado[0])
    return jsonify({'resultado': True})


# curl -i -H "Content-Type: application/json" -X POST -d '{"temperatura":"666","umidade":"666","luminosidade":"666","data":"666","hora":"666"}' http://127.0.0.1:5000/livros
# adicionar uma previsão do tempo
@app.route('/tempo', methods=['POST'])
def adicionar_previsao():
    currentDateAndTime = datetime.now()

    if not request.json or not 'temperatura' in request.json:
        abort(400)
    livro = {
        'id': previsoesDoTempo[-1]['id'] + 1,
        'temperatura': request.json['temperatura'],
        'umidade': request.json.get('umidade', ""),
        'luminosidade': request.json.get('luminosidade',""),
        'data': f"{currentDateAndTime.day}-{currentDateAndTime.month}-{currentDateAndTime.year}",
        'hora': f"{currentDateAndTime.hour}:{currentDateAndTime.minute}",
    }
    previsoesDoTempo.append(livro)
    return jsonify({'livro': livro}), 201

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'erro': 'Recurso Nao encontrado'}), 404)


# Update

@app.route('/tempo/<int:idPrevisao>', methods=['PUT'])
def update(idPrevisao):
    currentDateAndTime = datetime.now()

    for r in previsoesDoTempo:
        if r['id'] == idPrevisao:

            r.update({"temperatura": request.json['temperatura']})
            r.update({"umidade": request.json['umidade']})
            r.update({"luminosidade": request.json['luminosidade']})
            r.update({"data": f"{currentDateAndTime.day}-{currentDateAndTime.month}-{currentDateAndTime.year}"})
            r.update({"hora": f"{currentDateAndTime.hour}:{currentDateAndTime.minute}"})

            retorno = r


    return retorno

if __name__ == "__main__":
    app.run(debug=False)