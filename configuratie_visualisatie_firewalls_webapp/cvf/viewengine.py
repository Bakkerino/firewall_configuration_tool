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

# Accepts json object, headers[] and a color. Generates tables and entries, of which are contained by an accordeon menu. Outputs HTML
def genConfigToAccordeon(jsonConfigObject, arguments, gradeColor):
    html = ""
    for header, sectionData in jsonConfigObject.items():
        if arguments == True or header in arguments:
            header = header.lower().replace(' ', '-')
            html += "<div class=\"accordion\" id=\"accordion" + header + "\"><div class=\"card\"><div class=\"card-header\" id=\"heading" + header + "\">"
            html += "<h2 class=\"mb-0\"><button class=\"btn btn-link btn-block text-left collapsed\" id=\"accordeonbutton\" type=\"button\" style=\"color: " + gradeColor + "\"data-toggle=\"collapse\" data-target=\"#collapse" + header + "\" aria-expanded=\"true\" aria-controls=\"collapse" + header + "\">Specifieke instellingen (" + header + ")</button></h2></div>"
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

# Accepts json object, generates a card with logo, color and data entries. Is used to display the headers corrosponding with firewallconfiguration
def genCardMenus(jsonConfigObject, gradeColor="warning"):
    htmlBacklog = ""
    html = genHeadOveriew(jsonConfigObject) # header
    
    arguments = True #['interface', 'firewall policy']
    for header, sectionData in jsonConfigObject.items():
        if header in ['config', 'global']:
            continue
        if arguments == True or header in arguments:
            gradeColor, content, logo = genContentCard(header, sectionData)
            htmlCard = "<header class=\"p-3 mb-2 bg-grey rounded border border-" + gradeColor + "\" id=\"" + header.replace(' ', '-') + "\">"
            htmlCard += "<div class=\"media\">"
            htmlCard += "<img src=\"static/icons/" + logo + "\" class=\"align-self-start mr-3\" alt=\"" + header.replace(' ', '-') + "\">"
            htmlCard += "<div class=\"media-body\" id=\"mediaoverzicht\">"
            htmlCard += "<h5 class=\"mt-0\"><b>" + header.capitalize() + "</b> "
            htmlCard += genPopoverButton(header)
            htmlCard += "</h5><legend class=\"border-bottom mb-1\"></legend>"
            htmlCard += "<p>" + content + "</p>"
            htmlCard += "</div></div>"
            htmlCard += genConfigToAccordeon(jsonConfigObject, [header], boostrapColorToCSSColor(gradeColor))
            htmlCard += "</header>"
            if app.config["DEBUG"]: print('created card for: ' + header)
        if content == "": htmlBacklog += htmlCard; continue # Minder interessante informatie achteraan
        html += htmlCard
    html += htmlBacklog    
    return html

# Accepts a header and corresponding sectiondata, generates the contents of the cardmenu's, contents are custom per header
def genContentCard(header, sectionData):
    html = ""; logo = "fortigate.png"; gradeColors = (); 

    if header == 'firewall policy':
        logo = "firewallpolicy.png"
        pos= "front"
        for section, valueData in sectionData.items():
            html += "<h5>" + valueData['name'] + "</h5>"
            html += "<th>" + "service" + "</th>" + "<td>"
            for x in valueData.get('service', 'none').split(", "): 
                html += genPopoverButton(x)
            html += "</td>"

    if header == 'interface':
        logo = "interface5.png"
        for section, valueData in sectionData.items():
            html += "<h5>" + section + "(" + valueData.get('alias', '') + ")" + "</h5>"
    return findhighestGradeColor(html), html, logo

# Accepts a string and  checks if certain strings are contained within the string, resulting in returning the color with the highest priority
def findhighestGradeColor(gradeColorsHTML):
        if "danger" in gradeColorsHTML: return "danger"
        if "warning" in gradeColorsHTML: return "warning"
        if "success" in gradeColorsHTML: return "success"
        if "info" in gradeColorsHTML: return "info"
        return "secondary"

# Generates the header of het configoverview containing generic information like version, and names
def genHeadOveriew(cfgJsonObject):
    html = ""
    if cfgJsonObject.get('config', False) and cfgJsonObject.get('global', False):
        firewallversion = getPopoverContents(cfgJsonObject['config']['version']['version'].split('-')[1])
        html += """<header class=\"p-3 mb-2 bg-grey rounded border border-""" + firewallversion[2] + """\" id=\"overzichtheader\" >
              <div class=\"media\">
              <img src=\"static/icons/fortigate.png\" class=\"align-self-start mr-3\" alt=\"fortigate\">
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
                      title=\"""" +  firewallversion[0] + """\" data-trigger="focus" data-content=\"""" + firewallversion[1] + """\">
                        """ + cfgJsonObject['config']['version']['version'].split('-')[1] + """</button></td>
                      <th>Build:</th> <td>""" + cfgJsonObject['config']['version']['build'] + """</td>
                    </tr>
                  </tbody>
                </table>

              </div>
            </div>
            """ + genConfigToAccordeon(cfgJsonObject, ['config','global'], boostrapColorToCSSColor(firewallversion[2])) + """ </header> """
        return html
    else:
        return html

# Accepts an argument for a popoverbutton and returns an HTML popoverbutton with corrosponding header, title, content and colors
def genPopoverButton(argument):
    title, content, color = getPopoverContents(argument)
    button = """<button type=\"button\" data-trigger="focus"
            class="btn btn-sm btn-""" + color + """\" data-toggle=\"popover\" 
            title=\"""" +  title + """\" data-content=\"""" + content + "\">" + argument + "</button>"
    return button

# Accepts an argument for a popoverbutton and returns after referencing a json file corrosponding title, contents and color
def getPopoverContents(arg):
    f = open('./cvf/reference.json',)
    reference = json.load(f)
    if reference.get(arg, False):
        title = reference[arg]['title']
        content = reference[arg]['content']
        color = reference[arg]['color']
        return title, content, color
    else:
        title = "Titel"
        content = "Geen informatie beschikbaar"
        color = "secondary"
        return title, content, color

# Converts bootstrap colors arguments to CSS-colors
def boostrapColorToCSSColor(color):
    if color == "success": color = "green"
    if color == "warning": color = "#ffbf00"
    if color == "danger": color = "red"
    if color == "info": color = "blue"
    if color == "secondary": color = "black"
    return color


  