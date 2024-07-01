import os, requests, ipaddress, argparse, logging
from concurrent.futures import ThreadPoolExecutor

class Color: GREEN = '\033[92m'; YELLOW = '\033[93m'; RED = '\033[91m'; CYAN = '\033[96m'; BRIGHT = '\033[1m'; RESET = '\033[0m'
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
def clear_screen(): os.system('cls' if os.name == 'nt' else 'clear')
def get_ip_location(ip_address):
    try: return requests.get(f"http://ip-api.com/json/{ip_address}", timeout=10).json()
    except requests.RequestException as e: logger.error(f"Error retrieving information from IP-API: {str(e)}")
def get_proxy_info(ip_address):
    try: return requests.get(f"https://proxycheck.io/v2/{ip_address}?vpn=1&asn=1", timeout=10).json().get(ip_address, {})
    except requests.RequestException as e: logger.error(f"Error retrieving information from ProxyCheck: {str(e)}")
def fetch_info(ip_address):
    with ThreadPoolExecutor() as executor:
        loc, prox = executor.submit(get_ip_location, ip_address), executor.submit(get_proxy_info, ip_address)
        return loc.result(), prox.result()
def display_info(ip_address, loc_info, prox_info):
    if loc_info and loc_info.get("status") == "success":
        print(f"\n{Color.GREEN + Color.BRIGHT}IP: {ip_address}\nCountry: {loc_info.get('country', 'N/A')}\nRegion: {loc_info.get('regionName', 'N/A')}\nCity: {loc_info.get('city', 'N/A')}\nISP: {loc_info.get('isp', 'N/A')}\nLatitude: {loc_info.get('lat', 'N/A')}\nLongitude: {loc_info.get('lon', 'N/A')}\nOrganization: {loc_info.get('org', 'N/A')}")
    if prox_info: print(f"{Color.YELLOW}ASN: {prox_info.get('asn', 'N/A')}\nRange: {prox_info.get('range', 'N/A')}\nProvider: {prox_info.get('provider', 'N/A') if 'provider' in prox_info and 'isp' in loc_info and prox_info['provider'] != loc_info['isp'] else ''}\nContinent: {prox_info.get('continent', 'N/A')}\nContinent Code: {prox_info.get('continentcode', 'N/A')}\nRegion Code: {prox_info.get('regioncode', 'N/A')}\nTimezone: {prox_info.get('timezone', 'N/A')}\nPostcode: {prox_info.get('postcode', 'N/A')}\nCurrency: {prox_info.get('currency', {}).get('name', 'N/A')} ({prox_info.get('currency', {}).get('code', 'N/A')})\nProxy: {prox_info.get('proxy', 'N/A')}\nType: {prox_info.get('type', 'N/A')}\n{Color.RESET}")
    else: print(f"{Color.RED}No proxy information found for IP: {ip_address}")
    input("\nPress Enter to continue...")
def main():
    clear_screen()
    title_art = r"""
     ________     __   ____  ____  __ ____  ______ 
    /  _/ __ \   / /  / __ \/ __ \/ //_/ / / / __ \
    / // /_/ /  / /  / / / / / / / ,< / / / / /_/ /
  _/ // ____/  / /__/ /_/ / /_/ / /| / /_/ / ____/ 
 /___/_/      /_____\____/\____/_/ |_\____/_/      
                                                  
    """
    print(Color.CYAN + title_art + "\n" + f"{Color.YELLOW + Color.BRIGHT}Made by: {' ' * 14}github.com/cr0mb/\n{Color.RED + Color.BRIGHT}{'=' * 40}")
    parser = argparse.ArgumentParser(description="IP Information Lookup")
    parser.add_argument("ip_address", nargs='?', help="The IP address to look up")
    args = parser.parse_args(); ip = args.ip_address.strip() if args.ip_address else None
    if not ip: ip = input(Color.CYAN + Color.BRIGHT + "Please enter the IP address: ").strip()
    try: ipaddress.ip_address(ip); l, p = fetch_info(ip); display_info(ip, l, p)
    except ValueError: print(f"{Color.RED}Invalid IP address: {ip}")
if __name__ == "__main__": main()
