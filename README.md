# JTDX-controller
A small python script to control JTDX on JTAlerts

Functionality:
Call a station when an Alert is received from JTAlert

Requires: 
Python, pywsjtx, scapy

Settings:
-JTDX UDP port
-Loopback adapter name to sniff for JTDX packets
-JTDX should be set to 1QSO and locked Tx=Rx.

How to Run:
Create a .bat file that is called from JTAlert via custom alert. The .bat file should call the python script. Environmental variables are passed from JTAlert to python.
The content of .bat file should look like this -> start cmd /c python.exe "C:\Users\user\Desktop\call_alert.py"
