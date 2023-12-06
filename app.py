from flask import Flask, Response, jsonify, request, json
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)

#lista de produtos
@app.route('/internal')
def ler():
    try:
        with open("teste.json", "r") as arquivo:
            json_objeto = json.load(arquivo)
        return json_objeto
    except IOError:
        return [] 

#consultar(todos)
@app.route('/produtos', methods=['GET'])
def obter_produtos():
    resultado = ler()

    return Response(
        response=json.dumps(resultado), status=200,  mimetype="text/plain")
    
#consultar(por id)
@app.route('/produtos/<int:id>',methods=['GET'])
def obter_produto_por_id(id):
    resultado = ler()
    for produto in resultado:
        if produto["id"] == id:
            return produto  
        
#editar
@app.route('/produtos/<int:id>',methods=['PUT'])
def editar_produto_por_id(id):
    produto_alterado = request.get_json()
    resultado = ler()
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
def incluir_novo_produto():
    novo_produto = request.get_json()
    resultado = ler()
    resultado.append(novo_produto)
    json_objeto = json.dumps(resultado, indent=4)

    with open("teste.json", "w") as arquivo:
        arquivo.write(json_objeto)
    
    
    return Response(
        response=json.dumps(True), status=200,  mimetype="text/plain")
    
#excluir
@app.route('/produtos/<int:id>',methods=['DELETE'])
def excluir_produto(id):
    resultado = ler()
    for indice,produto in enumerate(resultado):
        if produto["id"] == id:
            del resultado[indice]
    json_objeto = json.dumps(resultado, indent=4)
    
    with open("teste.json", "w") as arquivo:
        arquivo.write(json_objeto)
        return Response(content_type=True, status=200)
    
app.run(port=4000,host='localhost', debug=True)    