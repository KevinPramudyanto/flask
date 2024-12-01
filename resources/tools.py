from flask import request, jsonify, Blueprint
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required

from db.db_pool import get_connection, release_connection #, cursor_factory
from validators.tools import AddToolsInputs

tools = Blueprint('tools',__name__)


@tools.route('/tools')
@jwt_required()
def all_tools():
    # conn = get_connection()
    # cursor = conn.cursor(cursor_factory=cursor_factory())
    conn, cursor = get_connection()
    cursor.execute('SELECT * FROM tools ORDER BY id')
    results = cursor.fetchall()
    release_connection(conn)

    if not results:
        results = []

    return jsonify(results), 200


# @tools.route('/tools/<tool_id>', methods=['GET'])
# def find_one_tool_by_id(tool_id):
#     # conn = get_connection()
#     # cursor = conn.cursor(cursor_factory=cursor_factory())
#     conn, cursor = get_connection()
#     cursor.execute('SELECT * FROM tools WHERE id=%s',(tool_id,))
#     results = cursor.fetchone()
#     release_connection(conn)
#
#     if not results:
#         results = {}
#
#     return jsonify(results), 200


@tools.route('/tools', methods=['PUT'])
def add_tool():
    data = request.get_json()
    try:
        AddToolsInputs().load(data)
    except ValidationError as err:
        return jsonify(err.messages)

    # conn = get_connection()
    # cursor = conn.cursor()
    conn, cursor = get_connection()
    cursor.execute(f'INSERT INTO tools (name, description) '
                   f'VALUES (%s, %s)', (data['name'], data['description']))
    conn.commit()
    release_connection(conn)

    return jsonify({'status':'ok','msg':'tool saved'}), 200


@tools.route('/tools', methods=['PATCH'])
def update_tool():
    tool_id = request.json.get('id')
    name = request.json.get('name')
    description = request.json.get('description')

    # conn = get_connection()
    # cursor = conn.cursor(cursor_factory=cursor_factory())
    conn, cursor = get_connection()
    cursor.execute('SELECT * FROM tools WHERE id=%s',(tool_id,))
    results = cursor.fetchone()
    print(name, results['name'], description, results['description'], tool_id)
    cursor.execute(f'UPDATE tools '
                   f'SET name=COALESCE(%s, %s), '
                   f'description=COALESCE(%s, %s) '
                   f'WHERE id=%s', (name, results['name'], description, results['description'], tool_id))

    conn.commit()
    release_connection(conn)

    return jsonify(status='ok',msg='tool updated'), 200


# @tools.route('/tools/<tool_id>', methods=['DELETE'])
# def delete_tool(tool_id):
#     # conn = get_connection()
#     # cursor = conn.cursor()
#     conn, cursor = get_connection()
#     cursor.execute('DELETE FROM tools WHERE id=%s',(tool_id,))
#     conn.commit()
#     release_connection(conn)
#
#     return jsonify(status='ok',msg='tool deleted'), 200


@tools.route('/tools/<tool_id>', methods=['GET', 'DELETE'])
def parameter_function(tool_id):
    conn, cursor = get_connection()
    return_value = None

    if request.method == 'GET':
        cursor.execute('SELECT * FROM tools WHERE id=%s', (tool_id,))
        results = cursor.fetchone()

        if not results:
            results = {}

        return_value = results

    elif request.method == 'DELETE':

        cursor.execute('DELETE FROM tools WHERE id=%s', (tool_id,))
        conn.commit()

        return_value = {'status':'ok', 'msg':'tool deleted'}

    release_connection(conn)

    return jsonify(return_value), 200