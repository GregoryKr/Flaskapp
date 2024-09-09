from project import app, db

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)


# users = [
#     {"id": 1, "username": "Andrey", "email": "123@mail.ru"},
#     {"id": 2, "username": "Sergey", "email": "321@google.com"},
#     {"id": 3, "username": "Egor", "email": "231@yandex.ru"},
# ]


# def find_next_id():
#     return max(user["id"] for user in users) + 1






