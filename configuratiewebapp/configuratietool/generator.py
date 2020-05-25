
outputData = []

def genFortianalyzer(server, serial):
    outputData.append((f"""config log fortianalyzer setting
 set status enable
 set server \""""  + server +  """\" 
 set serial """ + serial + """
end\n"""))
    outputData.append("Fortianalyzer is aangezet, met server: " + server + " en serial: " + serial)
    return outputData

def inputBestandVerwerking(bestand):
    verwerktbestand = "### VERWERKING ###" + "\n\n"
    for line in bestand.splitlines():
        ## Hier kan het bestand geanalyseerd worden per regellijn
        

        verwerktbestand += (line + "\n") 
    else:
        pass
    return verwerktbestand