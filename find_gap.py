import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pywsjtx.extra.simple_server
import numpy as np

IP_ADDRESS = '127.0.0.1'
PORT = 2237

s = pywsjtx.extra.simple_server.SimpleServer(IP_ADDRESS, PORT, timeout=2.0)
timelist = []
wsjtx_id = None

while True:

    (pkt, addr_port) = s.rx_packet()
    if (pkt != None):
        the_packet = pywsjtx.WSJTXPacketClassFactory.from_udp_packet(addr_port, pkt)
        if wsjtx_id is None and (type(the_packet) == pywsjtx.HeartBeatPacket):
            # we have an instance of WSJTX
            print("wsjtx detected, id is {}".format(the_packet.wsjtx_id))
            print("starting freq monitoring")
            wsjtx_id = the_packet.wsjtx_id

        if type(the_packet) == pywsjtx.StatusPacket:
#            print("this is a status packet")
#            print(timelist)
            if timelist:
                timelist.sort()
#                print(timelist)
                timegaplist = []
                gappairlist = []
                for i in range((len(timelist) - 1)):
                        if (( timelist[i] + 50 ) < timelist[i+1] and (timelist[i+1] < 2500)):
                            gappairlist.append([timelist[i], timelist[i+1]])
#                            print("there is a GAP in between " + str(timelist[i]) + " and " + str(timelist[i+1]))
#                print(gappairlist)
                gap = []
                for i in range(len(gappairlist)):
                    gap.append(gappairlist[i][1] - gappairlist[i][0])
                selectedindex = np.argmax(gap)
                selectedpair = gappairlist[selectedindex]
                if (gap[selectedindex] > 50):
                    newtxfreq = int((selectedpair[0] + 50 + ((selectedpair[1] - (selectedpair[0] + 50))/2)))
                    print("New TX freq is: " + str(newtxfreq))
                    if (wsjtx_id != None):
                        newfreq_packet = pywsjtx.SetTxDeltaFreq.Builder(wsjtx_id, newtxfreq ,True)
                        s.send_packet(addr_port, newfreq_packet)

#                print(gappairlist[selectedindex])
            timelist = []
        if type(the_packet) == pywsjtx.DecodePacket:
#            print(the_packet.delta_f)
            timelist.append(the_packet.delta_f)
        print(the_packet)


