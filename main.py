from flask import url_for, Flask, render_template

app = Flask(__name__)


@app.route('/<title>')
@app.route('/index/<title>')
def index(title):
    return render_template('base.html', title=title)


@app.route('/training/<prof>')
def training(prof):
    return render_template('training.html', prof=prof)


@app.route('/list_prof/<list_prop>')
def list_prof(list_prop):
    args = {'list': list_prop}
    args['professions'] = ['инженер-исследователь', 'пилот', 'строитель', 'экзобиолог', 'врач',
                           'инженер по терраформированию', 'климатолог',
                           'специалист по радиационной защите', 'астрогеолог', 'гляциолог',
                           'инженер жизнеобеспечения, метеоролог', 'оператор марсохода',
                           'киберинженер', 'штурман', 'пилот дронов']
    return render_template('list_prof.html', **args)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
