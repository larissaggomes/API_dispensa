import json

produto2 ={
        "id": 1,
        "nome": "leite desnatado",
        "preco": 32
    }

def ler():
    try:
        with open("teste.json", "r") as arquivo:
            json_objeto = json.load(arquivo)
        return json_objeto
    except IOError:
        return []   

def ler_id(id):
    resultado = ler()
    for produto in resultado:
        if produto["id"] == id:
            return produto    

def escrever(produto):
    #resultado recebe uma lista de produto ou uma lista vazia
    resultado = ler()
    #no append estou adicionado um novo item
    resultado.append(produto)

    #serializando o json(convetendo a varivel em texto)
    json_objeto = json.dumps(resultado, indent=4)
    
    #escrevendo no arquivo teste.json
    with open("teste.json", "w") as arquivo:
        arquivo.write(json_objeto)

def editar(id,data):
    resultado = ler()
    for produto in resultado:
        if produto["id"] == id:
           produto["nome"] = data["nome"]
           produto["preco"] = data["preco"]

    json_objeto = json.dumps(resultado, indent=4)
    with open("teste.json", "w") as arquivo:
        arquivo.write(json_objeto)

def deletar(id):
    resultado = ler()
    modificado = []
    for produto in resultado:
        if produto["id"] != id:
            modificado.append(produto)

    json_objeto = json.dumps(modificado, indent=4)
    with open("teste.json", "w") as arquivo:
        arquivo.write(json_objeto)    

# escrever(produto=produto2)
# print(ler())
# editar(id=1,data=produto2)
# deletar(id=8)
# print(ler_id(id=1))