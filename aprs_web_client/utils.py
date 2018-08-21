from python_arptable import get_arp_table

def mac_for_ip(ip):
    'Returns a list of MACs for interfaces that have given IP, returns None if not found'
    arps = get_arp_table()
    for arp in arps:
        if arp['IP address'] == ip:
            return arp['HW address']

    return None
