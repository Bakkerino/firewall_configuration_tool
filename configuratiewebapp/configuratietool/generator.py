import json
from configuratietool import app

outputData = []
config = {}

def genFortianalyzer(server, serial):
    outputData.append((f"""config log fortianalyzer setting
 set status enable
 set server \""""  + server +  """\" 
 set serial """ + serial + """
end\n"""))
    outputData.append("Fortianalyzer is aangezet, met server: " + server + " en serial: " + serial)
    return outputData

def inputBestandVerwerking(bestandsnaam):
    with open(app.config["CFG_UPLOADS"] + bestandsnaam) as fh:
        print(fh)
        arguments = ['system', 'vpn', 'user', 'vdom', 'firewall', 'voip', 'web-proxy', 'application', 'dlp', 'webfilter']
        config = {}
        previous_line = []
        section = ""
        count = 0
        for line in fh:
            count += 1
            current_line = line.split()
            print("-------------------")
            #print("Previous line: >", previous_line)
            #print("Current line: >", current_line)
            if line[0] in ("#", "\n"):
                print("leeg of comment")
                continue
            args = line.split()
            action, *args = line.split()

            if action == 'config' and args[0] in arguments:
                #print(args)
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
            # Waardes
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
    verwerktbestand = json.dumps(config, indent=4)
    #print(verwerktbestand)    
    return verwerktbestand