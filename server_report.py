import json


def load_servers(path):
    try:
        with open(path, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: {path} was not found.")
        raise SystemExit(1)
    except json.JSONDecodeError as e:
        print(f"Error: {path} is not valid JSON ({e}).")
        raise SystemExit(1)
    return data["servers"]


def classify(status, cpu):
    if status == "down" or cpu > 80:
        return "CRITICAL"
    elif cpu > 70:
        return "WARNING"
    return "OK"


def write_report(servers, path):
    flagged = 0
    skipped = 0

    with open(path, "w") as report:
        for server in servers:
            try:
                name = server["name"]
                status = server["status"]
                cpu = float(server["cpu"])
            except (KeyError, ValueError, TypeError) as e:
                print(f"Skipping a server, bad data: {e!r}")
                skipped += 1
                continue

            level = classify(status, cpu)
            if level != "OK":
                report.write(f"{name} - CPU {cpu:.0f}% - {status} - {level}\n")
                flagged += 1

        report.write(f"Total flagged: {flagged}\n")

    return flagged, skipped


def main():
    servers = load_servers("servers.json")
    flagged, skipped = write_report(servers, "report.txt")
    print(f"Done. Flagged: {flagged}, skipped: {skipped}")


if __name__ == "__main__":
    main()