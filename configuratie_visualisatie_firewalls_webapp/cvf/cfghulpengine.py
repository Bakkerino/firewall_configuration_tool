def genFortianalyzer(server, serial):
    outputData = []
    outputData.append((f"""config log fortianalyzer setting
 set status enable
 set server \""""  + server +  """\" 
 set serial """ + serial + """
end\n"""))
    outputData.append("Fortianalyzer is aangezet, met server: " + server + " en serial: " + serial)
    return outputData

