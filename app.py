from flask import Flask, flash, redirect, render_template, request, session
from cs50 import SQL


app = Flask(__name__)

# The server can be initialized with 'Flask.run()'.
# Debug mode can be activated with 'debug=True'.
# Apparently we can use 'port' to specify the port of the server


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/contato")
def materias():
    return render_template("contato.html")


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
