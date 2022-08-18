import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy  # , or_
from flask_cors import CORS
import random

from models import setup_db, Book

BOOKS_PER_SHELF = 8



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    
    @app.route("/books")
    def get_all_books():
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * BOOKS_PER_SHELF
        end = start + BOOKS_PER_SHELF

        books = Book.query.all()[start:end]
        total_books = Book.query.count()
        return jsonify({
            'success': True,
            'books': [book.format() for book in books],
            'total_books': total_books
        })
    @app.route("/books/<int:book_id>", methods=['PATCH'])
    def update_book_rating(book_id, rating):
        book = Book.query.get(book_id)
        book.rating = rating
        book.update()
        return jsonify({
            'success': True
        })
    
    @app.route("/books/<int:book_id>", methods=['DELETE'])
    def delete_book(book_id):
        book = Book.query.get(book_id)
        book.delete()
        return jsonify({
            'success': True,
            'deleted': book_id,
            'books': [book.format() for book in Book.query.all()],
            'total_books': Book.query.count()
        })
   
    @app.route('/books', methods=['POST'])
    def create_book():
        title = request.json.get('title', None)
        author = request.json.get('author', None)
        rating = request.json.get('rating', None)
        book = Book(title=title, author=author, rating=rating)
        book.insert()
        return jsonify({
            'success': True,
            'created': book.id,
            'books': [book.format() for book in Book.query.all()],
            'total_books': Book.query.count()
        })
  
    return app
