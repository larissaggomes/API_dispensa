from flask import Flask, Response, request, json
from flask_cors import CORS
import time

app = Flask(__name__)
cors = CORS(app)
DB = "dbdata.json"

def generateId():
    # pegando a data e hora em formato timestamp (migrosegundos)
    timestamp = time.time()
    # removendo o ponto que separa os segundos
    timestamp = str(timestamp).replace('.','')
    # retornado o valor
    return timestamp

#lista de produtos
@app.route('/internal')
def ler():
    try:
        with open(DB, "r") as arquivo:
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
    res = ""
    resultado = ler()
    for produto in resultado:
        if int(produto["id"]) == int(id):
            res = produto
    
    return Response(
        response=json.dumps(res), status=200,  mimetype="text/plain")
          
        
#editar
@app.route('/produtos/<int:id>',methods=['PUT'])
def editar_produto_por_id(id):
    produto_alterado = request.get_json()
    resultado = ler()
    for produto in resultado:
        if int(produto["id"]) == int(id):
            produto["nome"] = produto_alterado["nome"]
            produto["preco"] = produto_alterado["preco"] 
            produto["estoqueMinimo"] = produto_alterado["estoqueMinimo"]
            produto["estoque"] = produto_alterado["estoque"]
    json_objeto = json.dumps(resultado, indent=4)

    with open(DB, "w") as arquivo:
        arquivo.write(json_objeto)
        return produto_alterado
    
#criar 
@app.route('/produtos',methods=['POST'])    
def incluir_novo_produto():
    # pegando a lista de produtos do banco de dados
    produtos = ler()

    # pegando os dados do produtos que veio no body da requisição
    novo_produto = request.get_json()
    # gerando e adicionado um novo id para o produto
    novo_produto['id'] = generateId()

    # adicionado o novo produto na lista de produtos
    produtos.append(novo_produto)
    # convertendo a lista de produtos em objetos json
    json_objeto = json.dumps(produtos, indent=4)

    # abrindo o banco de dados no modo escrita(W)
    with open(DB, "w") as arquivo:
        # escrevendo no arquivo a lista de produtos
        arquivo.write(json_objeto)
    
    
    return Response(
        response=json.dumps(True), status=200,  mimetype="text/plain")
    
#excluir
@app.route('/produtos/<int:id>',methods=['DELETE'])
def excluir_produto(id):
    # pegando a lista de produtos do banco de dados
    # a partir do metodo ler
    produtos = ler()

    # fazendo um loop na lista de produtos
    for indice,produto in enumerate(produtos):

        # comparando se o id do banco é igual
        # ao id enviando pela reguisição
        if int(produto["id"]) == int(id):

            # removendo o produto da lista a partir do indice (posição)
            del produtos[indice]

    # convertendo a lista de produtos em um objeto no formato texto
    json_objeto = json.dumps(produtos, indent=4)
    
    # abrindo o arquivo de banco de dados no modo escrita(W)
    with open(DB, "w") as arquivo:
        # escrevando o objeto json no arquivo
        arquivo.write(json_objeto)

        # retornado uma resposta para o frontend
        return Response(response=json.dumps(True), status=200,  mimetype="text/plain")
    
app.run(port=4000,host='localhost', debug=True)    