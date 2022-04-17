import flask
from flask import jsonify, request

from data import db_session
from data.jobs import Jobs

blueprint = flask.Blueprint(
    'jobs_api', __name__, template_folder='templates'
)


@blueprint.route('/api/jobs', methods=['GET'])
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(
                    only=('id', 'job', 'team_leader', 'work_size',
                          'collaborators',
                          'start_date', 'end_date', 'is_finished')
                ) for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {'job': job.to_dict(only=(
            'id', 'job', 'team_leader', 'work_size', 'collaborators',
            'start_date', 'end_date', 'is_finished'))}
    )


@blueprint.route('/api/jobs', methods=['POST'])
def create_job():
    if not request.json:
        return jsonify({'error': 'Empty request'})

    elif not all(key in request.json for key in
                 ['id', 'job', 'work_size', 'collaborators', 'is_finished',
                  'team_leader']):
        return jsonify({'error': 'Bad request'})

    db_sess = db_session.create_session()
    if db_sess.query(Jobs).filter(Jobs.id == request.json['id']).first():
        return jsonify({'error': 'Id already exists'})

    job = Jobs(
        id=request.json['id'],
        job=request.json['job'],
        work_size=request.json['work_size'],
        collaborators=request.json['collaborators'],
        is_finished=request.json['is_finished'],
        team_leader=request.json['team_leader'],
    )
    db_sess.add(job)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        return jsonify({'error': 'Not found'})
    db_sess.delete(job)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:job_id>', methods=['PUT'])
def update_job(job_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})

    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        return jsonify({'error': 'Not found'})

    args = {
        'id': job.id,
        'job': job.job,
        'collaborators': job.collaborators,
        'work_size': job.work_size,
        'is_finished': job.is_finished,
        'team_leader': job.team_leader
    }
    for change in request.json:
        args[change] = request.json[change]

        # если пользователь хочет поменять id работы
        if change == 'id':
            # Проверка, что работы с таким id ещё не существует
            if db_sess.query(Jobs).filter(
                    Jobs.id == request.json['id']).first():
                return jsonify({'error': 'Id already exists'})

    new_job = Jobs(
        id=args['id'],
        job=args['job'],
        work_size=args['work_size'],
        collaborators=args['collaborators'],
        is_finished=args['is_finished'],
        team_leader=args['team_leader'],
    )
    db_sess.delete(job)
    db_sess.add(new_job)
    db_sess.commit()
    return jsonify({'success': 'OK'})
