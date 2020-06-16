import json
from cvf import app

# Accepts a json object and generates this in a html table format, with toggle buttons as headers. This function is similair to what json2html does
def genOverviewConfigHTML(jsonConfigObject):
    html = "<table id=\"viewtable\" class=\"table table-sm\">" + "<tbody>"
    for header, sectionData in jsonConfigObject.items():
        html += "<tr>" + "<th>"
        html += "<div class=\"btn-group-toggle\" data-toggle=\"button\"><label class=\"btn btn-outline-secondary\">"
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

# Checks for empty records in json using keys, deletes empty records
def deleteEmpty(jsonconfig):
    jsonObject = json.loads(jsonconfig)
    for k in list(jsonObject):
        try:
            if len(jsonObject[k])<1:
                del jsonObject[k]
                if app.config["DEBUG"]: print(k, "-> is leeg, record verwijderd")
        except: pass
    return jsonObject