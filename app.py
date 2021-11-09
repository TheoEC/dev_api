from flask import Flask, request
from flask_restful import Resource, Api
from models import Pessoas, Atividade, Administradores
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
app = Flask(__name__)
api = Api(app)

# Administradores = {
#     "Rafael" : "123",
#     "Galleani" : "321"
# }

# @auth.verify_password
# def verificacao(login, senha):
#     print("Validando o usuário")
#     if not (login, senha):
#         return False
#     else:
#         return Administradores.get(login) == senha

@auth.verify_password
def verificacao(login, senha):
    print("Validando o usuário: " + login, senha)
    if not (login, senha):
        return False
    else:
        return Administradores.query.filter_by(login = login, senha = senha).first()

class Pessoa(Resource):
    # Retorna os dados do primeiro objeto com o nome informado
    @auth.login_required
    def get(self, nome):
        try:
            pessoa = Pessoas.query.filter_by(nome=nome).first()
            response = {
                "nome:":  pessoa.nome,
                "idade:": pessoa.idade,
                "id":     pessoa.id
            }
        except:
            response = "Tem não"
        return response

    # Altera os dados do primeiro objeto com o nome informado
    @auth.login_required
    def put(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        dados = request.get_json()
        print("DADOS: ", dados)
        if ("nome" in dados):
            pessoa.nome = dados["nome"]
        if "idade" in dados:
            pessoa.idade = dados["idade"]
        pessoa.save()
        response = {
                "nome:":  pessoa.nome,
                "idade:": pessoa.idade,
                "id":     pessoa.id
            }
        return response
    
    # Delete o primeiro objeto com o nome informado
    @auth.login_required
    def delete(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        pessoa.delete()
        return {"status": "sucesso"}

class ListaPessoas(Resource):
    @auth.login_required
    def get(self):
        pessoas = Pessoas.query.all()
        response = [p.get_json() for p in pessoas]
        return response

class AddPessoas(Resource):
    @auth.login_required
    def post(self):
        dados = request.get_json()
        pessoa = Pessoas(nome = dados["nome"], idade = dados["idade"])
        pessoa.save()
        return pessoa.get_json()

class ListaAtividades(Resource):
    # Retorna todos as atividades
    @auth.login_required
    def get(self):
        atividades = Atividade.query.all()
        response = [a.get_json() for a in atividades]
        return response
    
    # Delete o primeiro objeto com o id informado
    @auth.login_required
    def delete(self):
        try:
            dados = request.get_json()
            atividade = Atividade.query.filter_by(id = dados["id"]).first()
            atividade.delete()
            response = {"status": "sucesso"}
        except:
            response = {"status": "Atividade inexistente"}
        return response

class AddAtividade(Resource):
    @auth.login_required
    def post(self):
        try:
            dados = request.get_json()
            usuario = Pessoas.query.filter_by(nome = dados["usuario"]).first()
            atividade = Atividade(nome = dados["nomeAtividade"], pessoa = usuario)
            response = atividade.get_json()
            atividade.save()
            if (response["id"] == None):
                response = atividade.get_json()
        except:
            response = {"status": "usuario inexistente"}
        return response

api.add_resource(AddPessoas, "/pessoa/add")
api.add_resource(ListaPessoas, "/pessoa/list")
api.add_resource(Pessoa, "/pessoa/<string:nome>")

api.add_resource(AddAtividade, "/atividade/add")
api.add_resource(ListaAtividades, "/atividade/list")

if __name__ == "__main__":
    app.run(debug=True)