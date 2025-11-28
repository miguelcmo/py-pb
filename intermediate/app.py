from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Datos simulados en memoria
books = [
    {"id": 1, "title": "Clean Code", "author": "Robert C. Martin"},
    {"id": 2, "title": "Fluent Python", "author": "Luciano Ramalho"},
    {"id": 3, "title": "The Pragmatic Programmer", "author": "Andrew Hunt"},
]

loans = []  # cada elemento será {"book": {...}, "borrower": "Nombre"}

@app.route("/")
def index():
    return render_template("index.html", books=books)

@app.route("/borrow/<int:book_id>", methods=["GET", "POST"])
def borrow(book_id):
    # Buscar libro
    book = next((b for b in books if b["id"] == book_id), None)
    if not book:
        return "Book not found", 404

    if request.method == "POST":
        borrower = request.form.get("borrower")
        if borrower:
            loans.append({"book": book, "borrower": borrower})
            return redirect(url_for("show_loans"))

    return render_template("borrow.html", book=book)

@app.route("/loans")
def show_loans():
    return render_template("loans.html", loans=loans)

if __name__ == "__main__":
    app.run(debug=True)
