# JTDX-controller
A small python script to control JTDX on JTAlerts

Functionality:
Call a station when an Alert is received from JTAlert

Requires: 
Python, pywsjtx, scapy, numpy

Settings:
-JTDX UDP port
-Loopback adapter name to sniff for JTDX packets
-JTDX should be set to 1QSO and locked Tx=Rx.

Installation:
pip install numpy
pip install scapy
Set JTDX to send UDP on 127.0.0.1 2237 (default)
Set JTALERT to re-broadcast UDP on 2334 (default port)
Create a .bat file that is called from JTAlert via custom alert. The .bat file should call the python script. Environmental variables are passed from JTAlert to python.
The content of .bat file should look like this -> start cmd /c python.exe "C:\Users\user\Desktop\call_alert.py"
Configure JTALERT for custom alerts to run BAT file
