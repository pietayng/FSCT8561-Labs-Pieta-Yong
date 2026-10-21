
import requests
import csv

BASE_URL = "http://localhost:3000"
records = []

tests = [
    ("GET", "/", ""),
    ("GET", "/rest/products/search", "apple"),
    ("GET", "/rest/products/search", "banana"),
    ("POST", "/rest/products/search", "apple")
]

for method, endpoint, value in tests:
    try:
        url = BASE_URL + endpoint
        if method == "GET":
            r = requests.get(url, params={"q": value} if value else None, timeout=5)
        else:
            r = requests.post(url, data={"q": value}, timeout=5)

        record = {
            "endpoint": endpoint,
            "method": method,
            "input": value,
            "status_code": r.status_code,
            "response_length": len(r.content),
            "content_type": r.headers.get("Content-Type"),
            "server": r.headers.get("Server")
        }
        records.append(record)
        print(record)

    except requests.RequestException as error:
        print("Could not connect:", error)

with open("http_scan_results.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=[
        "endpoint", "method", "input", "status_code",
        "response_length", "content_type", "server"
    ])
    writer.writeheader()
    writer.writerows(records)
