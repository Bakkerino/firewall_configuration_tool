import os
from flask import render_template, url_for, request, redirect, flash, session, jsonify
from cvf import app, db, bcrypt
from werkzeug.utils import secure_filename

from cvf.userforms import LoginForm, RegistrationForm, AccountChangeForm 
from cvf.models import User
from flask_login import login_user, current_user, logout_user, login_required
from datetime import timedelta
from cvf.parsingengine import cfgFileParsing
from cvf.viewengine import genConfigToTableHTML, genConfigToAccordeon, deleteEmpty
from cvf.filehandler import deleteImportCache, verify_filesize, verify_filename, readFile
from cvf.cfghulpengine import ConfigurationForm, genFortianalyzer # Legacy 


@app.route("/", methods=['GET', 'POST'])
@login_required
def home():
    form = ConfigurationForm()
    if current_user.is_authenticated:
        return render_template("home.html", form=form)
    else:
        return redirect(url_for("login"))

@app.route("/account", methods=["POST", "GET"])
@login_required
def account():
    # requests the contents from the form, if any
    form = AccountChangeForm()

    # checks if a user is authenticated, using flask_login
    if current_user.is_authenticated:
        # query's the database for the username of the current user
        usr = User.query.filter_by(username=current_user.username.lower()).first()
        if form.validate_on_submit():
            # compares the input password with the encrypted password from the database
            if usr and bcrypt.check_password_hash(usr.password, form.oldpassword.data):
                # generates a new encrypted/hashed password
                current_user.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                # commits the changes, in this case a new password
                db.session.commit()
                flash(f'{current_user.username} gewijzigd!', 'success')
                return redirect(url_for('account'))
            else:
                flash(f'Inloggegevens niet correct, probeer het overnieuw.', 'danger')
    return render_template("account.html", form=form)
    

@app.route("/register", methods=['GET', 'POST'])
def register():
    # requests the contents from the form, if any
    form = RegistrationForm()
    # checks if a user is already authenticated, using flask_login, redirects if true
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    else:
        if form.validate_on_submit():
            # generates a new encrypted/hashed password
            hash_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            # combines username and password and commits them in database
            usr = User(username=form.username.data.lower(), password=hash_pwd)  
            db.session.add(usr)
            db.session.commit()
            flash(f'Account aangemaakt voor {form.username.data}!', 'success')
            return redirect(url_for('login'))
            
    return render_template('registreren.html', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    # checks if a user is already authenticated, using flask_login, redirects if true
    if current_user.is_authenticated:
        flash(f'U bent ingelogd als {current_user.username}', 'success')
        return redirect(url_for("home"))
    else:
        # requests the contents from the form, if any
        form = LoginForm()
        if form.validate_on_submit():
            # query's the database for the username of the input username
            usr = User.query.filter_by(username=form.username.data.lower()).first()
            # compares database password with input password
            if usr and bcrypt.check_password_hash(usr.password, form.password.data):
                # user is logged in
                login_user(usr, remember=form.remember.data, duration=timedelta(minutes=5))
                flash(f'U bent ingelogd als {usr.username}!', 'success')
                return redirect(url_for("home"))
            else:
                # raises error string if login failed
                flash(f'Inloggen niet gelukt, probeer het overnieuw.', 'danger')
        return render_template('login.html', form=form)

@app.route("/get_my_ip", methods=["GET"])
def get_my_ip():
    # returns the ip-adress of the current user
    return request.environ.get('HTTP_X_REAL_IP', request.remote_addr)

@app.route("/logout")
def logout():
    # Logs the user out using flask_login and redirects
    logout_user()
    flash(f'Uitgelogd!', 'success')
    return redirect(url_for('login'))    

@app.route("/configuratieimport", methods=['GET', 'POST'])
@login_required
def configuratieimport():
    # Handles the input and view of firewallconfiguration files, using fileimport functionality
    extension = ""
    if request.method == 'POST':
        if request.files:

            # checks if file has a valid size, gathered from cookie, redirects if false
            if "filesize" in request.cookies:
                if not verify_filesize(request.cookies["filesize"]):
                    if app.config["DEBUG"]: print("Maximum bestandgrootte overschreden")
                    flash(f'Maximum bestandgrootte van {round(app.config["MAX_FILESIZE"]/1000, 2)}kB overschreden', 'danger')
                    return redirect(request.url)

            # requests the file that has been input
            cfgbestand = request.files["cfgbestand"]
            # checks if file has a filename
            if cfgbestand.filename == "":
                print("Geen bestandsnaam")
                return redirect(request.url)

            # Verifies the filename (extension)
            if verify_filename(cfgbestand.filename):
                # Saves the file that has been input
                bestandsnaam = secure_filename(cfgbestand.filename)
                cfgbestand.save(os.path.join(app.config["CFG_UPLOADS"], bestandsnaam))
                if app.config["DEBUG"]: print("#########################################"); print("Input: ", cfgbestand, bestandsnaam)   
                # Reads the file so it can be parsed
                cfgbestand = readFile(bestandsnaam)
                # Parses the contents of the file and outputs it in a json format
                cfgjson = cfgFileParsing(bestandsnaam) 
                # Deletes the uploaded file
                deleteImportCache(bestandsnaam)
                # Accepts json, deletes empty records, outputs json object
                cfgJsonObject = deleteEmpty(cfgjson)
                print(reference['fortigateversion'])
                # Formats the contents of the jsonobject (configuration) to html in a table format
                ConfigTableHTML = genConfigToTableHTML(cfgJsonObject)

                # Accepts json object and formats it to a user-friendly view as html
                overviewImpact="<h2>None</h2>"
                if app.config["DEBUG"]: 
                    return render_template('configuratieimport.html', fgenConfigToAccordeon=genConfigToAccordeon, bestandsnaam=bestandsnaam, 
                    cfgbestand=cfgbestand, cfgjson=cfgjson, cfgJsonObject=cfgJsonObject, ConfigTableHTML=ConfigTableHTML, overviewImpact=overviewImpact)
                else:
                    return render_template('configuratieimport.html', bestandsnaam=bestandsnaam,
                    cfgJsonObject=cfgJsonObject, ConfigTableHTML=ConfigTableHTML, overviewImpact=overviewImpact)

            else:
                # Displays error message when filename (extension) not allowed
                for x in app.config["ALLOWED_IMPORTFILE_EXTENSIONS"]: extension += "." + x.lower() + " "
                if app.config["DEBUG"]: print("Bestandsextentie niet toegestaan, gebruik", extension)
                flash(f'Bestandsextentie niet toegestaan, gebruik {extension}', 'danger')
                return redirect(request.url)    
        else:
            return redirect(request.url)
    else:
        return render_template('configuratieimport.html')


@app.route("/configuratiehulp", methods=['GET', 'POST'])
@login_required
def configuratiehulp():
    # Handles the input and view of firewallconfiguration, using inputforms
    # Legacy, only accessible from debug
    if app.config["DEBUG"]:
        form = ConfigurationForm()
        commandOutput = feedbackOutput = ""
        output = []

        if current_user.is_authenticated:
            if form.validate_on_submit():
                commandOutput += form.configuratie_vpn.data
                commandOutput += form.configuratie_interface_wan_ip.data

                if form.configuratie_fanServer.data and form.configuratie_fanSerial.data:
                    output = (genFortianalyzer(form.configuratie_fanServer.data, form.configuratie_fanSerial.data))
                    commandOutput += output[0] 
                    feedbackOutput += output[1]
            return render_template("configuratiehulp.html", form=form, commandOutput=commandOutput, feedbackOutput=feedbackOutput)
        else:
            return redirect(url_for("login"))
    else:
        flash(f'Niet toegankelijk, gebruik debug mode', 'danger')
        return redirect(url_for('home'))

    
   