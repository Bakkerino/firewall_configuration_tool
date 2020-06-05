import json

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

def inputBestandVerwerking(bestand):
    #verwerktbestand = "### VERWERKING ###" + "\n\n"
    #for line in bestand.splitlines():
        ## Hier kan het bestand geanalyseerd worden per regellijn
    for line in bestand.splitlines():
        print(line.split())
        if line == "" or line[0] == "#":
            print("leeg of comment")
            continue
        args = line.split()
        action, *args = line.split()

        if action == 'config':
            header  = ' '.join(args)
            if header not in config:
                config[header] = {}

        if action == 'edit':
            section = ' '.join(args).strip('"')
            if section not in config[header]:
                config[header][section] = {}

        if action == 'set':
            name  = args.pop(0)
            value = ' '.join(args).strip('"')
            config[header][section][name] = value
    #verwerktbestand += (line + "\n") 
    else:
        pass
    verwerktbestand = json.dumps(config, indent=4)    
    return verwerktbestand