from datetime import datetime

def monitor_logs():
    print("\n[*] SOC Log Monitor (Simulated)")
    print("[*] Method: Read sample logs (educational)\n")

    # Example: fake log entries
    logs = [
        {"timestamp": "2026-01-22 10:15", "event": "User login success"},
        {"timestamp": "2026-01-22 10:20", "event": "Failed login attempt"},
        {"timestamp": "2026-01-22 10:30", "event": "Suspicious IP detected"},
    ]

    for log in logs:
        print(f"{log['timestamp']} - {log['event']}")

    print(f"\n[*] Total logs analyzed: {len(logs)}")
    print(f"Timestamp: {datetime.now()}")
