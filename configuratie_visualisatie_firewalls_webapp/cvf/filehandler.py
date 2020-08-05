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
# makes sure that filenames containing ";","|", ":", "<", ">", "/" ,"\\", "*", "%", "$" are not possible, this for safety purposes
# makes sure that there are no double extension delimitors 

def verifyFilename(filename):
    dissalowed_chars= [";","|", ":", "<", ">", "/" ,"\\", "*", "%", "$"]

    if filename.count(".") == 1 and not any(ele in filename for ele in dissalowed_chars) and len(filename) in range(1, 255):
        bextensie = filename.rsplit(".", 1)[1]
    else:
        if app.config["DEBUG"]: print("Ongeldige bestandsnaam")
        return False

    if bextensie.upper() in app.config["ALLOWED_IMPORTFILE_EXTENSIONS"]:
        return True
    else:
        if app.config["DEBUG"]: print("Ongeldige bestandsextensie")
        return False

# Reads the file combining pre-configured config with filename
def readFile(bestandsnaam):
    with open(app.config["CFG_UPLOADS"] + bestandsnaam) as configfile:
        data = configfile.read()
    return data