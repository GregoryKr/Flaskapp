import unittest
from project import app, db
from project.models import User, Address
import logging
import sys
from logging.handlers import TimedRotatingFileHandler

# FORMATTER = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s")
# LOG_FILE = "my_app1.log"
#
# def get_console_handler():
#    console_handler = logging.StreamHandler(sys.stdout)
#    console_handler.setFormatter(FORMATTER)
#    return console_handler
#
#
# def get_file_handler():
#    file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight')
#    file_handler.setFormatter(FORMATTER)
#    return file_handler
#
#
# def get_logger(logger_name):
#    logger = logging.getLogger(logger_name)
#    logger.setLevel(logging.DEBUG) # better to have too much log than not enough
#    logger.addHandler(get_console_handler())
#    logger.addHandler(get_file_handler())
#    # with this pattern, it's rarely necessary to propagate the error up to parent
#    logger.propagate = False
#    return logger
#
#
# my_logger = get_logger(__name__)

class ViewsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.app = app
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_users_get(self):
        admin = User(username='admin', email='admin@example.com')
        guest = User(username='guest', email='guest@example.com')
        db.session.add(admin)
        db.session.add(guest)
        db.session.commit()
        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json)
        self.assertEqual(2, len(response.json))
        self.assertEqual(response.json[0]['email'], 'admin@example.com')
        self.assertEqual(response.json[1]['email'], 'guest@example.com')
        # if response.json:
        #     try:
        #         self.assertEqual(response.status_code, 200)
        #         # print(response.json)
        #         self.assertEqual(response.json[0]['email'], 'admin@example.com')
        #         self.assertEqual(response.json[1]['email'], 'guest@example.com')
        #     except Exception as e:
        #         print(e, 'test_users_get')
        # else:
        #     print('there are no users in the database, test: test_users_get')

    def test_users_get_error(self):
        response = self.client.get('/users')
        print(response.json)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(0, len(response.json))
        self.assertFalse(response.json)

    def test_users_post(self):
        response = self.client.post('/users', json={
            'username': 'test',
            'email': 'test@example.ru'
        })
        user = User.query.filter_by(username='test').first()
        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(response.json)
        self.assertEqual(user.email, 'test@example.ru')

        # if response:
        #     try:
        #         self.assertEqual(response.status_code, 201)
        #         user = User.query.filter_by(username='test').first()
        #         self.assertEqual(user.email,'test@example.ru')
        #     except Exception as e:
        #         print(e, 'test_users_post')
        # else:
        #     print('there are no users in the database, test: test_users_post')

    def test_users_post_error(self):
        response = self.client.post('/users', json={
            'username': 'test',
            # 'email': 'test@example.ru'
        })
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json['message'], 'error creating user')

    def test_users_get_first(self):
        admin = User(username='admin', email='admin@example.com')
        db.session.add(admin)
        db.session.commit()
        response = self.client.get('/users/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['user']['email'], 'admin@example.com')
        self.assertEqual(1, len(response.json))
        # print(response.json)
        # if response.json:
        #     try:
        #         self.assertEqual(response.status_code, 200)
        #         self.assertEqual(response.json['user']['email'], 'admin@example.com')
        #
        #     except Exception as e:
        #         print(e, 'test_users_get_first')
        # else:
        #     print('there are no users in the database, test: test_users_get_first')

    def test_users_get_first_error404(self):
        admin = User(username='admin', email='admin@example.com')
        db.session.add(admin)
        db.session.commit()
        response = self.client.get('/users/2')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['message'], 'user_not_found')

    # def test_users_get_first_error500(self):
    #     admin = User(username='admin', email='admin@example.com')
    #     db.session.add(admin)
    #     db.session.commit()
    #     response = self.client.get('/users/2')
    #     self.assertEqual(response.status_code, 500)
    #     self.assertEqual(response.json['message'], 'error getting user')

    def test_users_put(self):
        admin = User(username='admin', email='admin@example.com')
        db.session.add(admin)
        db.session.commit()
        response = self.client.put('/users/1', json={
            'username': 'test1',
            'email': 'test1@example.ru'
        })
        self.assertEqual(response.status_code, 200)
        user = User.query.filter_by(username='test1').first()
        self.assertEqual(user.email, 'test1@example.ru')

        # if response:
        #     try:
        #         self.assertEqual(response.status_code, 200)
        #         user = User.query.filter_by(id=1).first()
        #         self.assertEqual(user.email, 'test1@example.ru')
        #     except Exception as e:
        #         print(e, 'test_users_post')
        # else:
        #     print('there are no such user in the database, test: test_users_put')

    def test_users_put_error404(self):
        admin = User(username='admin', email='dmin@example.com')
        db.session.add(admin)
        db.session.commit()
        response = self.client.put('/users/2', json={
            'username': 'test1',
            'email': 'test1@example.ru'
        })
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['message'], 'user not found')

    def test_users_delete_first(self):
        admin = User(username='admin', email='admin@example.com')
        db.session.add(admin)
        db.session.commit()
        response = self.client.delete('/users/1')
        self.assertEqual(response.status_code, 200)
        user = User.query.filter_by(id=1).first()
        self.assertEqual(user, None)
        # try:
        #     response = self.client.delete('/users/1')
        #     self.assertEqual(response.status_code, 200)
        #     user = User.query.filter_by(id=1).first()
        #     self.assertEqual(user, None)
        # except Exception as e:
        #     print(e, 'test_users_delete_first')

    def test_users_delete_first_error404(self):
        response = self.client.delete('/users/1')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['message'], 'user not found')

    # def test_address_post(self):
    #     response = self.client.post('/addresses/1', json={
    #         'address': 'test4@example.ru'
    #     })
    #     # print(response.json)
    #     self.assertEqual(response.status_code, 201)
    #     address = Address.query.filter_by(person_id=1).first()
    #     self.assertEqual(address.address, 'test4@example.ru')

    def test_address_get_by_id(self):
        admin1 = Address(person_id=1, address='admin2@example.com')
        db.session.add(admin1)
        db.session.commit()
        response = self.client.get('/users/1/addresses/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json["message"]['address'], 'admin2@example.com')

    def test_address_get_by_id_error404(self):
        admin1 = Address(person_id=1, address='admin2@example.com')
        db.session.add(admin1)
        db.session.commit()
        response = self.client.get('/users/1/addresses/2')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json["message"], 'address_not_found')

    def test_address_put_by_id(self):
        admin1 = Address(person_id=1, address='admin2@example.com')
        db.session.add(admin1)
        db.session.commit()
        response = self.client.put('/users/1/addresses/1', json={
            'address': 'test5@example.com'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"]['address'], 'test5@example.com')

    def test_address_put_by_id_error404(self):
        response = self.client.put('/users/1/addresses/1', json={
            'address': 'test5@example.com'
        })
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json["message"], 'users email with id 1 not updated, not found')

    def test_address_delete_by_id(self):
        admin1 = Address(person_id=1, address='admin2@example.com')
        db.session.add(admin1)
        db.session.commit()
        response = self.client.delete('/users/1/addresses/1')
        self.assertEqual(response.status_code, 200)
        address = Address.query.filter_by(person_id=1).first()
        self.assertEqual(address, None)

    def test_address_delete_by_id_error404_person_id(self):
        admin1 = Address(person_id=1, address='admin2@example.com')
        db.session.add(admin1)
        db.session.commit()
        response = self.client.delete('/users/2/addresses/1')
        self.assertEqual(response.status_code, 404)
        # address = Address.query.filter_by(person_id=2).first()
        self.assertEqual(response.json['message'], 'user or address 2 or  1 not found')

    def test_address_delete_by_id_error404_id(self):
        admin1 = Address(person_id=1, address='admin2@example.com')
        db.session.add(admin1)
        db.session.commit()
        response = self.client.delete('/users/1/addresses/2')
        self.assertEqual(response.status_code, 404)
        # address = Address.query.filter_by(person_id=2).first()
        self.assertEqual(response.json['message'], 'user or address 1 or  2 not found')

    def test_address_post_email_by_id(self):
        admin1 = Address(person_id=1, address='admin2@example.com')
        db.session.add(admin1)
        db.session.commit()
        response = self.client.post('/users/1/addresses', json={
            'person_id': 1,
            'address': 'test7@example.com'
        })
        self.assertEqual(response.status_code, 201)
        address = Address.query.filter_by(id=2).first()
        self.assertEqual(address.address, 'test7@example.com')
        # print(address.address)

    def test_address_post_email_by_id_error500(self):
        admin1 = Address(person_id=1, address='admin2@example.com')
        db.session.add(admin1)
        db.session.commit()
        response = self.client.post('/users/1/addresses', json={
            'person_id': 1,
            #'address': 'test7@example.com'
        })
        self.assertEqual(response.status_code, 500)
        # address = Address.query.filter_by(id=2).first()
        self.assertEqual(response.json['message'], 'error creating address')

    def test_address_get_all_emails(self):
        admin1 = Address(person_id=1, address='admin2@example.com')
        db.session.add(admin1)
        db.session.commit()
        email2 = Address(person_id=1, address='123@example.com')
        db.session.add(email2)
        db.session.commit()
        response = self.client.get('/users/1/addresses')
        # print(response.json)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]['address'], 'admin2@example.com')
        self.assertEqual(response.json[1]['address'], '123@example.com')

    def test_address_get_all_emails_error404(self):
        response = self.client.get('/users/1/addresses')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['message'], 'person_not_found')

    def test_address_all_addresses_delete_by_id(self):
        admin1 = Address(person_id=1, address='admin2@example.com')
        db.session.add(admin1)
        db.session.commit()
        email2 = Address(person_id=1, address='123@example.com')
        db.session.add(email2)
        db.session.commit()
        response = self.client.delete('/users/1/addresses')
        self.assertEqual(response.status_code, 200)
        address = Address.query.filter_by(person_id=1).first()
        self.assertEqual(address, None)

    def test_address_all_addresses_delete_by_id_error500(self):
        admin1 = Address(person_id=1, address='admin2@example.com')
        db.session.add(admin1)
        db.session.commit()
        response = self.client.delete('/users/2/addresses')
        self.assertEqual(response.status_code, 500)
        # address = Address.query.filter_by(person_id=1).first()
        self.assertEqual(response.json, 'error getting user/addresses')


if __name__ == '__main__':
    unittest.main()


