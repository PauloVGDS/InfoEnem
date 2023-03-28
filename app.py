from flask import Flask, flash, redirect, render_template, request, session
from cs50 import SQL


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/knowledge")
def knowledge():
    return render_template("knowledge.html")


@app.route("/projects")
def projects():
    return render_template("projects.html")



@app.route("/contacts")
def contacts():
    return render_template("contacts.html")

