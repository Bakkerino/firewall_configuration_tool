import os
from cvf import app


# Deletes the file that has been uploaded, combining pre-configured config with filename
def deleteImportCache(bestandsnaam): 
    if os.path.exists(app.config["CFG_UPLOADS"] + bestandsnaam):
        os.remove(app.config["CFG_UPLOADS"] + bestandsnaam)
        if app.config["DEBUG"]: print(bestandsnaam, " -> verwijderd")
    else:
        if app.config["DEBUG"]: print(bestandsnaam, " -> verwijderen niet mogelijk")

# Verifies the filesize, depending on the pre-configered config
def verifyFilesize(filesize):
    print(filesize)
    if int(filesize) <= app.config["MAX_FILESIZE"]:
        return True
    else:
        return False

# verifies filename and extension, depending on the pre-configured config
def verifyFilename(filename):
    if not "." in filename:
        if app.config["DEBUG"]: print("Ongeldige bestandsnaam")
        return False
    bextensie = filename.rsplit(".", 1)[1]

    if bextensie.upper() in app.config["ALLOWED_IMPORTFILE_EXTENSIONS"]:
        return True
    else:
        return False

# Reads the file combining pre-configured config with filename
def readFile(bestandsnaam):
    with open(app.config["CFG_UPLOADS"] + bestandsnaam) as configfile:
        data = configfile.read()
    return data