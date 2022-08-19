#Import all dependencies
from re import S
from flask_sqlalchemy import SQLAlchemy
import unittest
import json
from flaskr import create_app
from models import setup_db, Book

class BookshelfTestCase(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "test_db"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            "student", "student", "localhost:5432", self.database_name
        )
        setup_db(self.app, self.database_path)
        
     
        self.new_book = {
            'title': 'test',
            'author': 'test',
            'rating': 4
        }
        
         # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
       
    def tearDown(self):
        """Executed after each test"""
        pass
    
    def test_create_book(self):
        """Test create book"""
        res = self.client().post('/books', json=self.new_book)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.content_type, 'application/json')
        self.assertEqual(res.json['success'], True)
        self.assertTrue(res.json['created'])
        self.assertTrue(len(res.json['books']))
        
    def test_get_all_books(self):
        """Test get all books """
        res = self.client().get('/books')

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.content_type, 'application/json')
        self.assertEqual(res.json['success'], True)
        self.assertTrue(len(res.json['books']))
        
    def test_paginated_books(self):
        """Test paginated books"""
        res = self.client().get('/books')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.content_type, 'application/json')
        self.assertEqual(res.json['success'], True)
        self.assertTrue(res.json['total_books'])
        self.assertTrue(len(res.json['books']))
        
    def test_get_book_by_id(self):
        """Test get book by id"""
        res = self.client().get('/books/3')
        data = json.loads(res.data)
        print(data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json['success'], True)
        
    def test_delete_book(self):
        """Test delete book"""
        res = self.client().delete('/books/20')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.content_type, 'application/json')
        self.assertEqual(res.json['success'], True)
        self.assertEqual(res.json['deleted'], 20)
      
        
    def test_400_for_failed_update(self):
        """Test update book with bad data"""
        res = self.client().patch('/books/5')
        self.assertEqual(res.status_code, 400)
        # data = json.loads(res.data)
        self.assertEqual(res.get_json()['success'], False)
        self.assertEqual(res.get_json()['message'], 'bad request')
        
    def test_404_if_book_not_found(self):
        res = self.client().delete('/books/1000')
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.content_type, 'application/json')
        self.assertEqual(res.json['success'], False)
        self.assertEqual(res.json['message'], 'Not found')
        
    # def test_404_sent_requesting_beyond_valid_page(self):
    #     data = self.client().get('/books?page=1')
    #     self.assertEqual(data.status_code, 404)
    #     self.assertEqual(data.content_type, 'application/json')
    #     self.assertEqual(data.json['success'], False)
    #     self.assertEqual(data.json['message'], 'Not found')
        
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()