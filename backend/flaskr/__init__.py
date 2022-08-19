import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy  # , or_
from flask_cors import CORS
import random

from models import setup_db, Book

BOOKS_PER_SHELF = 8

def paginate_books(request, selection):
    page = request.args.get('page', 1, type=int)
    start =  (page - 1) * BOOKS_PER_SHELF
    end = start + BOOKS_PER_SHELF

    books = [book.format() for book in selection]
    current_books = books[start:end]

    return current_books

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
        books = paginate_books(request, Book.query.order_by(Book.id).all())
        if len(books) == 0:
            abort(404)
        
        total_books = Book.query.count()
        print(total_books, books)
        return jsonify({
            'success': True,
            'books': [book for book in books],
            'total_books': total_books
        })
    @app.route("/books/<int:id>", methods=['GET'])
    def get_book_by_id(id):
        book = Book.query.get(id)
        if book is None:
            abort(404)

        return jsonify({
            'success': True,
            'book': book.format()
        })
        
    @app.route("/books/<int:book_id>", methods=['PATCH'])
    def update_book_rating(book_id):
            try:
                body =request.get_json()
                print(body)
                if body is None:
                    abort(400)
                book = Book.query.get(book_id)
                if book is None:
                    abort(404)
                if 'rating' in body:
                    book.rating = int(body.get('rating'))
                if 'author' in body:
                    book.author = body.get('author')
                if 'title' in body:
                    book.title = body.get('title')
                book.update()
                print(book.format())
                return jsonify({
                    'success': True
                })
            except:
                abort(400)
    
    @app.route("/books/<int:book_id>", methods=['DELETE'])
    def delete_book(book_id):
        try:
            
            book = Book.query.get(book_id)
            if book is None:
                abort(422)
            book.delete()
            return jsonify({
                'success': True,
                'deleted': book_id,
                'books': [book.format() for book in Book.query.all()],
                'total_books': Book.query.count()
            })
        except:
            abort(404)
   
    @app.route('/books', methods=['POST'])
    def create_book():
            try:
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
            except Exception as e:
                abort(422)
            
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False, 
            "error": 404,
            "message": "Not found"
            }), 404
        
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
        "success": False, 
        "error": 422,
        "message": "unprocessable"
        }), 422
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
        "success": False, 
        "error": 400,
        "message": "bad request"
        }), 400
        
    @app.errorhandler(403)
    def bad_request(error):
        return jsonify({
        "success": False, 
        "error": 403,
        "message": "unprocessable"
        }), 403
    return app
