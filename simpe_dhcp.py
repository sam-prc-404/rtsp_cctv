from scapy.all import *
from scapy.layers.dhcp import DHCP, BOOTP
from scapy.layers.inet import UDP, IP
from scapy.layers.l2 import Ether

# Configuration
INTERFACE = "enp2s0"
SERVER_IP = "192.168.1.1"  # Your machine's IP
OFFERED_IP = "192.168.1.66"  # IP to assign to clients
SUBNET_MASK = "255.255.255.0"
GATEWAY = SERVER_IP  # Clients will use 1.1 as gateway
DNS_SERVER = SERVER_IP  # Clients will use 1.1 as DNS

LEASES = {}  # Store assigned MACs

def handle_dhcp(pkt):
    if pkt.haslayer(DHCP) and pkt.haslayer(BOOTP):
        mac = pkt[Ether].src
        xid = pkt[BOOTP].xid  # Transaction ID

        if pkt[DHCP].options[0][1] == 1:  # DHCPDISCOVER
            print(f"[+] Received DHCPDISCOVER from {mac}")
            LEASES[mac] = OFFERED_IP

            offer = Ether(dst=mac) / IP(src=SERVER_IP, dst="255.255.255.255") / \
                    UDP(sport=67, dport=68) / BOOTP(op=2, yiaddr=OFFERED_IP, xid=xid, chaddr=mac) / \
                    DHCP(options=[("message-type", "offer"),
                                  ("server_id", SERVER_IP),
                                  ("subnet_mask", SUBNET_MASK),
                                  ("router", GATEWAY),
                                  ("name_server", DNS_SERVER),
                                  "end"])
            sendp(offer, iface=INTERFACE, verbose=False)
            print(f"[+] Sent DHCPOFFER: {OFFERED_IP} to {mac}")

        elif pkt[DHCP].options[0][1] == 3:  # DHCPREQUEST
            print(f"[+] Received DHCPREQUEST from {mac}")
            if mac in LEASES:
                ack = Ether(dst=mac) / IP(src=SERVER_IP, dst="255.255.255.255") / \
                      UDP(sport=67, dport=68) / BOOTP(op=2, yiaddr=OFFERED_IP, xid=xid, chaddr=mac) / \
                      DHCP(options=[("message-type", "ack"),
                                    ("server_id", SERVER_IP),
                                    ("subnet_mask", SUBNET_MASK),
                                    ("router", GATEWAY),
                                    ("name_server", DNS_SERVER),
                                    "end"])
                sendp(ack, iface=INTERFACE, verbose=False)
                print(f"[+] Sent DHCPACK: {OFFERED_IP} to {mac}")

print(f"[*] DHCP Server running on {INTERFACE}, offering {OFFERED_IP}...")
sniff(filter="udp and (port 67 or 68)", prn=handle_dhcp, store=0, iface=INTERFACE)
