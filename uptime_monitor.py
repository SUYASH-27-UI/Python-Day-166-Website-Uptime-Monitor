
import urllib.request
import urllib.error
import threading
import csv
from datetime import datetime

WEBSITES = [
    "https://www.google.com",
    "https://www.github.com",
    "https://www.wikipedia.org",
    "https://www.python.org",
    "https://example.invalid"
]

results = []
lock = threading.Lock()


def check_website(url):
    start_time = datetime.now()

    try:
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "Python-Uptime-Monitor"}
        )

        with urllib.request.urlopen(request, timeout=5) as response:
            status = response.status
            result = "ONLINE"

    except urllib.error.HTTPError as error:
        status = error.code
        result = "ONLINE (HTTP Error Response)"

    except Exception:
        status = "N/A"
        result = "OFFLINE"

    elapsed = (datetime.now() - start_time).total_seconds()

    record = {
        "url": url,
        "status": status,
        "result": result,
        "response_time": round(elapsed, 2)
    }

    with lock:
        results.append(record)

    print(
        f"{url} | {result} | "
        f"Status: {status} | {elapsed:.2f}s"
    )


def save_report():
    with open("uptime_report.csv", "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "Website",
            "HTTP Status",
            "Result",
            "Response Time"
        ])

        for item in results:
            writer.writerow([
                item["url"],
                item["status"],
                item["result"],
                item["response_time"]
            ])

    print("\nReport saved to uptime_report.csv")


def main():
    print("===== WEBSITE UPTIME MONITOR =====\n")

    threads = []

    for website in WEBSITES:
        thread = threading.Thread(
            target=check_website,
            args=(website,)
        )

        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    online = sum(
        1 for item in results
        if item["result"].startswith("ONLINE")
    )

    offline = len(results) - online

    print("\n===== SUMMARY =====")
    print("Total Websites:", len(results))
    print("Online:", online)
    print("Offline:", offline)

    save_report()


if __name__ == "__main__":
    main()
