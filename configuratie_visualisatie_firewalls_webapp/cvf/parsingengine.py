import json
from cvf import app
config = {}



# Parsing engine that can parse fortigate configuration files, the function returns a json dump containing ordened config
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
                if line.startswith('#config-version='):
                    header = "config"; config[header] = {}
                    section = "version"; config[header][section] = {}; 
                    name, value  = line.split('=', 1)[1].replace('-', ' ').replace(':', ', ').split(maxsplit=1)

                    config[header][section][name] = {}
                    config[header][section][name] = value

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

    jsonconfig = json.dumps(config, indent=4)
    
    return jsonconfig