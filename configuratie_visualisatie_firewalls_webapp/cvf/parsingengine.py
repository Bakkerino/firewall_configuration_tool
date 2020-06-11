import json, os
from cvf import app
from json2html import *

config = {}

def jsonToHTML(verwerktbestand):
    return json2html.convert(json = verwerktbestand, table_attributes="class=\"table table-bordered\"style=\"width: 75%\"")


def verify_filesize(filesize):
    print(filesize)
    if int(filesize) <= app.config["MAX_FILESIZE"]:
        return True
    else:
        return False

def verify_filename(filename):
    if not "." in filename:
        if app.config["DEBUG"]: print("Ongeldige bestandsnaam")
        return False
    bextensie = filename.rsplit(".", 1)[1]

    if bextensie.upper() in app.config["ALLOWED_IMPORTFILE_EXTENSIONS"]:
        return True
    else:
        return False

def readFile(bestandsnaam):
    with open(app.config["CFG_UPLOADS"] + bestandsnaam) as fh:
        data = fh.read()
    return data

def cfgFileParsing(bestandsnaam):
    with open(app.config["CFG_UPLOADS"] + bestandsnaam) as fh:

        arguments = ['system', 'vpn', 'user', 'vdom', 'firewall', 'voip', 'web-proxy', 'application', 'dlp', 'webfilter']
        config = {}
        previous_line = []
        section = ""
        count = 0
        for line in fh:
            if app.config["DEBUG"]:
                count += 1
                current_line = line.split()
                print("###########################################")
                print(count - 1, ": Previous line: >", previous_line)
                print(count, ": Current line: >", current_line)

            if line[0] in ("#", "\n"):
                if app.config["DEBUG"]: print("empty/comment")
                continue

            args = line.split()
            action, *args = line.split()

            if action == 'config' and args[0] in arguments:

                if args[0] == 'system': args.pop(0)
                header = ' '.join(args)
                if header not in config:
                    config[header] = {}
            else:
                pass

            if action == 'edit':
                section = ' '.join(args).strip('"')
                if section not in config[header]:
                    config[header][section] = {}

            if action == 'set':
                if previous_line[0] == 'config' and section not in config[header]:
                    section = '1'
                    config[header][section] = {}

                name  = args.pop(0)
                value = ' '.join(args).strip('"')
                if value.startswith('-----'):
                    value += " "
                    for line in fh:
                        if line.startswith('-----'): value += " " + ' '.join(line.split()).strip('"'); break
                        else: value += ' '.join(line.split()).strip('"')
                config[header][section][name] = value


            if action == 'append':
                name  = args.pop(0)
                value = ' '.join(args).strip('"')
                config[header][section][name] = value

            previous_line = line.split()


        else:
            pass
    if os.path.exists(app.config["CFG_UPLOADS"] + bestandsnaam):
        os.remove(app.config["CFG_UPLOADS"] + bestandsnaam)
        if app.config["DEBUG"]: print(bestandsnaam, " verwijderd")
    else:
        if app.config["DEBUG"]: print(bestandsnaam, " verwijderen niet mogelijk")

    verwerktbestand = json.dumps(config, indent=4)

    return verwerktbestand