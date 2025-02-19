import socket
import concurrent.futures
import sys

commonPorts = set(range(1, 1001))

def scanPort(ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        result = s.connect_ex((ip, port)) 
        return port if result == 0 else None

def stealthScan(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP) as s:
            s.settimeout(1)
            s.connect((ip, port))
            return port
    except:
        return None

def portScanner(ip, portsToScan, mode="normal"):
    openPorts = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        if mode == "stealth":
            results = executor.map(lambda p: stealthScan(ip, p), portsToScan)
        else:
            results = executor.map(lambda p: scanPort(ip, p), portsToScan)
    openPorts = [port for port in results if port]
    return openPorts

def menu():
    print("\n--- Port Scanner ---")
    print("1. Snelle scan (Top 1000 poorten)")
    print("2. Diepe scan (Alle 65535 poorten)")
    print("3. Stealth scan (SYN-scan, root vereist)")
    print("4. Exit")

    choice = input("Kies een optie: ")
    return choice

if __name__ == "__main__":
    targetIp = input("Voer IP in om te scannen: ")

    while True:
        choice = menu()

        if choice == "1":
            portsToScan = commonPorts
            scanMode = "normal"
        elif choice == "2":
            portsToScan = set(range(1, 65536))
            scanMode = "normal"
        elif choice == "3":
            portsToScan = commonPorts
            scanMode = "stealth"
        elif choice == "4":
            print("Scanner afgesloten")
            sys.exit()
        else:
            print("Ongeldige keuze, probeer opnieuw.")
            continue

        print(f"Scannen van {targetIp} op {len(portsToScan)} poorten...")
        openPorts = portScanner(targetIp, portsToScan, scanMode)

        if openPorts:
            print(f"Open poorten gevonden: {openPorts}")
        else:
            print("Geen open poorten gevonden")
