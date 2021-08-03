from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect, session
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, logout_user
from forms import SignupForm
from forms import LoginForm


app = Flask(__name__)
db = SQLAlchemy()
login_manager = LoginManager()
mysql = MySQL(cursorclass=DictCursor)

app.config.from_object("config.Config")
mysql.init_app(app)
db.init_app(app)
login_manager.init_app(app)

with app.app_context():
    import auth
    db.create_all()

@app.route('/', methods=['GET'])
def index():
    user = {'username': 'Oscar Project'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM oscar_age_male')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, oscar=result)


@app.route('/view/<int:oscar_id>', methods=['GET'])
def record_view(oscar_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM oscar_age_male WHERE id=%s', oscar_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', osc=result[0])


@app.route('/edit/<int:oscar_id>', methods=['GET'])
def form_edit_get(oscar_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM oscar_age_male WHERE id=%s', oscar_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', osc=result[0])


@app.route('/edit/<int:oscar_id>', methods=['POST'])
def form_update_post(oscar_id):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('sIndex'), request.form.get('sYear'), request.form.get('sName'),request.form.get('sAge'),
                 request.form.get('sMovie'), request.form.get('sNote'), oscar_id)
    sql_update_query = """UPDATE oscar_age_male t SET t.sIndex = %s, t.sYear = %s, t.sName = %s, t.sAge = %s,t.sMovie = 
    %s, t.sNote = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/oscar/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New Oscar Form')


@app.route('/oscar/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('sIndex'), request.form.get('sYear'), request.form.get('sName'),request.form.get('sAge'),
                 request.form.get('sMovie'), request.form.get('sNote'))
    sql_insert_query = """INSERT INTO oscar_age_male (sIndex,sYear,sName,sAge,sMovie,sNote) VALUES (%s, %s,%s, %s,%s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/delete/<int:oscar_id>', methods=['POST'])
def form_delete_post(oscar_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM oscar_age_male WHERE id = %s """
    cursor.execute(sql_delete_query, oscar_id)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/oscar', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM oscar_age_male')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/oscar/<int:oscar_id>', methods=['GET'])
def api_retrieve(oscar_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM oscar_age_male WHERE id=%s', oscar_id)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp

@app.route('/api/v1/oscar/<int:oscar_id>', methods=['PUT'])
def api_edit(oscar_id) -> str:
    cursor = mysql.get_db().cursor()
    content = request.json
    inputData = (content['sIndex'], content['sYear'], content['sName'],
                 content['sAge'], content['sMovie'],
                 content['sNote'], oscar_id)
    sql_update_query = """UPDATE oscar_age_male t SET t.sIndex = %s, t.sYear = %s, t.sName = %s, t.sAge = 
            %s, t.sMovie = %s, t.sNote = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=201, mimetype='application/json')
    return resp

@app.route('/api/v1/oscar', methods=['POST'])
def api_add() -> str:
    content = request.json
    cursor = mysql.get_db().cursor()
    inputData = (content['sIndex'], content['sYear'], content['sName'],
                 content['sAge'], content['sMovie'],
                 content['sNote'])
    sql_insert_query = """INSERT INTO oscar_age_male (sIndex,sYear,sName,sAge,sMovie,sNote) VALUES (%s, %s,%s, %s,%s, %s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=201, mimetype='application/json')
    return resp

@app.route('/api/v1/oscar/<int:oscar_id>', methods=['DELETE'])
def api_delete(oscar_id) -> str:
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM oscar_age_male WHERE id = %s """
    cursor.execute(sql_delete_query, oscar_id)
    mysql.get_db().commit()
    resp = Response(status=210, mimetype='application/json')
    return resp

@app.route('/signup', methods=['GET', 'POST'])
def signup_page():
    return render_template(
        'signup.jinja2',
        title='Create an Account.',
        form=SignupForm(),
        template='signup-page',
        body="Sign up for a user account."
    )


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    return render_template(
        '/login.jinja2',
        title='Create an Account.',
        form=LoginForm,
        template='login-page',
        body="Log in to your account."
    )


@app.route("/session", methods=["GET"])
@login_required
def session_view():
    """Display session variable value."""
    return render_template(
        "session.jinja2",
        title="MLB Players",
        template="dashboard-template",
        session_variable=str(session["redis_test"]),
    )


@app.route("/logout")
@login_required
def logout():
    """User log-out logic."""
    logout_user()
    return render_template('login.jinja2')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)