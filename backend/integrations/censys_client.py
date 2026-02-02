import requests
from backend.config import CENSYS_API_TOKEN, CENSYS_BASE_URL


class CensysClient:
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {CENSYS_API_TOKEN}",
            "Accept": "application/json"
        }

    def get_host_asset(self, ip):
        url = f"{CENSYS_BASE_URL}/v3/global/asset/host/{ip}"
        r = requests.get(url, headers=self.headers, timeout=20)
        r.raise_for_status()
        return r.json()
