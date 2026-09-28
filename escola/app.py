from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

app.secret_key = "chave-secreta-do-site"

editais_lista = [
    {
        "titulo": "Edital de Matrícula 2026",
        "descricao": "Informações sobre matrícula escolar para o ano de 2026."
    },
    {
        "titulo": "Edital de Transferência Escolar",
        "descricao": "Informações sobre transferência de alunos."
    },
    {
        "titulo": "Edital de Vagas Remanescentes",
        "descricao": "Lista de vagas disponíveis nas escolas."
    }
]


@app.route("/")
def inicio():
    if "nome" not in session:
        return redirect(url_for("entrada"))

    return render_template("index.html", nome=session["nome"])


@app.route("/entrada", methods=["GET", "POST"])
def entrada():
    if request.method == "POST":
        nome = request.form["nome"]
        session["nome"] = nome
        return redirect(url_for("inicio"))

    return render_template("entrada.html")


@app.route("/sobre")
def sobre():
    return render_template("sobre.html")


@app.route("/editais")
def editais():
    pesquisa = request.args.get("pesquisa", "")

    resultados = []

    for edital in editais_lista:
        if (
            pesquisa.lower() in edital["titulo"].lower()
            or pesquisa.lower() in edital["descricao"].lower()
        ):
            resultados.append(edital)

    return render_template(
        "editais.html",
        editais=resultados,
        pesquisa=pesquisa
    )


@app.route("/prazos")
def prazos():
    return render_template("prazos.html")


@app.route("/faq")
def faq():
    return render_template("faq.html")


@app.route("/suporte")
def suporte():
    return render_template("suporte.html")


if __name__ == "__main__":
    app.run(debug=True)