cStalker
======

SNMP abuse like its the 1990's. Idea unashamedly stolen from Sensepost's Snoopy, and somewhat of an edge case. Rather than tracking probe requests, we're tracking connections to wireless networks in a corporate environment. Turns out you can do this using Cisco Wireless LAN Controllers, since they all ship with a default SNMP community string, and expose client connection details via SNMP

Mock'ed up as POC only (I believe it took me longer to come up with a (so elite and hardcore) name for the script than to code it - so it could probably benefit from some refactoring :-) Maltego transforms included - your need to edit the db connection string and then working directory for the transforms if you want to replicate. If I get time I'll tidy up.

This also probably falls foul of various European privacy / data protection regulations if do this across some European countries so I'm not sure you actually want to implement this in a corporate environment but if you did and you scaled it globally you can get some really nice Maltego maps of which sites your business travelers are traveling to/from.

Tracking travelling users:

![tracking_travels](https://cloud.githubusercontent.com/assets/3184320/5536589/6f8d4480-8a8c-11e4-9a4a-1092af6cdacf.png)

Tracking movement around a campus or building:

![tracking_building](https://cloud.githubusercontent.com/assets/3184320/5536591/724aa050-8a8c-11e4-9e4d-eb38d35da32d.png)