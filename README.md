cStalker
======

SNMP abuse like its the 1990's. Idea unashamedly stolen from Sensepost's Snoopy, and somewhat of an edge case. Rather than tracking probe requests, we're tracking connections to wireless networks in a corporate environment. Turns out you can do this using Cisco Wireless LAN Controllers, since they all ship with a default SNMP community string (come on Cisco it's not 1990 anymore!), and expose all client details via SNMP

Mock'ed up as POC only (I believe it took me longer to come up with a name than to code it - so it could probably benefit from some refactoring :-) Maltego transforms included - your need to edit the db connection string and then working directory for the transforms if you want to replicate.

This also probably falls foul of various European privacy / data protection regulations if do this across some countries so I'm not sure you actually want to implement this in a corporate environment but if you did and you scaled it globally you can get some really nice Maltego maps of which sites your business travelers are traveling to/from: