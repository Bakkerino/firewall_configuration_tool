import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
import socket
import struct


form = tk.Tk()
form.title("Configuratiehulp Firewalls")
form.geometry("400x530")

tab_hoofd = ttk.Notebook(form)

tabInput = ttk.Frame(tab_hoofd)
tabOutput = ttk.Frame(tab_hoofd)

tab_hoofd.add(tabInput, text="Input")
tab_hoofd.add(tabOutput, text="Output")


## UITVOEREN ##
def uitvoeren():

    outputMEM = []
    inputIp1 = inputIpAdress1.get()
    inputIpCIDR1 = prefixBox1.get()
    inputIp2 = inputIpAdress2.get()
    inputIpCIDR2 = prefixBox2.get()
    inputDHCP = inputDHCPAdress.get().split("-")

    DNS = DNScheck.get()
    NTP = NTPcheck.get()
    FORTIANALYZER = FORTIANALYZERcheck.get()
    DHCPserver = DHCPSERVERcheck.get()

    def configIpAdress1(portint, mode):
        
        
        if mode == "static": outputMEM.append(f"""config system interface
edit """ + "port"+str(portint) + """
 set alias "INTERNET"
 set ip """ + str(inputIp1) + " " + str(socket.inet_ntoa(struct.pack('!I', (1 << 32) - (1 << (32 - int(inputIpCIDR1[1:])))))) + """
 append allowaccess https ssh
end\n""")
        else: outputMEM.append(f"""config system interface
edit """ + "port"+str(portint) + """
 set alias "INTERNET"
 set mode dhcp
 append allowaccess https ssh
end\n""")

    def configIpAdress2(portint):

        outputMEM.append(f"""config system interface
edit """ + "port"+str(portint) + """
 set alias "LAN"
 set ip """ + str(inputIp2) + " " + str(socket.inet_ntoa(struct.pack('!I', (1 << 32) - (1 << (32 - int(inputIpCIDR2[1:])))))) + """
 append allowaccess ping https ssh http fgfm
end\n""")

    def configDNS():
        outputMEM.append(f"""config system dns
 set primary 1.1.1.1
 set secondary 8.8.8.8
end\n""")

    def configNTP():
        outputMEM.append(f"""config system ntp
 set server 0.nl.pool.ntp.org
 set status enable
end\n""")

    def configFortiAnalyzer():
        outputMEM.append(f"""config log fortianalyzer setting
 set status enable
 set server "fortianalyzer.arrix.nl"
 set serial "FAZ-VMTM20001206"
end\n""")

    def configDHCPserver():
        outputMEM.append(f"""config system dhcp server
edit 1
 set forticlient-on-net-status disable
 set dns-service default
 set default-gateway """+ str(inputIp2) + """
 set netmask """ + str(socket.inet_ntoa(struct.pack('!I', (1 << 32) - (1 << (32 - int(inputIpCIDR2[1:])))))) + """
 set interface "port2"
 config ip-range
     edit 1
         set start-ip """ + inputDHCP[0] + """
         set end-ip """ + inputDHCP[1] + """
     end
end\n""")

    if inputIp1 != "" and inputIpCIDR1 != "": configIpAdress1(1, "static")
    if inputIp1 == "" and inputIpCIDR1 == "": configIpAdress1(1, "dhcp")
    if inputIp2 != "" and inputIpCIDR2 != "": configIpAdress2(2)
    if DNS == 1: configDNS()
    if NTP == 1: configNTP()
    if FORTIANALYZER == 1: configFortiAnalyzer()
    if DHCPserver == 1 and inputIpCIDR2 != "": configDHCPserver()

## configuratiebestand ##
    def schrijfConfig():
        configTekstBox.delete('1.0',tk.END)

        for i in range(len(outputMEM)):
            configTekstBox.insert(tk.INSERT, str(outputMEM[i]) + "\n")
            i += 1
## Tablad Output ##
    schrijfConfig()
    return configTekstBox

def schrijfConfigBestand():
    configTekstBox = uitvoeren()
    bestand = open("configuratie.log","w+")
    bestand.write(configTekstBox.get("1.0","end-1c"))



## Tablad Input ##
labelIp1 = tk.Label(tabInput, text="WAN IP (port1): ")
labelIp1.place(x=8, y=10)
inputIpAdress1 = tk.Entry(tabInput)
inputIpAdress1.place(x=100, y=10)
prefixBox1 = ttk.Combobox(tabInput,values=["/20","/21","/22","/23","/24","/25","/26","/27","/28","/29","/30"], postcommand=uitvoeren, width = 5)
prefixBox1.place(x=230, y=10)

labelIp2 = tk.Label(tabInput, text="LAN IP (port2): ")
labelIp2.place(x=8, y=45)
inputIpAdress2 = tk.Entry(tabInput)
inputIpAdress2.place(x=100, y=45)
prefixBox2 = ttk.Combobox(tabInput,values=["/20","/21","/22","/23","/24","/25","/26","/27","/28","/29","/30"], postcommand=uitvoeren, width = 5)
prefixBox2.place(x=230, y=45)

labelDHCP = tk.Label(tabInput, text="DHCP: ")
labelDHCP.place(x=8, y=68)
inputDHCPAdress = tk.Entry(tabInput)
inputDHCPAdress.place(x=100, y=70)


labelDNS = tk.Label(tabInput, text="DNS: ")
labelDNS.place(x=290, y=80)
DNScheck = tk.IntVar()
inputBox = tk.Checkbutton(tabInput, variable=DNScheck, onvalue=1, offvalue=0)
inputBox.place(x=315, y=80)

labelNTP = tk.Label(tabInput, text="NTP: ")
labelNTP.place(x=340, y=80)
NTPcheck = tk.IntVar()
inputBox = tk.Checkbutton(tabInput, variable=NTPcheck, onvalue=1, offvalue=0)
inputBox.place(x=365, y=80)

labelFortianalyzer = tk.Label(tabInput, text="FORTIANALYZER")
labelFortianalyzer.place(x=290, y=105)
FORTIANALYZERcheck = tk.IntVar()
inputBox = tk.Checkbutton(tabInput, variable=FORTIANALYZERcheck, onvalue=1, offvalue=0)
inputBox.place(x=325, y=120)

DHCPSERVERcheck = tk.IntVar()
inputBox = tk.Checkbutton(tabInput, variable=DHCPSERVERcheck, onvalue=1, offvalue=0)
inputBox.place(x=70, y=68)

configTekstBox = tk.Text(tabOutput, height = 30, width = 45)
configTekstBox.pack()


button = tk.Button(tabInput, text="Uitvoeren", command=uitvoeren)
button.place(x=315, y=10)
buttonExport = tk.Button(tabInput, text="Export", command=schrijfConfigBestand)
buttonExport.place(x=315, y=45)

tab_hoofd.pack(expand=1, fill='both')

form.mainloop()