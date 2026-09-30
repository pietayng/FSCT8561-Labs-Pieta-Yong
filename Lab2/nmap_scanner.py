import nmap


scanner = nmap.PortScanner()


target = input("Enter target host: ")


try:
    start_port = int(input("Enter starting port: "))
    end_port = int(input("Enter ending port: "))

except ValueError:
    print("Ports must be numbers.")
    exit()


if start_port < 1 or start_port > 65535:
    print("Starting port must be between 1 and 65535.")
    exit()

if end_port < 1 or end_port > 65535:
    print("Ending port must be between 1 and 65535.")
    exit()

if start_port > end_port:
    print("Starting port cannot be greater than ending port.")
    exit()

if end_port - start_port + 1 > 1000:
    print("Port range cannot exceed 1000 ports.")
    exit()


port_range = str(start_port) + "-" + str(end_port)

print("Scanning", target, "ports", port_range)


try:
    scanner.scan(target, port_range)

    if len(scanner.all_hosts()) == 0:
        print("No hosts found.")

    else:
        for host in scanner.all_hosts():

            print("Host:", host)
            print("Port\tState\tService")

            for protocol in scanner[host].all_protocols():

                ports = scanner[host][protocol].keys()

                for port in sorted(ports):

                    state = scanner[host][protocol][port]["state"]
                    service = scanner[host][protocol][port]["name"]

                    print(
                        str(port)
                        + "\t"
                        + state
                        + "\t"
                        + service
                    )

    print("Scan complete.")

except nmap.PortScannerError:
    print("There was an error running Nmap.")

except Exception:
    print("An error occurred while scanning.")