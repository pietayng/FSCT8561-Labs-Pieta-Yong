from scapy.all import rdpcap, IP, TCP, UDP

packets = rdpcap("botnet-capture-20110812-rbot.pcap")

timestamps = {}
alerted = set()
tcp_count = 0
udp_count = 0

for pkt in sorted(packets, key=lambda pkt: float(pkt.time)):
    if IP in pkt and (TCP in pkt or UDP in pkt):
        if TCP in pkt:
            tcp_count += 1
        else:
            udp_count += 1

        ip = pkt[IP].src
        time = float(pkt.time)

        if ip not in timestamps:
            timestamps[ip] = []

        timestamps[ip] = [t for t in timestamps[ip]
                          if time - t <= 5]
        timestamps[ip].append(time)

        if len(timestamps[ip]) > 20 and ip not in alerted:
            print("ALERT: Suspicious traffic from", ip)
            alerted.add(ip)

print("Total TCP packets:", tcp_count)
print("Total UDP packets:", udp_count)
print("Suspicious IPs:", len(alerted))
