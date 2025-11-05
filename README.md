# ZoneSpy
ZoneSpy is a powerful DNS enumeration tool that helps security professionals and network administrators gather comprehensive DNS information about target domains and test for vulnerable DNS zone transfers.

# Description

ZoneSpy is a powerful DNS enumeration tool that helps security professionals and network administrators gather comprehensive DNS information about target domains and test for vulnerable DNS zone transfers.

# installation

git clone https://github.com/Youssefbakrey/ZoneSpy.git

cd ZoneSpy

python zonespy.py 

# Features

· DNS record enumeration (A, AAAA, MX, TXT, NS, CNAME, SOA)                   
                              
· Zone transfer (AXFR) testing                            

. Whois

## Usage
zonespy -d example.com                                        

zonespy -d zonetransfer.me --axfr -s nsztm1.digi.ninja                        
 
zonespy -d example.com --whois
