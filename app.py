from flask import Flask, render_template, request, redirect
from cs50 import SQL



app = Flask(__name__)


# The server can be initialized with 'Flask.run()'.
# Debug mode can be activated with 'debug=True'.
# Apparently we can use 'port' to specify the port of the server
db = SQL("sqlite:///registers.db")


def insertData(nome, sexo, idade, email, telefone, msg):
    try: 
        db.execute("INSERT INTO registros (Nome, Idade, Sexo, Email, Mensagem, Telefone) VALUES (?, ?, ?, ?, ?, ?)", nome, idade, sexo, email, msg, telefone);
    
    except Exception as e:
        return print(f"Erro: {e}")
    
        

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/contato", methods=['GET', 'POST']) # type: ignore
def materias():
    if request.method == "GET":
        return render_template("contato.html")
    else:

        insertData(
                nome=request.form.get("nome"),
                sexo=request.form.get("sexo"),
                idade = request.form.get("idade"),
                email = request.form.get("email"),
                telefone = request.form.get("telefone"),
                msg = request.form.get("mensagem")
            )
        return redirect("#")


@app.route("/sobre")
def sobre():
    return render_template("sobre.html")


@app.route("/matematica")
def matematica():
    return render_template("matematica.html")


@app.route("/portugues")
def portugues():
    return render_template("portugues.html")


@app.route("/geografia")
def geografia():
    return render_template("geografia.html")


@app.route("/historia")
def historia():
    return render_template("historia.html")


@app.route("/fisica")
def fisica():
    return render_template("fisica.html")


@app.route("/quimica")
def quimica():
    return render_template("quimica.html")


@app.route("/biologia")
def biologia():
    return render_template("biologia.html")


@app.route("/sociologia")
def sociologia():
    return render_template("sociologia.html")


@app.route("/filosofia")
def filosofia():
    return render_template("filosofia.html")


@app.route("/artes")
def artes():
    return render_template("artes.html")

@app.route("/ingles")
def ingles():
    return render_template("ingles.html")