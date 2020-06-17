import json
from cvf import app

# Accepts a json object and generates this in a html table format, with toggle buttons as headers. This function is similair to what json2html does
def genConfigToTableHTML(jsonConfigObject):
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

def genConfigToAccordeon(jsonConfigObject, arguments):
    html = ""
    for header, sectionData in jsonConfigObject.items():

        if arguments == True or header in arguments:
            header = header.lower().replace(' ', '-')
            html += "<div class=\"accordion\" id=\"accordion" + header + "\"><div class=\"card\"><div class=\"card-header\" id=\"heading" + header + "\">"
            html += "<h2 class=\"mb-0\"><button class=\"btn btn-link btn-block text-left collapsed\" id=\"accordeonbutton\" type=\"button\" data-toggle=\"collapse\" data-target=\"#collapse" + header + "\" aria-expanded=\"true\" aria-controls=\"collapse" + header + "\">Specifieke instellingen (" + header + ")</button></h2></div>"
            html += "<div id=\"collapse" + header + "\" class=\"collapse\" aria-labelledby=\"heading" + header + "\" data-parent=\"#accordion" + header + "\">"
            html += "<div class=\"card-body\">"
            html += "<td class=\"hide\" style=\"display: none;\" id=\"dataview\">" + "<table id=\"viewtable\" class=\"table table-sm borderless\">" + "<tbody>"
            for section, valueData in sectionData.items():
                html += "<tr>" + "<th>" + section + "</th>" + "<td>" + "<table id=\"viewtable\" class=\"table table-sm borderless\">" + "<tbody>"
                for value in valueData.items():
                    html += "<tr>" + "<th>" + value[0] + "</th>" + "<td>" + value[1] + "</td>" + "</tr>"
                html += "</tbody>" + "</table>" + "</td>" + "</tr>"
            html += "</tbody>" + "</table>" + "</td>" + "</tr>"               
            html += "</div></div></div>"
    return html

def genCardMenus(jsonConfigObject, border_color="warning"):
    arguments = ['interface'] #True
    html = ""
    for header, sectionData in jsonConfigObject.items():
        if header in ['config', 'global']:
            continue
        if arguments == True or header in arguments:
            html += "<header class=\"p-3 mb-2 bg-grey rounded border border-" + border_color + "\" id=\"" + header.replace(' ', '-') + "\">"
            html += "<div class=\"media\">"
            html += "<img src=\"static/icons/fortigate.png\" class=\"align-self-center mr-3\" alt=\"" + header.replace(' ', '-') + "\">"
            html += "<div class=\"media-body\" id=\"mediaoverzicht\">"
            html += "<h5 class=\"mt-0\"><b>" + header.capitalize() + "</b></h5>"
            html += "<p>tekst of tabellen</p>"
            html += "</div></div>"
            html += genConfigToAccordeon(jsonConfigObject, [header])
            html += "</header>"
    return html

def genHeadOveriew(cfgJsonObject):
    html = ""
    if cfgJsonObject.get('config', False) and cfgJsonObject.get('global', False):
        firewallversion = getSecurityGrade(cfgJsonObject['config']['version']['version'].split('-')[1])
        html += """<header class=\"p-3 mb-2 bg-grey rounded border border-""" + firewallversion[2] + """\" id=\"overzichtheader\" >
              <div class=\"media\">
              <img src=\"static/icons/fortigate.png\" class=\"align-self-center mr-3\" alt=\"fortigate\">
              <div class=\"media-body\" id=\"mediaoverzicht\">
                <h5 class=\"mt-0\"><b>""" + cfgJsonObject['config']['version']['version'].split('-')[0].replace('FGT', 'FortiGate ') + """</b></h5>
                <table id=\"headertable\" class=\"table table-borderles\">
                  <tbody>
                      <tr>
                      <th>Hostname:</th> <td>""" + cfgJsonObject['global']['1']['hostname'] + """</td>
                      <th>Alias:</th> <td>""" + cfgJsonObject['global']['1']['alias'] + """</td>
                    </tr>
                    <tr>
                      <th>Software versie:</th><td><button type=\"button\" class="btn btn-sm btn-""" + firewallversion[2] +  """\" data-toggle=\"popover\" 
                      title=\"""" +  firewallversion[0] + """\" data-content=\"""" + firewallversion[1] + """\">
                        """ + cfgJsonObject['config']['version']['version'].split('-')[1] + """</button></td>
                      <th>Build:</th> <td>""" + cfgJsonObject['config']['version']['build'] + """</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
            """ + genConfigToAccordeon(cfgJsonObject, ['config','global']) + """ </header> """
        return html
    else:
        return html

def getSecurityGrade(arg):
    print (arg)
    f = open('./cvf/reference.json',)
    reference = json.load(f)
    if reference.get(arg, False):
        title = reference[arg]['title']
        content = reference[arg]['content']
        color = reference[arg]['color']
        return title, content, color
    else:
        title = "Titel"
        content = "Geen"
        color = "warning"
        return title, content, color



  