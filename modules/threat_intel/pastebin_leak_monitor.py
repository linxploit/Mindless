import requests

def pastebin_monitor(query):
    print("\n[*] Pastebin/Leak Monitor (OSINT-safe)")
    print("[*] Method: Public search simulation\n")

    try:
        response = requests.get(f"https://pastebin.com/search?q={query}", timeout=10)
        if query.lower() in response.text.lower():
            print(f"[!] Query '{query}' found in recent public pastes (possible leak)")
        else:
            print(f"[-] Query '{query}' not found in public pastes")
    except Exception as e:
        print(f"[!] Error: {e}")
