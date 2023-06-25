from flask import Flask, flash, redirect, render_template, request, session
from cs50 import SQL


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


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
def filosifia():
    return render_template("filosofia.html")

