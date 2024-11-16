from flask import Flask, jsonify, request
from http import HTTPStatus

app = Flask(__name__)


books = [
    {"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "year": 1925},
    {"id": 2, "title": "1984", "author": "George Orwell", "year": 1949},
]


def find_book(book_id):
    for book in books:
        if book["id"] == book_id:
            return book
    return None

@app.route("/api/books", methods=["GET"])
def get_books():
    return jsonify({"success": True, "data": books, "total": len(books)}), HTTPStatus.OK

@app.route("/api/books/book_id", methods=["GET"])
def get_book(book_id):
    
    book = find_book(book_id)

    if book is None:
        return (
            jsonify({
                "success": False,
                "error": "Book not found"
            }),
            HTTPStatus.NOT_FOUND
        )

    return jsonify({"success": True, "data": book}), HTTPStatus.OK

@app.route("/api/books", methods=["POST"])
def create_book():
    if not request.is_json:
        return (
            jsonify({
                "success": False,
                "error": "Content-type must be application/json"
            }),
            HTTPStatus.BAD_REQUEST
        )

    data = request.get_json()

    required_fields = ["title", "author", "year"]
    for field in required_fields:
        if field not in data:
            return jsonify({
                "success": False,
                "error": f"Missing required field: {field}"
            }), HTTPStatus.BAD_REQUEST

    new_book = {
        "id": max(book['id'] for book in books) + 1,  # Generate a new ID
        "title": data["title"],
        "author": data["author"],
        "year": data["year"]
    }

    books.append(new_book)

    return jsonify({
        "success": True,
        "data": new_book
    }), HTTPStatus.CREATED

if __name__ == "__main__":
    app.run(debug=True)