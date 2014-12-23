#!/usr/bin/python
#
# Name: 
#	cStalker.py
#
# Description: 
#		Proof of Concept - user tracking via wireless in corporate environment using Cisco Wireless LAN Controllers and SNMP.
# 		Idea unashamedly stolen from Sensepost's Snoopy
#
# Initial Date: 
#		28/10/2014
# ChangeLog: 
#		v0.1 - initial release
# 
# Notes: 
#	Requires net-snmp's python bindings. To install the bindings:
#			
#	1. download net-snmp
#	2. configure && make install
# 	3. change to the python folder
# 	4. python setup build
# 	5. python setup install
# 	6. apt-get install snmp-mibs-downloader
#
# 	To replicate via native SNMP:
#
# 		Unique_OID = snmpwalk -v 2c -O x -c $snmp_community $snmp_host 1.3.6.1.4.1.14179.2.1.4.1.1
# 		Client_IP = snmpwalk -v 2c -c $snmp_community $snmp_host 1.3.6.1.4.1.14179.2.1.4.1.2
# 		Client_Username = snmpwalk -v 2c -c $snmp_community $snmp_host 1.3.6.1.4.1.14179.2.1.4.1.3
# 		Client_AP = snmpwalk -v 2c -O x -c $snmp_community $snmp_host 1.3.6.1.4.1.14179.2.1.4.1.4
# 		Client_SSID = snmpwalk -v 2c -c $snmp_community $snmp_host 1.3.6.1.4.1.14179.2.1.4.1.7
# 		WLC_Name =  snmpwalk -v 2c -c $snmp_community $snmp_host 1.3.6.1.2.1.1.5.0
# 		WLC_Location =  snmpwalk -v 2c -c $snmp_community $snmp_host 1.3.6.1.2.1.1.6.0




import netsnmp
import binascii
import sqlite3 as lite
import sys
import time
import argparse

def getsnmp(h):

        id = netsnmp.VarList(netsnmp.Varbind('.1.3.6.1.4.1.14179.2.1.4.1.1'))
        wlc_name = netsnmp.VarList(netsnmp.Varbind('.1.3.6.1.2.1.1.5.0'))
        client_ap_mac = netsnmp.VarList(netsnmp.Varbind('.1.3.6.1.4.1.14179.2.1.4.1.4'))
        client_mac = netsnmp.VarList(netsnmp.Varbind('.1.3.6.1.4.1.14179.2.1.4.1.1')) 	
        client_username = netsnmp.VarList(netsnmp.Varbind('.1.3.6.1.4.1.14179.2.1.4.1.3'))
        client_SSID = netsnmp.VarList(netsnmp.Varbind('.1.3.6.1.4.1.14179.2.1.4.1.7'))

        wlc_uid = netsnmp.snmpwalk(id,DestHost=h, Version=2, Community=Community )
        uid=[]
        for i in wlc_uid:
                y = [binascii.b2a_hex(x) for x in i]
                z = ":".join(y)			
                uid.append(z)

        session = netsnmp.Session(DestHost=h,Version=2,Community=Community)
        vars = netsnmp.VarList(netsnmp.Varbind('.1.3.6.1.2.1.1.5.0'))
        wlc = session.get(vars)


        ap_mac = netsnmp.snmpwalk(client_ap_mac, DestHost=h, Version=2, Community=Community )
        ap=[]
        for i in ap_mac:
                mac = [binascii.b2a_hex(x) for x in i]
                s = ":".join(mac)			
                ap.append(s)

        c_mac = netsnmp.snmpwalk(client_mac, DestHost=h, Version=2, Community=Community )
        cmac=[]
        for i in c_mac:
                mac = [binascii.b2a_hex(x) for x in i]
                t = ":".join(mac)			
                cmac.append(t)

        users = netsnmp.snmpwalk(client_username, DestHost=h, Version=2, Community=Community )
        uname = []
        for username in users:
                uname.append(username)

        bssid = netsnmp.snmpwalk(client_SSID, DestHost=h, Version=2, Community=Community )
        ssid = []
        for w in bssid:
                ssid.append(w)

#	Check count of each list, and use the lowest to loop through and populate db - required as sometimes I see more 
#	entries for one particular oid than others, and then you get an 'List Index out of index' error. I would expect oid's
#	to match espically against uid but it doesn't :-( Probably my code but this seems as good work around as any
#	and probably doesn't loose too many devices.

        count1 = len(uid)
        count2 = len(ap)
        count3 = len(cmac)
        count4 = len(uname)
        count5 = len(ssid)
        l = min(count1,count2,count3,count4,count5)

        i = 0
        while i < l:
                one = time.strftime('%Y%m%d%H%M')
                two = wlc[0]
                three = ap[i]
                four =  cmac[i]
                five = uname[i]
                six = ssid[i]			
                conn.execute("INSERT INTO cstalker VALUES (?, ?, ?, ?, ?, ?);", (one, two, three, four, five, six))
                i += 1	
        conn.commit()




if __name__ == '__main__':
        con = None


        try:
                parser = argparse.ArgumentParser()
                parser.add_argument('-c', action='store', dest='community', required=False, default='Public', help='SNMP Community with read access, default is Public')
                parser.add_argument('-d', action='store', dest='db', required=False, default='cstalker.db', help='Database name, default is cStalker')		
                parser.add_argument('-f', action='store', dest='filename', required=True, help='File with list of Wireless LAN Controller IP Addresses')
                args = parser.parse_args()
                wlclist = args.filename
                Community = args.community
                dbname = args.db

                print 'Setting up Database...'

                try:
                        conn = lite.connect(dbname)  
                        conn.execute('''CREATE TABLE IF NOT EXISTS cstalker(Date, WLC_Name, Access_Point, MAC_Address, Username, SSID)''')	    		
                        #echo "sqlite:///`pwd`/cstalker.db" > ./transforms/db_path.conf 
                        print 'Done'

                except lite.Error, e:
                        print "Oh no, it sucks to be you - Database Error %s:" % e.args[0]
                        sys.exit(1)


                while True:
                        try:						
                                print 'Reading List of WLC IP Addresses...'		
                                file = open(wlclist, "r")
                                for text in file.readlines():
                                        ip = text.rstrip()
                                        print 'Polling WLC: ', ip			
                                        getsnmp(ip)   	
                                print 'Sleeping 5 minutes'
                                time.sleep(300)
                        except KeyboardInterrupt:
                                print 'OK, Quiting...\n'
                                print 'Saving db...'
                                conn.commit()
                                print 'Saved!...\n'
                                file.close()
                                print 'Bye'
                                sys.exit()

                        finally:
                                file.close()

        except IOError, (errno, strerror):
                print "Oh no, it sucks to be you - I/O Error(%s) : %s" % (errno, strerror)
                sys.exit(1)







