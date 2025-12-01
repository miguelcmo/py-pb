import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "secret-key-demo"

DB = "library.db"

# ------------------------------ Helpers DB ---------------------------- #

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

# ------------------------------ Auth --------------------------------- #

def login_required(func):
    def wrapper(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("login"))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

# ------------------------------ Rutas --------------------------------- #

@app.route("/")
@login_required
def index():
    conn = get_db()
    books = conn.execute("SELECT * FROM books").fetchall()
    conn.close()
    return render_template("index.html", books=books)

# ------------------------------ Login --------------------------------- #

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        ).fetchone()
        conn.close()

        if user:
            session["user"] = username
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Credenciales inválidas")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ---------------------------- Agregar libros --------------------------- #

@app.route("/add", methods=["GET", "POST"])
@login_required
def add_book():
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]

        conn = get_db()
        conn.execute(
            "INSERT INTO books (title, author) VALUES (?, ?)",
            (title, author)
        )
        conn.commit()
        conn.close()

        return redirect(url_for("index"))

    return render_template("add_book.html")

# ----------------------------- Prestar -------------------------------- #

@app.route("/borrow/<int:book_id>", methods=["GET", "POST"])
@login_required
def borrow(book_id):
    conn = get_db()
    book = conn.execute("SELECT * FROM books WHERE id=?", (book_id,)).fetchone()

    if not book:
        return "Libro no encontrado", 404

    # Validar si ya está prestado
    existing = conn.execute(
        "SELECT * FROM loans WHERE book_id=?",
        (book_id,)
    ).fetchone()

    if existing:
        conn.close()
        return "Este libro ya está prestado.", 400

    if request.method == "POST":
        borrower = request.form["borrower"]

        conn.execute(
            "INSERT INTO loans (book_id, borrower) VALUES (?, ?)",
            (book_id, borrower)
        )
        conn.commit()
        conn.close()
        return redirect(url_for("show_loans"))

    conn.close()
    return render_template("borrow.html", book=book)

# ---------------------- Mostrar y devolver préstamos ------------------- #

@app.route("/loans")
@login_required
def show_loans():
    conn = get_db()
    rows = conn.execute("""
        SELECT 
            loans.id AS loan_id,
            loans.borrower,
            books.id AS book_id,
            books.title AS book_title
        FROM loans
        JOIN books ON loans.book_id = books.id
    """).fetchall()
    conn.close()

    # Transformación a estructuras anidadas para Jinja
    loans = []
    for row in rows:
        loans.append({
            "id": row["loan_id"],
            "borrower": row["borrower"],
            "book": {
                "id": row["book_id"],
                "title": row["book_title"]
            }
        })

    return render_template("loans.html", loans=loans)

@app.route("/return/<int:book_id>")
@login_required
def return_book(book_id):
    conn = get_db()
    conn.execute("DELETE FROM loans WHERE book_id=?", (book_id,))
    conn.commit()
    conn.close()

    return redirect(url_for("show_loans"))

# ------------------------------- RUN ---------------------------------- #

if __name__ == "__main__":
    app.run(debug=True)
