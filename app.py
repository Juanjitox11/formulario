from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Crear la base de datos y tabla si no existe
def init_db():
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT NOT NULL,
            telefono TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        nombre = request.form["nombre"]
        email = request.form["email"]
        telefono = request.form["telefono"]

        conn = sqlite3.connect("usuarios.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (nombre, email, telefono) VALUES (?, ?, ?)",
                       (nombre, email, telefono))
        conn.commit()
        conn.close()
        return redirect("/")

    # Consultar usuarios
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    conn.close()

    return render_template("index.html", usuarios=usuarios)

if __name__ == "__main__":
    app.run(debug=True)
