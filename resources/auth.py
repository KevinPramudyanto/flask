import bcrypt

from flask import request, jsonify, Blueprint
from marshmallow import ValidationError

from db.db_pool import get_connection, release_connection
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt


auth = Blueprint('auth',__name__)


@auth.route('/register', methods=['POST'])
def registration():
    data = request.get_json()
    conn, cursor = get_connection()
    cursor.execute('SELECT uuid FROM auth WHERE email=%s', (data['email'],))
    result = cursor.fetchone()

    if result:
        return jsonify(status='error', msg='duplicate email'), 400

    password_hash = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

    cursor.execute('INSERT INTO auth (email, name, password) VALUES (%s, %s, %s)',
                   (data['email'], data['name'], password_hash.decode('utf-8')))
    conn.commit()
    release_connection(conn)

    return jsonify(status='ok', msg='registration done'), 200


@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    conn, cursor = get_connection()
    cursor.execute('SELECT name, password FROM auth WHERE email=%s', (data['email'],))
    result = cursor.fetchone()
    release_connection(conn)

    if not result:
        return jsonify(status='error', msg='username or password is incorrect'), 401

    access = bcrypt.checkpw(data['password'].encode('utf-8'), result['password'].encode('utf-8'))

    if not access:
        return jsonify(status='error', msg='wrong username or password'), 401

    access_token = create_access_token(data['email'], additional_claims={'name':result['name']})
    refresh_token = create_refresh_token(data['email'], additional_claims={'name':result['name']})

    return jsonify(access=access_token, refresh=refresh_token)


@auth.route('/refresh')
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    claims = get_jwt()

    access_token = create_access_token(identity, additional_claims={'name':claims['name']})

    return jsonify(access=access_token)