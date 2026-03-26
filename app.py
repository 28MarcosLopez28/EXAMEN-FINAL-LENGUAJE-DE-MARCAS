from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def db():
    return sqlite3.connect("ex_final_ldm.db")

# ----------- INICIO -----------
@app.route("/")
def index():
    return render_template("index.html")

# ----------- LOGIN -----------
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        return redirect("/")
    return render_template("login.html")

# ----------- REGISTER -----------
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        nombre = request.form["nombre"]
        email = request.form["email"]
        password = request.form["password"]

        con = db()
        con.execute("INSERT INTO usuarios (nombre,email,password) VALUES (?,?,?)",
                    (nombre,email,password))
        con.commit()
        return redirect("/login")

    return render_template("register.html")

# ----------- HABITOS -----------
@app.route("/habitos", methods=["GET","POST"])
def habitos():
    con = db()

    if request.method == "POST":
        nombre = request.form["nombre"]
        con.execute("INSERT INTO habitos (nombre) VALUES (?)", (nombre,))
        con.commit()

    habitos = con.execute("SELECT * FROM habitos").fetchall()
    return render_template("habitos.html", habitos=habitos)

@app.route("/eliminar_habito/<int:id>")
def eliminar_habito(id):
    con = db()
    con.execute("DELETE FROM habitos WHERE id=?", (id,))
    con.commit()
    return redirect("/habitos")

# ----------- REGISTROS -----------
@app.route("/registros", methods=["GET","POST"])
def registros():
    con = db()

    if request.method == "POST":
        descripcion = request.form["descripcion"]
        con.execute("INSERT INTO registros (descripcion) VALUES (?)", (descripcion,))
        con.commit()

    registros = con.execute("SELECT * FROM registros").fetchall()
    return render_template("registros.html", registros=registros)

@app.route("/eliminar_registro/<int:id>")
def eliminar_registro(id):
    con = db()
    con.execute("DELETE FROM registros WHERE id=?", (id,))
    con.commit()
    return redirect("/registros")

app.run(debug=True)