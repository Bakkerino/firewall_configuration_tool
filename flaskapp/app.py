from flask import Flask, render_template, url_for, request, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from formulieren import RegistratieFormulier, LoginFormulier
from datetime import timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dc7c6759cbb3d6ce0d57d790ec3b8ffb'
app.permanent_session_lifetime = timedelta(minutes=10) # sessietijd

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

    if form.validate_on_submit():
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
            if form.username.data == 'admin' and form.password.data == 'P@ssword':
                session.permanent = True
                session["user"] = form.username.data
                flash(f'Je bent ingelogd als {form.username.data}!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Inloggen niet gelukt, probeer het overnieuw.', 'danger')
        return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    session.pop("user", None)
    flash(f'Uitgelogd!', 'success')
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)