"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from api.models import db, User, People, Planets, Vehicles, UserFavorites
from api.utils import generate_sitemap, APIException
from flask_cors import CORS

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

#  Login, Access Token, Protected y JWT Requiered ----------------------------------------------------

@api.route('/login', methods=['POST'])
def login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    # Aquí deberías validar contra tu base de datos
    users_query = User.query.filter_by(email=email, password=password).first()
    if email != users_query.email or password != users_query.password:
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token), 200

@api.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user()), 200

    
# USER-----------------------------------------------------------------------------------------------

#Create a User
@api.route('/user', methods=['POST'])
def create_user():
    # Process the information coming from the client
    user_data = request.get_json()

    # We create an instance without being recorded in the database
    user = User()
    user.firstName = user_data["firstName"]
    user.lastName = user_data["lastName"]
    user.email = user_data["email"]

    if not (user.name and user.last_name and user.email):
        return jsonify({'message': 'All fields are required'}), 400

    return jsonify({'message': 'User registered successfully'}), 201


#Get all users
@api.route('/users', methods=['GET'])
def get_users():
    #access all registered users
    users_querys = User.query.all()
    #map users to convert into an array and return an array of objects
    results = list(map(lambda user: user.serialize(), users_querys))

    #is users empty, returns error code
    if results == []:
        return jsonify({"msg": "No registered users"}), 404
    
    #display results of access
    response_body = {
        "msg": "These are the registered users", 
        "results": results
    }
    return jsonify(response_body), 200

#DGet user by id
@api.route('/users/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    #filter all users by id
    user_query = User.query.filter_by(user = user_id).first()

    if user_query is None:
        return jsonify({"msg": "User with id: " + str(user_id) + " doesn't exist"}), 404
    
    response_body = {
        "msg": "User is", 
        "result": user_query.serialize()
    }

    return jsonify(response_body), 200

#Returns ALL People
@api.route('/people', methods=['GET'])
def get_people():
    people_querys = People.query.all()
    results = list(map(lambda people: people.serialize(), people_querys))
    
    if results == []:
        return jsonify({"msg": "No hay personajes registrados"}), 404
    
    response_body = {
        "msg": "Hola, estos son los personajes", 
        "results": results
    }

    return jsonify(response_body), 200

#Return Person by id
@api.route('/people/<int:people_id>', methods=['GET'])
def get_one_person(people_id):
    person_query = People.query.filter_by(id = people_id).first()

    if person_query is None:
        return jsonify({"msg": "Person with id: " + str(people_id) + " doesn't exist"}), 404
    
    response_body = {
        "msg": "Person is:", 
        "result": person_query.serialize()
    }

    return jsonify(response_body), 200

#Return ALL Planets
@api.route('/planets', methods=['GET'])
def get_planets():
    planets_querys = Planets.query.all()
    results = list(map(lambda planet: planet.serialize(), planets_querys))

    if results == []:
        return jsonify({"msg": "No Planets registered"}), 404
    
    response_body = {
        "msg": "These are the Planets", 
        "results": results
    }

    return jsonify(response_body), 200

#Return Planet by id
@api.route('/planets/<int:planet_id>', methods=['GET'])
def get_one_planet(planet_id):
    planet_query = Planets.query.filter_by(id = planet_id).first()

    if planet_query is None:
        return jsonify({"msg": "Planet with id: " + str(planet_id) + " doesn't exist"}), 404
    
    response_body = {
        "msg": "Planet is:", 
        "result": planet_query.serialize()
    }

    return jsonify(response_body), 200

#Returns ALL Vehicles
@api.route('/vehicles', methods=['GET'])
def get_vehicles():
    vehicles_querys = Vehicles.query.all()
    results = list(map(lambda vehicle: vehicle.serialize(), vehicles_querys))

    if results == []:
        return jsonify({"msg": "No Vehicles regstered"}), 404
    
    response_body = {
        "msg": "These are the Vehicles", 
        "results": results
    }

    return jsonify(response_body), 200

#returns Vehicle by id
@api.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_one_vehicle(vehicle_id):
    vehicle_query = Vehicles.query.filter_by(id = vehicle_id).first()

    if vehicle_query is None:
        return jsonify({"msg": "Vehicle with id: " + str(vehicle_id) + " doesn't exist"}), 404
    
    response_body = {
        "msg": "This is the Vehicle", 
        "result": vehicle_query.serialize()
    }

    return jsonify(response_body), 200

#Returns ALL User Favorites
@api.route('/users/<int:id>/fav', methods=['GET'])
def get_user_fav(id):
    favs_querys = UserFavorites.query.filter_by(user_id = id)
    results = list(map(lambda fav: fav.serialize(), favs_querys))
    user_query = User.query.filter_by(id = id).first()
    if user_query is None:
        return jsonify({"msg": "User isn't registered"}), 404
    if results == []:
        return jsonify({"msg": "No Favoritos registered"}), 404
    
    response_body = {
        "msg": "These are the User Favorites", 
        "results": results
    }

    return jsonify(response_body), 200

#Add a Planet to User Favorites
@api.route('/fav/planets/<int:planeta_id>', methods=['POST'])
def add_planet_fav(planet_id):
    
    request_body = request.get_json(force=True)

    user_query = User.query.filter_by(id = request_body["user_id"]).first()
    if user_query is None:
        return jsonify({"msg": "User isn't registered"}), 404
    
    planet_query = Planets.query.filter_by(id = planet_id).first()
    if planet_query is None:
        return jsonify({"msg": "Planeta doesn't exist"}), 404
    
    fav = UserFavorites.query.filter_by(user_id = request_body["user_id"]).filter_by(planets_id = planet_id).first() 
    if fav: 
        return jsonify({"msg": "Planet is already a favorite"}), 404
    
    new_planet_fav = UserFavorites(user_id = request_body["user_id"], planets_id = planet_id)
    db.session.add(new_planet_fav)
    db.session.commit()

    request_body = {
        "msg": "Planet added as favorite"
    }
    return jsonify(request_body), 200

#Delete Planet from User Favorites
@api.route('/fav/planets/<int:planeta_id>', methods=['DELETE'])
def delete_planet_fav(planet_id):
    
    request_body = request.get_json(force=True)

    user_query = User.query.filter_by(id = request_body["user_id"]).first()
    if user_query is None:
        return jsonify({"msg": "User isn't registered"}), 404
    
    planet_query = Planets.query.filter_by(id = planet_id).first()
    if planet_query is None:
        return jsonify({"msg": "Planet trying to delete doesn't exist"}), 404
    
    fav = UserFavorites.query.filter_by(user_id = request_body["user_id"]).filter_by(planets_id = planet_id).first()
    if fav is None:
        return jsonify({"msg": "Planet trying to delete isn't a favorite"}), 404

    db.session.delete(fav)
    db.session.commit()

    request_body = {
        "msg": "Planet deleted from favorites"
    }
    return jsonify(request_body), 200

#Add a Person to User Favorites
@api.route('/fav/people/<int:person_id>', methods=['POST'])
def add_person_fav(person_id):
    
    request_body = request.get_json(force=True)

    user_query = User.query.filter_by(id = request_body["user_id"]).first() 
    if user_query is None:
        return jsonify({"msg": "User ins't registred"}), 404
    
    people_query = People.query.filter_by(id = person_id).first()
    if people_query is None:
        return jsonify({"msg": "Person doesn't exist"}), 404
    
    fav = UserFavorites.query.filter_by(user_id = request_body["user_id"]).filter_by(people_id = person_id).first()
    if fav: 
        return jsonify({"msg": "Person is already in favorites"}), 404
    
    new_person_fav = UserFavorites(user_id = request_body["user_id"], people_id = person_id)
    db.session.add(new_person_fav)
    db.session.commit()

    request_body = {
        "msg": "Person added to favorites"
    }
    return jsonify(request_body), 200

#Delete Person from User Favorites
@api.route('/fav/people/<int:person_id>', methods=['DELETE'])
def delete_person_fav(person_id):
    
    request_body = request.get_json(force=True)

    user_query = User.query.filter_by(id = request_body["user_id"]).first()
    if user_query is None:
        return jsonify({"msg": "User doen't exist"}), 404
    
    people_query = People.query.filter_by(id = person_id).first() 
    if people_query is None:
        return jsonify({"msg": "Person to delete doesn't existe"}), 404
    
    fav = UserFavorites.query.filter_by(user_id = request_body["user_id"]).filter_by(people_id = person_id).first()
    if fav is None:
        return jsonify({"msg": "Person to delete isn't in favorites"}), 404

    db.session.delete(fav)
    db.session.commit()

    request_body = {
        "msg": "Person deleted from favorites"
    }
    return jsonify(request_body), 200


#Add a Vehicle to User Favorites
@api.route('/fav/vehicles/<int:vehicle_id>', methods=['POST'])
def add_vehicle_fav(vehicle_id):
    
    request_body = request.get_json(force=True)

    user_query = User.query.filter_by(id = request_body["user_id"]).first() 
    if user_query is None:
        return jsonify({"msg": "User doesn't exist"}), 404
  
    vehicles_query = Vehicles.query.filter_by(id = vehicle_id).first()
    if vehicles_query is None:
        return jsonify({"msg": "Vehicle doesn't exist"}), 404
    
    fav = UserFavorites.query.filter_by(user_id = request_body["user_id"]).filter_by(vehicles_id = vehicle_id).first()
    if fav: 
        return jsonify({"msg": "Vehicle already in favories"}), 404
    
    new_vehicle_fav = Fav(user_id = request_body["user_id"], vehicles_id = vehicle_id)
    db.session.add(new_vehicle_fav)
    db.session.commit()

    request_body = {
        "msg": "Vehicle added to favorites"
    }
    return jsonify(request_body), 200

#Delete a Vehicle from User Favorites
@api.route('/fav/vehicles/<int:vehicle_id>', methods=['DELETE'])
def delete_vehicle_fav(vehicle_id):
    
    request_body = request.get_json(force=True)

    user_query = User.query.filter_by(id = request_body["user_id"]).first()
    if user_query is None:
        return jsonify({"msg": "User isn't registered"}), 404
    
    people_query = Vehicles.query.filter_by(id = vehicle_id).first() 
    if people_query is None:
        return jsonify({"msg": "Vehicle to delete doesn't exist"}), 404
    
    fav = UserFavorites.query.filter_by(user_id = request_body["user_id"]).filter_by(vehicles_id = vehicle_id).first()
    if fav is None:
        return jsonify({"msg": "Vehicle to delete isn't in favorites"}), 404

    db.session.delete(fav)
    db.session.commit()

    request_body = {
        "msg": "Vehcle deleted from favorites"
    }
    return jsonify(request_body), 200
