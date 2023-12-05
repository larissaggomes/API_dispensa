from flask import Flask, Response, jsonify, request, json
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app, resources={r"/foo": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-type'

#consultar(todos)
@app.route('/produtos', methods=['GET'])
@cross_origin(origin='+',headers=['Content- Type','Authorization'])
def obter_produto():
    try:
        with open("teste.json", "r") as arquivo:
            json_objeto = json.load(arquivo)
        return json_objeto
    except IOError:
        return []   
    
#consultar(por id)
@app.route('/produtos/<int:id>',methods=['GET'])
def obter_produto_por_id(id):
    resultado = obter_produto()
    for produto in resultado:
        if produto["id"] == id:
            return produto  
        
#editar
@app.route('/produtos/<int:id>',methods=['PUT'])
def editar_produto_por_id(id):
    produto_alterado = request.get_json()
    resultado = obter_produto()
    for produto in resultado:
        if produto["id"] == id:
            produto["nome"] = produto_alterado["nome"]
            produto["preco"] = produto_alterado["preco"] 
    json_objeto = json.dumps(resultado, indent=4)

    with open("teste.json", "w") as arquivo:
        arquivo.write(json_objeto)
        return produto_alterado
    
#criar 
@app.route('/produtos',methods=['POST'])
@cross_origin()        
def incluir_novo_produto():
    novo_produto = request.get_json()
    resultado = obter_produto()
    resultado.append(novo_produto)
    json_objeto = json.dumps(resultado, indent=4)

    with open("teste.json", "w") as arquivo:
        arquivo.write(json_objeto)
        return Response(content_type=True, status=200)
    
#excluir
@app.route('/produtos/<int:id>',methods=['DELETE'])
def excluir_produto(id):
    resultado = obter_produto()
    for indice,produto in enumerate(resultado):
        if produto["id"] == id:
            del resultado[indice]
    json_objeto = json.dumps(resultado, indent=4)
    
    with open("teste.json", "w") as arquivo:
        arquivo.write(json_objeto)
        return Response(content_type=True, status=200)
    
app.run(port=4000,host='localhost', debug=True)    