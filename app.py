from datetime import datetime
from flask import Flask, request, redirect, render_template, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from logging.handlers import RotatingFileHandler
from logging import Formatter
import logging
from logs_api.logs_request import get_logs

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///logs.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SECRET_KEY"] = 'confidential!'
app.config["LOGFILE"] = 'app_logging.log'
app.config["DEBUG"] = True

handler = RotatingFileHandler(app.config['LOGFILE'],
                              maxBytes=1000000, backupCount=1)
handler.setLevel(logging.DEBUG)
handler.setFormatter(Formatter('%(asctime)s %(levelname)s: %(message)s'))
app.logger.addHandler(handler)

db = SQLAlchemy(app)


class LogItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, default='n/a')
    created_at = db.Column(db.DateTime(50), default=datetime(1970, 1, 1))
    first_name = db.Column(db.String(50), default='n/a')
    second_name = db.Column(db.String(50), default='n/a')
    message = db.Column(db.Text, default='n/a')


@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        return redirect(url_for('index', day=request.form['date']))
    return render_template("index.html")


@app.route("/<day>")
def index(day):

    logs = get_logs(day)

    try:
        for log in logs:
            user_id = log['user_id']
            created_at = datetime.fromisoformat(log['created_at'])
            first_name = log['first_name']
            second_name = log['second_name']
            message = log['message']

            new_log = LogItem(
                user_id=user_id,
                created_at=created_at,
                first_name=first_name,
                second_name=second_name,
                message=message)
            db.session.add(new_log)
            db.session.commit()
    except (TypeError, KeyError):
        app.logger.info("Unsuccessfull call attempt")
        flash('Something wrong! Please check the error message:' + logs['error'], 'danger')
        return redirect(url_for('home'))
    
    app.logger.info("A new record in the DB")

    flash('Logs have been successfully dropped to the DB', 'success')
    return redirect(url_for('home'))


if __name__ == "__main__":

    db.create_all()
    app.run(debug=True)
