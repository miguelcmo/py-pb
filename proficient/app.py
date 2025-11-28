from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "secret-key-demo"   # Solo para pruebas

# Usuarios simulados
users = {
    "admin": "1234"
}

# Datos simulados en memoria
books = [
    {"id": 1, "title": "Clean Code", "author": "Robert C. Martin"},
    {"id": 2, "title": "Fluent Python", "author": "Luciano Ramalho"},
    {"id": 3, "title": "The Pragmatic Programmer", "author": "Andrew Hunt"},
]

loans = []   # cada elemento: {"book": {...}, "borrower": "Nombre"}

# ----------------------------- Helpers -------------------------------- #

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
    return render_template("index.html", books=books)

# ------------------------------ Login --------------------------------- #

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username] == password:
            session["user"] = username
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Credenciales inválidas")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# -------------------------- Agregar libros ----------------------------- #

@app.route("/add", methods=["GET", "POST"])
@login_required
def add_book():
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]

        new_id = max([b["id"] for b in books]) + 1 if books else 1
        books.append({"id": new_id, "title": title, "author": author})

        return redirect(url_for("index"))

    return render_template("add_book.html")

# ----------------------------- Prestar -------------------------------- #

@app.route("/borrow/<int:book_id>", methods=["GET", "POST"])
@login_required
def borrow(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if not book:
        return "Book not found", 404

    # Si ya está prestado, no se puede prestar de nuevo
    for loan in loans:
        if loan["book"]["id"] == book_id:
            return "Este libro ya está prestado.", 400

    if request.method == "POST":
        borrower = request.form.get("borrower")
        loans.append({"book": book, "borrower": borrower})
        return redirect(url_for("show_loans"))

    return render_template("borrow.html", book=book)

# --------------------------- Listar/Devolver --------------------------- #

@app.route("/loans")
@login_required
def show_loans():
    return render_template("loans.html", loans=loans)

@app.route("/return/<int:book_id>")
@login_required
def return_book(book_id):
    global loans
    loans = [loan for loan in loans if loan["book"]["id"] != book_id]
    return redirect(url_for("show_loans"))

# ------------------------------ Run ----------------------------------- #

if __name__ == "__main__":
    app.run(debug=True)
