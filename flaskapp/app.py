from flask import Flask, render_template, url_for, request, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from formulieren import RegistratieFormulier, LoginFormulier
from datetime import timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dc7c6759cbb3d6ce0d57d790ec3b8ffb'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=2) # sessietijd

db = SQLAlchemy(app)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.password}')"


@app.route("/")
@app.route("/home")
def home():
    if "user" in session:
        user = session["user"]
        return render_template("home.html", user=user)
    else:
        return redirect(url_for("login"))

#@app.route("/user", methods=["POST", "GET"])
#def user():
#    if "user" in session:
#        user = session["user"]
#        return render_template("user.html",  user=user, form=form)
#    else:
#        return redirect(url_for("login"))

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistratieFormulier()
    if "user" in session:
        user = session["user"]
        return render_template('registreren.html', title='Register', user=user, form=form)
    else:
        if form.validate_on_submit():

            if User.query.filter_by(naam=form.username.data).first().username:
                flash(f'Probeer het overnieuw!', 'danger')
            else:
                usr = User(form.username.data, form.password.data)    
                db.session.add(usr)
                db.session.commit()
                

                session["user"] = form.username.data
                session.permanent = True
                flash(f'Account aangemaakt voor {form.username.data}!', 'success')
                return redirect(url_for('home'))


    return render_template('registreren.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if "user" in session:
        user = session["user"]
        flash(f'U bent ingelogd als {user}', 'success')
        return redirect(url_for("home"))
    else:
        form = LoginFormulier()
        if form.validate_on_submit():
            #flash(f'test {user_exist.naam}!', 'success')
            
            if form.username.data == User.query.filter_by(username=form.username.data, password=form.password.data).first().username:
                session.permanent = True
                session["user"] = User.query.filter_by(username=form.username.data, password=form.password.data).first().username
                flash(f'Je bent ingelogd als {session["user"]}!', 'success')
                return redirect(url_for('home'))
            else:
                flash(f'Inloggen niet gelukt, probeer het overnieuw. { user_exist, user_exist.naam }', 'danger')
        return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    session.pop("user", None)
    flash(f'Uitgelogd!', 'success')
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)