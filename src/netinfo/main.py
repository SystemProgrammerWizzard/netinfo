import psutil

class Network:
    def __init__(self):
        self.ip = ""
        self.hostname = []
        self.subnet = []
        self.psutil = psutil.net_if_addrs()
        self.port_tcp = []
        self.port_udp = []
        self.get_ip()
        self.get_hostname()
        self.get_open_ports_tcp()
        self.get_open_ports_udp()

    def get_ip(self):
        import socket
        
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        self.ip = s.getsockname()[0]
        s.close()
        return self.ip

    def get_hostname(self):
        import socket
        self.hostname = socket.gethostname()
        return self.hostname
    
    def get_open_ports_tcp(self):
        port = psutil.net_connections(kind="tcp")
        for i in port:
            if i.laddr[0] == self.ip:
                self.port_tcp.append(i.laddr[1])
        return self.port_tcp

    def get_open_ports_udp(self):
        port = psutil.net_connections(kind="udp")
        for i in port:
            if not i.laddr:
                continue  # skip if no local address

            addr, port_num = i.laddr

            if addr in [self.ip, "0.0.0.0", "::"]:
                self.port_udp.append(port_num)
        return self.port_udp
        

    

    def __str__(self):
        lines = []
        lines.append("========================================")
        lines.append("            System Network Info         ")
        lines.append("========================================\n")

        lines.append(f"Hostname: {self.hostname}")
        lines.append(f"Active IP Address: {self.ip}\n")

        lines.append("Network Interfaces:")
        lines.append("-------------------")
        for i in self.psutil:
            lines.append(f"Interface: {i}")
            lines.append(f"  IP Address: {self.psutil[i][0].address}")
            lines.append(f"  Netmask: {self.psutil[i][0].netmask}")
            lines.append(f"  Broadcast: {self.psutil[i][0].broadcast}\n")
        lines.append("----------------------------------------")

        lines.append("Active Connections:")
        lines.append("----------------------------------------")
        lines.append("Local Address\t\t\tPort\t\tStatus")
        lines.append("-----------------------------------------------------")
        for i in self.port_tcp:
            lines.append(f"{self.ip}:{i}\t\t{i}\t\tEstablished")

        lines.append("-------------------")
        lines.append("Active UDP Connections:")
        lines.append("-------------------")
        lines.append("Local Address\t\t\tPort\t\tStatus")
        lines.append("-----------------------------------------------------")
        for i in self.port_udp:
            lines.append(f"{self.ip}:{i}\t\t{i}\t\tLISTENING")

        lines.append("========================================\n")

        return "\n".join(lines)


def main():
    print("Welcome to netinfo!")
    network = Network()
    print(network)


if __name__ == "__main__":
    main()