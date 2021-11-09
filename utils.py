from models import Pessoas, db_session, Administradores

def insere_pessoas():
    pessoa = Pessoas(nome = "Caio", idade = 25)
    try:
        pessoa.save()
    except:
        print("DB Communication Error!")

def consulta_pessoas():
    pessoa = Pessoas.query.all()
    print(pessoa)
    # pessoa = Pessoas.query.filter_by(nome="Rafael")[0]
    # print(pessoa)

def altera_pessoa():
    pessoa = Pessoas.query.filter_by(nome="Rafael")[0]
    pessoa.idade = 22
    pessoa.save()

def exclui_pessoa():
    pessoa = Pessoas.query.filter_by(nome="Rafael")[0]
    pessoa.delete()

def insere_administrador(login, senha):
    admin = Administradores(login = login, senha = senha)
    admin.save()

def consulta_admin():
    admins = Administradores.query.all()
    print(admins)

if __name__ == "__main__":
    consulta_admin()
    insere_administrador("Rafael", "123")
    consulta_admin()