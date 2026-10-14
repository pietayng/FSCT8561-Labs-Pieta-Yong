from scapy.all import rdpcap, IP, TCP, UDP

packets = rdpcap("botnet-capture-20110812-rbot.pcap")

tcp_count = 0
udp_count = 0
shown = 0

for pkt in packets:
    if IP in pkt:
        if TCP in pkt:
            tcp_count += 1
            protocol = "TCP"
            sport = pkt[TCP].sport
            dport = pkt[TCP].dport
        elif UDP in pkt:
            udp_count += 1
            protocol = "UDP"
            sport = pkt[UDP].sport
            dport = pkt[UDP].dport
        else:
            continue

        if shown < 20:
            print("Source:", pkt[IP].src,
                  "Destination:", pkt[IP].dst,
                  "Protocol:", protocol,
                  "Source port:", sport,
                  "Destination port:", dport)
            shown += 1

print("Total TCP packets:", tcp_count)
print("Total UDP packets:", udp_count)
