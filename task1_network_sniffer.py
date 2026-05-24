"""
Task 1: Basic Network Sniffer
Arch Technologies - Cyber Security Internship
Description: Captures and analyzes network packets using scapy
"""

from scapy.all import sniff, IP, TCP, UDP, ICMP, Raw
import datetime
import sys


LOG_FILE = "network_capture.log"


def analyze_packet(packet):
    """Analyze and log each captured packet."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"\n[{timestamp}]\n"

    # Check if packet has IP layer
    if packet.haslayer(IP):
        ip_layer = packet[IP]
        log_entry += f"  Source IP     : {ip_layer.src}\n"
        log_entry += f"  Destination IP: {ip_layer.dst}\n"
        log_entry += f"  TTL           : {ip_layer.ttl}\n"

        # TCP Packet
        if packet.haslayer(TCP):
            tcp_layer = packet[TCP]
            log_entry += f"  Protocol      : TCP\n"
            log_entry += f"  Src Port      : {tcp_layer.sport}\n"
            log_entry += f"  Dst Port      : {tcp_layer.dport}\n"
            log_entry += f"  Flags         : {tcp_layer.flags}\n"

        # UDP Packet
        elif packet.haslayer(UDP):
            udp_layer = packet[UDP]
            log_entry += f"  Protocol      : UDP\n"
            log_entry += f"  Src Port      : {udp_layer.sport}\n"
            log_entry += f"  Dst Port      : {udp_layer.dport}\n"

        # ICMP Packet
        elif packet.haslayer(ICMP):
            log_entry += f"  Protocol      : ICMP (Ping)\n"

        else:
            log_entry += f"  Protocol      : Other IP\n"

        # Raw payload preview
        if packet.haslayer(Raw):
            raw_data = packet[Raw].load
            try:
                decoded = raw_data[:80].decode("utf-8", errors="replace")
                log_entry += f"  Payload (80B) : {decoded}\n"
            except Exception:
                log_entry += f"  Payload       : [Binary Data]\n"

    else:
        log_entry += "  Layer         : Non-IP packet (ARP, Ethernet, etc.)\n"

    log_entry += "-" * 60

    # Print to console
    print(log_entry)

    # Write to file
    with open(LOG_FILE, "a") as f:
        f.write(log_entry + "\n")


def start_sniffer(packet_count=20, interface=None):
    """
    Start the network sniffer.
    :param packet_count: Number of packets to capture (0 = infinite)
    :param interface: Network interface (None = auto-detect)
    """
    print("=" * 60)
    print("   BASIC NETWORK SNIFFER - Arch Technologies")
    print("   Cyber Security Internship - Task 1")
    print("=" * 60)
    print(f"[*] Capturing {packet_count} packets...")
    print(f"[*] Logs saved to: {LOG_FILE}")
    print("[*] Press Ctrl+C to stop\n")

    # Write header to log file
    with open(LOG_FILE, "a") as f:
        f.write(f"\n{'='*60}\n")
        f.write(f"Capture Session: {datetime.datetime.now()}\n")
        f.write(f"{'='*60}\n")

    try:
        sniff(
            prn=analyze_packet,         # Callback for each packet
            count=packet_count,         # 0 = capture indefinitely
            iface=interface,            # None = scapy picks default
            store=False                 # Don't store in memory
        )
    except KeyboardInterrupt:
        print("\n[!] Sniffing stopped by user.")
    except PermissionError:
        print("[ERROR] Run this script as Administrator/root.")
        sys.exit(1)

    print(f"\n[*] Capture complete. Log saved to: {LOG_FILE}")


if __name__ == "__main__":
    # Capture 20 packets on default interface
    # Change count=0 for continuous capture
    # Change interface="eth0" or "Wi-Fi" for specific interface
    start_sniffer(packet_count=20, interface=None)
