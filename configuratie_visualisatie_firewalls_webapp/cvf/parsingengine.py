import json, os
from cvf import app

config = {}

def genOverviewConfigHTML(jsonConfigObject):
    html = "<table id=\"viewtable\" class=\"table table-sm\">" + "<tbody>"
    for header, sectionData in jsonConfigObject.items():
        html += "<tr>" + "<th>"
        html += "<div class=\"btn-group-toggle\" data-toggle=\"buttons\"><label class=\"btn btn-outline-secondary\">"
        html += "<input type=\"checkbox\" name=\"" + header.lower() + "\" id=\"" + header.lower() + "\" data-toggle=\"toggle\">" + header + "</th>" 
        html += "</label>" + "</div>"
        html += "<td class=\"hide\" style=\"display: none;\" id=\"dataview\">" + "<table id=\"viewtable\" class=\"table table-sm\">" + "<tbody>"
        for section, valueData in sectionData.items():
            html += "<tr>" + "<th>" + section + "</th>" + "<td>" + "<table id=\"viewtable\" class=\"table table-sm\">" + "<tbody>"
            for value in valueData.items():
                html += "<tr>" + "<th>" + value[0] + "</th>" + "<td>" + value[1] + "</td>" + "</tr>"
            html += "</tbody>" + "</table>" + "</td>" + "</tr>"
        html += "</tbody>" + "</table>" + "</td>" + "</tr>"
    html += "</tbody>" + "</table>"
    return html

def jsonToHTML(verwerktbestand):
    return json2html.convert(json = verwerktbestand, table_attributes="class=\"table table-sm\"id=\"viewtable\"")

    #html = ""
    #for k in list(jsonConfigObject):
    #    html += "<h2>" + k + "</h2>"
    #return html

def deleteEmpty(jsonconfig):
    jsonObject = json.loads(jsonconfig)
    for k in list(jsonObject):
        try:
            if len(jsonObject[k])<1:
                del jsonObject[k]
                if app.config["DEBUG"]: print(k, "-> is leeg, record verwijderd")
        except: pass
    return jsonObject



def deleteImportCache(bestandsnaam): 
    if os.path.exists(app.config["CFG_UPLOADS"] + bestandsnaam):
        os.remove(app.config["CFG_UPLOADS"] + bestandsnaam)
        if app.config["DEBUG"]: print(bestandsnaam, " -> verwijderd")
    else:
        if app.config["DEBUG"]: print(bestandsnaam, " -> verwijderen niet mogelijk")

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
        arguments = ['system', 'vpn', 'user', 'vdom', 'firewall', 'voip', 'web-proxy', 'application', 'dlp', 'webfilter', 'spamfilter', 'log', 'router']
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

            if line[0] in ("#", "\n", "\""):
                if app.config["DEBUG"]: print("leeg/comment")
                continue

            if line.split()[0] == 'end' and previous_line[0] == 'config':
                if app.config["DEBUG"]: print("inhoud leeg")
                continue

            line = line.replace("\"", "")
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
                if section not in config.get(header):
                    config[header][section] = {}

            if action == 'set':
                if previous_line[0] == 'config' and section not in config[header]:
                    section = '1'
                    config[header][section] = {}
                     
                name  = args.pop(0)

                if action == 'password' or 'passwd' and args[0] == 'ENC': name = name + " " + args[0]; del args[0]

                value = ' '.join(args).strip('"')

                if value.startswith('-----'):
                    value += " "
                    for line in fh:
                        count += 1
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
    deleteImportCache(bestandsnaam)

    jsonconfig = json.dumps(config, indent=4)
    jsonConfigObject = deleteEmpty(jsonconfig)
    return jsonconfig, jsonConfigObject