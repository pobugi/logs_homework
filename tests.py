import os
import unittest
from app import app, db
from logs_api.merge_sort import merge_sort


class BasicTestCase(unittest.TestCase):

    mock_data = [
        {'name': 'Petya', 'age': 80}, 
        {'name': 'Vasya', 'age': 15}, 
        {'name': 'Kolya', 'age': 35}]

    # "mainpage is html/accessible"
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///logs_test.db'
        self.app = app.test_client()
        db.create_all()

    def test_main_page(self):
        """ensure that mainpage type is html/txt and it is accessible"""
        response = self.app.get('/', content_type='html/txt')
        self.assertEqual(response.status_code, 200)

    def test_database_exists(self):
        """ensure that the test database is created successfully"""
        result = os.path.isfile("logs_test.db")
        self.assertTrue(result)

    def test_sorting(self):
        """ensure that sorting function works correctly"""
        sorted_arr = merge_sort(self.mock_data, 'age')
        self.assertEqual(sorted_arr, [{'name': 'Vasya', 'age': 15}, {'name': 'Kolya', 'age': 35},
                                      {'name': 'Petya', 'age': 80}])

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        os.remove("logs_test.db")


if __name__ == "__main__":
    unittest.main()
