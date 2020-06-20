import json
from cvf import app
import re
config = {}


# Parsing engine that parses files line by line, written for fortigate configuration files, the function returns a json dump containing ordened config
def cfgFileParsing(filename):

    # The config headers that are used, viable and detected for parsing
    arguments = ['entries', 'system', 'vpn', 'user', 'vdom', 'firewall', 'voip', 'web-proxy', 'application', 'dlp', 'webfilter', 'spamfilter', 'log', 'router'] 
    fwConf = {}; previous_line = []; section = ""; count = 0; indentation = 0; indentation_name = indentation_config = "" # inits

    with open(app.config["CFG_UPLOADS"] + filename) as configfile:

        # Start of parsing line-by-line
        for line in configfile:
            # Print statements for debugging
            if app.config["DEBUG"]:
                count += 1
                current_line = line.split()
                print("###########################################")
                print(count - 1, ": Previous line: >", previous_line)
                print(count, ": Current indentation: >", indentation)
                print(count, ": indentation name: >", indentation_name)
                print(count, ": Current line: >", current_line)

            # If line is empty, commented or not viable
            if line[0] in ("#", "\n", "\""):

                def inputValuesConfig(name, value):
                    # Internal function for assigning the found (generic) values within this if statement
                    fwConf[head][section][name] = {}; fwConf[head][section][name] = value  
                    return  
                # Parsing the line for getting the generic information for a firewall, like the name and version etc
                if line.startswith('#config-version='):                
                    line = line.replace('\n', '')
                    head = "config"; fwConf[head] = {}
                    section = "version"; fwConf[head][section] = {}; 
                    # Using regex for getting the wanted variables
                    name, value = re.findall('version=\w+\W.+?(?=-)', line)[0].split('='); inputValuesConfig(name, value)
                    name, value = re.findall('build\d+\W\d+', line)[0].replace('build', 'build ').split(); inputValuesConfig(name, value)
                    name, value = re.findall('opmode=.+?(?=:)', line)[0].split('='); inputValuesConfig(name, value)
                    name, value = re.findall('vdom=.+?(?=:)', line)[0].split('='); inputValuesConfig(name, value)
                    name, value = re.findall('user=\w+', line)[0].split('='); inputValuesConfig(name, value)
                # Parsing and getting information about the configuration file version and buildnumber
                if line.startswith(tuple(['#conf_file_ver=', '#buildno=', '#global_vdom='])):
                    name, value = line.replace('#', '').replace('\n', '').split('='); inputValuesConfig(name, value)
                if app.config["DEBUG"]: print("leeg/comment")
                continue

            # Start of the actual parsing

            # Keeps track of the indentation of the configuraiton file, this because fortigate firewallconfiguration files contain multiple "config" statements within one block
            if line.split()[0] == 'end': indentation -= 1
            if line.split()[0] == 'config': indentation += 1
            
            # Checks for the current 'end' and previous 'config' argument so it can be decided that the contents are empty, and skips. 
            if line.split()[0] == 'end' and previous_line[0] == 'config':
                if app.config["DEBUG"]: print("inhoud leeg")
                continue

            # Splits the line into usable variables
            #args = line.split()
            action, *args = line.split()

            # Checks for 'config' as action and also that the argument is viable
            if action == 'config' and args[0] in arguments:
                indentation_name = "" # Clears the indentations so it doesn't get used in the loop
                if indentation == 2: indentation_config = args[0] + " "; continue # checks if the indentation is deep enough for a nested 'config' and saves this name in a variable, and skips
                if args[0] == 'system': args.pop(0) # pops the string 'system' form a variable
                head = ' '.join(args)
                
                # Checks if the header not already exists, when false creates an entry using this header
                if head not in fwConf:
                    fwConf[head] = {}
            else:
                pass

            # Checks for 'edit' as action
            if action == 'edit':
                if indentation == 1: indentation_name = "" # clears indentation_name when it is not viable for usage
                if indentation == 2: indentation_name = "(" + indentation_config + unquote(line.split()[1]) + "): "; continue # Saves the nested config name combining this with the argument after 'edit' on the current line 
                section = unquote(' '.join(args)) # joins the arguments, unquotes them and saves it as the section name
                # Checks if the section not already exists, when false creates an entry using this section
                if section not in fwConf.get(head):
                    fwConf[head][section] = {}

            # Checks for 'set' as action
            if action == 'set':
                name  = args.pop(0) # Drops the first word (name) from arguments and saves it in a variable
                # Checks if the previous line started with 'config' and the current section not already exists in the firewall configuration dict
                if previous_line[0] == 'config' and section not in fwConf[head]:
                    section = '1' # Gives a generic value to section
                    fwConf[head][section] = {} # defines section                   

                # Checks for 'password' and 'passwd' as action and the first argument is 'ENC', saves the encrypted password in variable and content
                if action == 'password' or 'passwd' and args[0] == 'ENC': name = name + " " + args[0]; del args[0]
                value = unquote(' '.join(args)) # Unquotes and joins the contents of arguments (the configurtation)
                # If lien starts wit 5 lines (annotating the start of a certificate)
                if value.startswith('-----'):
                    value += " "
                    # Starts a new forloop so the certificate that is written over multiple lines can be parsed
                    for line in configfile:
                        count += 1
                        if line.startswith('-----'): value += " " + ' '.join(line.split()).strip('"'); break
                        else: value += ' '.join(line.split()).strip('"')
                # Finally saves the indentation_name (optional) and name, puts the found value in it
                fwConf[head][section][indentation_name + name] = value

            previous_line = line.split() # saves the current line as the previous line

        else:
            pass

    jsonConfig = json.dumps(fwConf) # Dumps the made dict as a json in a variable
    
    return jsonConfig

    # Checks for empty values/records in json using keys, deletes empty records
def deleteEmpty(jsonConfig):
    jsonObject = json.loads(jsonConfig)
    for k in list(jsonObject):
        try:
            if len(jsonObject[k])<1:
                del jsonObject[k]
                if app.config["DEBUG"]: print(k, "-> is leeg, record verwijderd")
        except: pass
    return jsonObject


def unquote(s):
    # Checks a string for double quotes (at the beginning and end) and removes them,  also replaces two quotes with a space between them with a comma
    # Possible input: "Web Access" "HTTP" "SSH" "Service DNS"
    # Output: Web Access, HTTP, SSH, Service DNS
    if s:
        if (s[0] == s[-1]) and s.startswith(("'", '"')):
            s = s[1:-1].replace('\" \"', ", ")
    return s