import dns.resolver
import time
from rich.console import Console
from rich.table import Table
import dns.exception
import dns.query
import dns.zone
import argparse
import pyfiglet
import whois
from colorama import Fore, Style
console = Console()

DNS_LOOKUP = ["A","AAAA","MX","CNAME","NS","SOA","PTR","TXT"]

def dns_lookup(domin_lookup,type=None,server=None):
    banner=pyfiglet.figlet_format("ZoneSpy")
    print(f"{Fore.BLUE}{banner}{Style.RESET_ALL}")
    print(f"{Fore.BLUE}Developed by : Bakrey {Style.RESET_ALL}")
    resolver = dns.resolver.Resolver()
    if server:
        resolver.nameservers = [server]
    if type in DNS_LOOKUP:
        records = type
    else :
        records = DNS_LOOKUP
    table = Table(title=f"Dns records for {domin_lookup}")
    table.add_column("Record type", style="cyan")
    table.add_column("Result", style="magenta")
    table.add_column("Time (ms)", style="green")

    for rtype in records:
        try :
            start_time = time.time()
            data = resolver.resolve(domin_lookup, rtype)
            res = ""
            for i in data:
                res += str(i) + "\n"
            res = res.strip() + "\n"
            end_time = time.time()
            result_time = round((end_time - start_time)*1000 , 2)
            table.add_row(rtype , res , str(result_time) )
        except dns.resolver.NoAnswer :
            table.add_row(rtype, "No Found \n ")
        except dns.resolver.NXDOMAIN :
            console.print(f"[red]Error: {domin_lookup} NOT Found[/red]")
            return
        except Exception as e :
            table.add_row(rtype,f"Error - {e} \n ")
    console.print(table)
def dns_axfr(domain, server):
    try:
        try:
            ip = dns.resolver.resolve(server, 'A')[0].to_text()
            print(f"[+] Resolved {server} → {ip}")
        except Exception as e:
            print(f"[-] Failed to resolve {server}, using it as-is")
            ip = server

        zone_transfer = dns.query.xfr(ip, domain)
        zone = dns.zone.from_xfr(zone_transfer)
        if not zone:
            print("Zone not found")
            return
        for name, node in zone.nodes.items():
            print(f"{name} : {node.to_text(name)}")

    except dns.exception.DNSException as e:
        print(f"after valid : {e}")
    except Exception as e:
        print(f"Unexpected Error : {e}")


def whois_whois(domin_lookup):
    try :
        w = whois.whois(domin_lookup)
        print(f"Domain: {domin_lookup} \n")
        print(f"Registrar : {w.registrar}\n")
        print(f"Name Server : {w.name_servers}\n")
        print(f"Emails : {w.emails}\n")
        print(f"Creation date : {w.creation_date}\n")
        print(f"Expiration date : {w.expiration_date}\n")
        print(f"Status : {w.status}\n")
    except Exception as e:
        print(f"Error : {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='DNS Lookup Tool')
    parser.add_argument("-d", "--domain",nargs="+",required=True, help="Domain(s) Name")
    parser.add_argument("-t", "--type",help="DNS Type(A,AAAA,MX,CNAME,NS,SOA,PTR,TXT) default : all")
    parser.add_argument("-s", "--server",help="Dns Server" ,default=None)
    parser.add_argument("--axfr",action="store_true",help="Zone transfer(AXFR)")
    parser.add_argument("--whois",action="store_true",help="Zone transfer(WHOIS)")
    args = parser.parse_args()
    for domain in args.domain:
        if args.axfr:
            if not args.server:
                print("AXFR requires --server")
            else:
                dns_axfr(domain, args.server)
        elif args.whois:
            whois_whois(domain)

        else:
            dns_lookup(domain, args.type,args.server)
