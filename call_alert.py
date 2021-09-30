import os
import sys
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pywsjtx.extra.simple_server
from scapy.all import *

IP_ADDRESS = '127.0.0.1'
PORT = 2334
udp_sport=0
timeout = time.time() + 60*5

conf.iface="[Unknown] Adapter for loopback traffic capture"
logfile = 'C:\\Users\\user\\AppData\\Local\\JTDX\\wsjtx_log.adi'
def find_port(pkt):
    if UDP in pkt:
        global udp_sport
        udp_sport=pkt[UDP].sport
        print("Found UDP source port: " + str(udp_sport))

s = pywsjtx.extra.simple_server.SimpleServer(IP_ADDRESS, PORT, timeout=2.0)

wsjtx_id = None
dxcall = os.getenv('JTAlert_Call')
dxband = os.getenv('JTAlert_Band')
dxsnr=0
dxdt=0
dxdf=0
dxmode=''
dxmsg=''
dxtime=0
file1 = open("log.txt","a")
file1.write("Alert for: " + str(dxcall) + "\n")
print("Alert for: " + str(dxcall) + "\n")
file1.flush()
sniff(filter = 'dst port 2237', prn=find_port, count=1)
file1.write("UDP source port is: " + str(udp_sport) + "\n")
file1.flush()
#reply_packet = pywsjtx.ReplyPacket.Builder(wsjtx_id, dxtime, dxsnr, dxdt, dxdf, dxmode, dxmsg)
#s.send_packet(('127.0.0.1', udp_sport), reply_packet)
#print("PACKET SENT")
#file1.close()

with open(logfile) as f:
    for line in f:
        if dxcall in line:
            if dxband in line.split()[9]:
                print("Call " + dxcall + " at band " + dxband + " found in log, quiting")
                quit()

while True:

    (pkt, addr_port) = s.rx_packet()
    if time.time() > timeout:
        print("Timeout reached")
        file1.write("Timeout reached\n")
        file1.close()
        break
    if (pkt != None):
        the_packet = pywsjtx.WSJTXPacketClassFactory.from_udp_packet(addr_port, pkt)
        if wsjtx_id is None and (type(the_packet) == pywsjtx.HeartBeatPacket):
            # we have an instance of WSJTX
            print("wsjtx detected, id is {}".format(the_packet.wsjtx_id))
            file1.write("wsjtx detected, id is {}".format(the_packet.wsjtx_id))
            print("starting freq monitoring for " + dxcall)
            file1.flush()
            wsjtx_id = the_packet.wsjtx_id

        if type(the_packet) == pywsjtx.DecodePacket:
            dxmsg = (the_packet.message)
            if len(dxmsg.split()) > 1:
              if (dxmsg.split()[1] == dxcall)  and (dxmsg.split()[0] == "CQ" or dxmsg.split()[2] == "73" or dxmsg.split()[2] == "RR73"):
                dxdf = (the_packet.delta_f)
                dxdt = (the_packet.delta_t)
                dxsnr = (the_packet.snr)
                dxmode = (the_packet.mode)
                dxtime = (the_packet.millis_since_midnight)
                print("Found DX call   " + dxcall)
                print("Delta time      " + str(dxdt))
                print("Delta Frequency " + str(dxdf))
                print("DX mode         " + dxmode)
                print("DX time         " + str(dxtime))
                print("DX msg          " + dxmsg)
                if (wsjtx_id != None):
                    reply_packet = pywsjtx.ReplyPacket.Builder(wsjtx_id, dxtime, dxsnr, dxdt, dxdf, dxmode, dxmsg)
                    s.send_packet(('127.0.0.1', udp_sport), reply_packet)
                    print("PACKET SENT")
                    file1.write(str(wsjtx_id) + " " + str(dxtime) + " " + str(dxsnr) + " " + str(dxdt) + " " + str(dxdf) + " " + str(dxmode) + " " + str(dxmsg) + "\n")
                    #file1.write(str(addr_port))
                    #print(str(addr_port))
                    file1.close()
                    quit()


    #if type(the_packet) == pywsjtx.StatusPacket:


#print(dxcall)
#file1 = open("log.txt","a")
#file1.write(str(dxcall))

