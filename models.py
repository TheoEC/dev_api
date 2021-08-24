from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import  scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
import os

engine = create_engine("sqlite:///DIO/avancedPyRest/api_atividade/atividades.db")
db_session = scoped_session(sessionmaker(autocommit=False, 
                                        bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

class Pessoas(Base):
    __tablename__ = "pessoas"
    id = Column(Integer, primary_key=True)
    nome = Column(String(40), index=True)
    idade = Column(Integer)

    #__repr__ retorna o que deve ser 'printado' no print(Object) desta classe
    def __repr__(self):
        return "<Pessoa {}: {}>".format(self.nome, self.idade)
    
    #Salva o objeto desta classe no DB
    def save(self):
        db_session.add(self)
        db_session.commit()
    
    #Deleta este objeto no BD
    def delete(self):
        db_session.delete(self)
        db_session.commit()

    #Retorna o json deste objeto
    def get_json(self):
        dado = {
            "nome":  self.nome,
            "idade": self.idade,
            "id":    self.id
        }
        return dado

class Atividade(Base):
    __tablename__ = "atividades"
    id = Column(Integer, primary_key=True)
    nome = Column(String(80))
    pessoa_id = Column(Integer, ForeignKey("pessoas.id"))
    pessoa = relationship("Pessoas")

    def get_json(self):
        dado = {
            "Usuario" : self.pessoa.nome,
            "Nome"    : self.nome,
            "id"      : self.id
        }
        return dado
    
    #Salva o objeto desta classe no DB
    def save(self):
        db_session.add(self)
        db_session.commit()
    
    #Deleta este objeto no BD
    def delete(self):
        db_session.delete(self)
        db_session.commit()

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()