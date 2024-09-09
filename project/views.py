from project import app, db
from flask import Flask, request, jsonify, make_response
from project.models import User, Address
from project.__init__ import my_logger


@app.route('/test', methods=['GET']) # endpoint обрабатывает запрос на получение информации
def test():# тестовая функция
    return make_response(jsonify({'message': 'test route'}), 200) #


# create a user
@app.route('/users', methods=['POST']) # endpoint users
def create_user(): # функция размещает информацию о user
    try:
        data = request.get_json() # получает json файл из запроса
        new_user = User(username=data['username'], email=data['email']) # создаётся новый user(переменная new_user), используются предоставленные данные username, email
        db.session.add(new_user) # добавляется в сессию new_user
        db.session.commit() # коммит, добавляем изменения в базу данных
        my_logger.info('new user created')
        return make_response(jsonify({'message': 'user created'}), 201) # если создан новый user, ответ 201 - создан
    except Exception:
        my_logger.error('user not created, 500 error')
        return make_response(jsonify({'message': 'error creating user'}), 500) # 500 ошибка на стороне сервера,
        # return app.my_logger.error('user not created, 500 error')
    # return jsonify(users)


# get all users
@app.route('/users', methods=['GET'])
def get_users(): # функция возвращает информацию о всех пользователях
    try:
        users = User.query.all() # испльзуется модель User и метод query.all() для извлечения всех user в базе данных, переменная users
        return make_response(jsonify([user.json() for user in users]), 200) # для каждого user вызывается json(), получется список словарей, jsonify() преобразует в json файл
    except Exception:
        return make_response(jsonify({'message': 'error getting users'}), 500) # если информация не найдена ошибка сревера 500


# get user by id
@app.route('/users/<int:id>', methods=['GET']) # получаем информацию о user по id
def get_user(id):
    try:
        user = User.query.filter_by(id=id).first() # фильтруем user по id filter_by(), first() возвращает первого user, который подошёл по критерию
        if user: # если user найден
            return make_response(jsonify({'user': user.json()}), 200) # 200 - успешно отработан запрос, возвращает словарь user: вся информация о user из таблицы
        return make_response(jsonify({'message': 'user_not_found'}), 404) # ответ, если user не найден, 404 сервер не может найти данные
    except Exception:
        return make_response(jsonify({'message': 'error getting user'}), 500) #


# update a user
@app.route('/users/<int:id>', methods=['PUT']) # частично обновляем информацию о user по id
def update_user(id): # id может динамически изменяться в зависимости от запроса
    try:
        user = User.query.filter_by(id=id).first() # фильтруем user по id filter_by(), first() возвращает первого user, который подошёл по критерию
        if user: # если пользователь с этим id найден
            data = request.get_json() # получаем JSON из объекта запроса, сохраняем в переменную data
            user.username = data['username'] # обращаемся по ключу username в словаре  и добавляем в таблицу обновленные данные(колонку user.username)
            user.email = data['email'] # обращаемся по ключу email в словаре, добавляем обновленные данные
            db.session.commit() # сохраняем данные в таблицу
            my_logger.warning(f'the user with id: {id} updated')
            return make_response(jsonify({'message': "user updated"}), 200) # в случае успеха возаращаем файл json, 200 запрос успешно обработан
        my_logger.warning(f'user with id {id} not updated, not found')
        return make_response(jsonify({'message': 'user not found'}), 404) # 404 сервер не может найти данные согласно запросу
    except Exception:
        my_logger.error(f'error updating user with id: {id}')
        return make_response(jsonify({'message': 'error updating user'}), 500) # ошибка на стороне сервера


# delete a user
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id): # удаляем пользователя по id
    try:
        user = User.query.filter_by(id=id).first() # фильтруем user по id filter_by(), first() возвращает первого user, который подошёл по критерию
        if user: # если пользователь найден
            db.session.delete(user) # удаляем пользователя, сохраненного в переменную user
            db.session.commit() # сохраняем изменения в таблицу
            my_logger.warning(f'the user with id: {id} deleted')
            return make_response(jsonify({'message': 'user deleted'}), 200)
        my_logger.warning(f'the user with id: {id} not found')
        return make_response(jsonify({'message': 'user not found'}), 404)
    except Exception:
        return make_response(jsonify({'message': 'error deleting user'}), 500)


# creates new address in 'address'
# @app.route('/addresses/<int:id>', methods=['POST'])
# def create_address(id):
#     try:
#         data = request.get_json()
#         user = User.query.get_or_404(id, description='user not found')
#         address = Address(address=data['address'], user=user)
#         my_logger.info(str(address))
#         db.session.add(address)
#         db.session.commit()
#         return make_response(jsonify({'message': 'address created'}), 201)
#     except Exception as e:
#         my_logger.error(e)
#         return make_response(jsonify({'message': str(e)}), 500)


# gets email from the 'address'
@app.route('/users/<int:person_id>/addresses/<int:id>', methods=['GET'])
def get_address(person_id, id):
    try:
        address = Address.query.filter_by(person_id=person_id, id=id).first()
        if address:
            return make_response(jsonify({'message': address.json()}), 200)
        return make_response(jsonify({'message': 'address_not_found'}), 404)
    except Exception as e:
        my_logger.error(e)
        return make_response(jsonify({'message': 'error getting address'}), 500)


# updates email in the 'address'
@app.route('/users/<int:person_id>/addresses/<int:id>', methods=['PUT'])
def update_address(person_id, id):
    try:
        address = Address.query.filter_by(person_id=person_id, id=id).first()
        if address:
            data = request.get_json()  # получаем JSON из объекта запроса, сохраняем в переменную data
            address.address = data['address']
            db.session.commit()  # сохраняем данные в таблицу
            my_logger.warning(f'the users email with id: {person_id} updated')
            return make_response(jsonify({'message': address.json()}), 200)
        my_logger.warning(f'users email with id {person_id} not updated, not found')
        return make_response(jsonify({'message': f'users email with id {person_id} not updated, not found'}), 404)
    except Exception as e:
        my_logger.error(e)
        return make_response(jsonify({'message': 'error getting user/address'}), 500)

# deletes email from the 'address'
@app.route('/users/<int:person_id>/addresses/<int:id>', methods=['DELETE'])
def delete_address(person_id, id):
    try:
        address = Address.query.filter_by(person_id=person_id, id=id).first()
        if address:
            db.session.delete(address)  # удаляем address
            db.session.commit()  # сохраняем изменения в таблицу
            my_logger.warning(f'the address of the user with id: {person_id} deleted')
            return make_response(jsonify({'message': 'address deleted'}), 200)
        my_logger.warning(f'the address of the user with id: {person_id} not found')
        return make_response(jsonify({'message': f'user or address {person_id} or  {id} not found'}), 404)
    except Exception as e:
        my_logger.error(e)
        return make_response(jsonify({'message': 'error getting user/address'}), 500)

# adds new email in the 'address' to existing user
@app.route('/users/<int:person_id>/addresses', methods=['POST'])
def add_address(person_id): # функция размещает информацию о address
    try:
        data = request.get_json() # получает json файл из запроса
        new_address = Address(address=data['address'], person_id=data['person_id'])
        db.session.add(new_address)
        db.session.commit()
        my_logger.info(f'new address added to user with id {person_id}')
        return make_response(jsonify({'message': 'new address added'}), 201)
    except Exception as e:
        my_logger.error(e)
        return make_response(jsonify({'message': 'error creating address'}), 500)


# gets all emails of user from the 'address'
@app.route('/users/<int:person_id>/addresses', methods=['GET'])
def get_addresses(person_id):
    try:
        addresses = Address.query.filter_by(person_id=person_id).all()
        if addresses:
            return make_response(jsonify([address.json() for address in addresses]), 200) #jsonify([user.json() for user in users] jsonify({'message': address.json()}
        return make_response(jsonify({'message': 'person_not_found'}), 404)
    except Exception as e:
        my_logger.error(e)
        return make_response(jsonify({'message': 'error getting address'}), 500)


# deletes all emails of the user from the 'address'
@app.route('/users/<int:person_id>/addresses', methods=['DELETE'])
def delete_addresses(person_id):
    try:
        # addresses = Address.query.filter_by(person_id=person_id).all()
        # if addresses:
        db.session.query(Address).filter_by(person_id=person_id).delete()
        # db.session.delete(addresses)  # удаляем addresses
        db.session.commit()
        my_logger.warning(f'all addresses of the user with id: {person_id} deleted')
        return make_response(jsonify({'message': 'addresses deleted'}), 200)
        # my_logger.warning(f'addresses of the user with id: {person_id} not found')
        # return make_response(jsonify({'message': f'addresses of use with id: {person_id} not found'}), 404)
    except Exception as e:
        my_logger.error(e)
        return make_response(jsonify({'message': 'error getting user/addresses'}), 500)