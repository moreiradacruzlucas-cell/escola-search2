from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

app.secret_key = "chave-secreta-do-site"


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


if __name__ == "__main__":
    app.run(debug=True)
