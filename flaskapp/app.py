from flask import Flask, render_template, url_for, request, redirect, flash
from random import random, randint
from formulieren import RegistratieFormulier, LoginFormulier
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dc7c6759cbb3d6ce0d57d790ec3b8ffb'

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

#@app.route("/<usr>")
#def user(usr):
#    return f"{usr}"


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistratieFormulier()
    if form.validate_on_submit():
        flash(f'Account aangemaakt voor {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('registreren.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginFormulier()
    if form.validate_on_submit():
        if form.username.data == 'admin' and form.password.data == 'P@ssword':
            flash(f'Je bent ingelogd als {form.username.data}!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Inloggen niet gelukt, probeer het overnieuw.', 'danger')
    return render_template('login.html', title='Login', form=form)


if __name__ == "__main__":
    app.run(debug=True)