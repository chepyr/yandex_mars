import flask
from flask import jsonify, request

from data import db_session
from data.users import User

blueprint = flask.Blueprint(
    'user_api', __name__, template_folder='templates'
)


@blueprint.route('/api/users', methods=['GET'])
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return jsonify(
        {'users':
            [item.to_dict(only=(
                'id', 'surname', 'name', 'age', 'position',
                'speciality', 'address', 'email')
            ) for item in users]}
    )


@blueprint.route('/api/user/<int:user_id>', methods=['GET'])
def get_job(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    return jsonify({
        'user': user.to_dict(only=('id', 'surname', 'name', 'age', 'position',
                                   'speciality', 'address', 'email'))
    })


@blueprint.route('/api/user/<int:user_id>', methods=['DELETE'])
def delete_job(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    db_sess.delete(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/user', methods=['POST'])
def create_job():
    if not request.json:
        return jsonify({'error': 'Empty request'})

    elif not all(key in request.json for key in
                 ['id', 'email', 'hashed_password']):
        pass
#     TODO: kmdkjs


@blueprint.route('/api/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    pass
