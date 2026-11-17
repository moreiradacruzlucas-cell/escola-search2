
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configurações do Flask
app.secret_key = "chave-secreta-do-site"

# Configuração do banco de dados
os.makedirs(app.instance_path, exist_ok=True)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///escola.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# Modelo da tabela de editais
class Edital(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    ano = db.Column(db.Integer, nullable=True)
    arquivo = db.Column(db.String(255), nullable=True)


# Criar o banco e substituir os editais fictícios
with app.app_context():
    db.create_all()

    # Remover os três editais antigos
    Edital.query.delete()

    # Cadastrar os novos editais
    editais_iniciais = [
        Edital(
            titulo="PROCESSO DE SELEÇÃO DE DISCENTES E SERVIDORES PARA INTERCÂMBIO INTERNACIONAL NO CANADÁ 2026",
            descricao="Resultado da apuração.",
            ano=2026,
            arquivo="editais/edital1.pdf"
        ),
        Edital(
            titulo="SELEÇÃO INTERNA BANDA DO IFAP CAMPUS MACAPÁ",
            descricao="Abertura das inscrições no processo de seleção para provimento de vagas para as funções decoordenador da banda.",
            ano=2026,
            arquivo="editais/edital2.pdf"
        ),
        Edital(
            titulo="PROCESSO SELETIVO DISCENTE PARA INGRESSO NOS CURSOS TÉCNICOS DE NÍVEL MÉDIO",
            descricao="Processo Seletivo Discente (PSD) para preenchimento de vagas para ingresso nos cursos técnicos de nível médio na forma integrada/integral e modalidade presencial.",
            ano=2026,
            arquivo="editais/edital3.pdf"
        )
    ]

    db.session.add_all(editais_iniciais)
    db.session.commit()


# Página inicial
@app.route("/")
def inicio():
    if "nome" not in session:
        return redirect(url_for("entrada"))

    return render_template("Index.html", nome=session["nome"])


# Página de entrada
@app.route("/entrada", methods=["GET", "POST"])
def entrada():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()

        if nome:
            session["nome"] = nome
            return redirect(url_for("inicio"))

    return render_template("Entrada.html")


# Página Sobre
@app.route("/sobre")
def sobre():
    return render_template("Sobre.html")


# Página de Editais
@app.route("/editais")
def editais():
    pesquisa = request.args.get("pesquisa", "").strip()

    if pesquisa:
        resultados = Edital.query.filter(
            db.or_(
                Edital.titulo.ilike(f"%{pesquisa}%"),
                Edital.descricao.ilike(f"%{pesquisa}%")
            )
        ).order_by(Edital.id.desc()).all()
    else:
        resultados = Edital.query.order_by(Edital.id.desc()).all()

    return render_template(
        "Editais.html",
        editais=resultados,
        pesquisa=pesquisa
    )


# Página de Prazos
@app.route("/prazos")
def prazos():
    return render_template("Prazos.html")


# Página de Perguntas Frequentes
@app.route("/faq")
def faq():
    return render_template("FAQ.html")


# Página de Suporte
@app.route("/suporte")
def suporte():
    return render_template("Suporte.html")


# Executar o servidor
if __name__ == "__main__":
    app.run(debug=True)
