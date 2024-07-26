import requests
import socket
import csv
import argparse

def get_geolocation(ip_address):
    url = f"https://ipinfo.io/{ip_address}/json"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        data = response.json()
        if 'error' in data:
            return {"error": data['error']['info']}
        return data
    except requests.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}

def reverse_dns_lookup(ip_address):
    try:
        host_name = socket.gethostbyaddr(ip_address)
        return host_name[0]
    except socket.herror:
        return "Unknown"

def save_to_csv(data, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["IP", "Country", "Region", "City", "ZIP", "Latitude", "Longitude", "ISP", "Org", "AS", "Timezone", "Currency", "Reverse DNS"])
        for item in data:
            writer.writerow([
                item.get("ip", ""),
                item.get("country", ""),
                item.get("region", ""),
                item.get("city", ""),
                item.get("postal", ""),
                item.get("loc", "").split(",")[0],
                item.get("loc", "").split(",")[1],
                item.get("org", ""),
                item.get("org", ""),
                item.get("as", ""),
                item.get("timezone", ""),
                item.get("currency", ""),
                reverse_dns_lookup(item.get("ip", ""))
            ])

def main():
    parser = argparse.ArgumentParser(description="IP Geolocation Tool")
    parser.add_argument("input", help="IP address or path to a file with IP addresses")
    parser.add_argument("-b", "--batch", action="store_true", help="Enable batch processing")
    parser.add_argument("-o", "--output", help="Output file for batch processing (CSV format)")
    args = parser.parse_args()

    if args.batch:
        if not args.output:
            print("Error: Output file must be specified for batch processing.")
            return
        try:
            with open(args.input, 'r') as file:
                ips = file.read().splitlines()
        except FileNotFoundError:
            print(f"Error: File {args.input} not found.")
            return
        geolocations = []
        for ip in ips:
            data = get_geolocation(ip)
            if "error" in data:
                print(f"Error for IP {ip}: {data['error']}")
            else:
                geolocations.append(data)
        save_to_csv(geolocations, args.output)
        print(f"Batch processing complete. Results saved to {args.output}")
    else:
        ip = args.input
        data = get_geolocation(ip)
        if "error" in data:
            print(f"Error: {data['error']}")
        else:
            print("\nGeolocation Information:\n")
            print(f"IP: {data.get('ip', 'N/A')}")
            print(f"Country: {data.get('country', 'N/A')}")
            print(f"Region: {data.get('region', 'N/A')}")
            print(f"City: {data.get('city', 'N/A')}")
            print(f"ZIP: {data.get('postal', 'N/A')}")
            print(f"Latitude: {data.get('loc', 'N/A').split(',')[0]}")
            print(f"Longitude: {data.get('loc', 'N/A').split(',')[1]}")
            print(f"ISP: {data.get('org', 'N/A')}")
            print(f"Org: {data.get('org', 'N/A')}")
            print(f"AS: {data.get('as', 'N/A')}")
            print(f"Timezone: {data.get('timezone', 'N/A')}")
            print(f"Currency: {data.get('currency', 'N/A')}")
            print(f"Reverse DNS: {reverse_dns_lookup(data.get('ip', 'N/A'))}")

if __name__ == "__main__":
    main()
