import os
import time

import phonenumbers
import pyfiglet
from googlesearch import search
from phonenumbers import carrier, timezone
from phonenumbers.phonenumberutil import region_code_for_number
from requests.exceptions import HTTPError

print("\n")
Ascii_Art = pyfiglet.figlet_format("PhoNumSpy")
print(Ascii_Art)
version = "Version 1.1"
print(version)
print("\n")
time.sleep(1)

maininput = input(
    "Input the target phone number using this format: +(prefix)(phonenumber) "
    "ES: +447455869664\n-->"
).strip()

lookuptarget = maininput.lstrip("+")
fileoutput = open(f"{maininput}_results.txt", "w", encoding="utf-8")

fileoutput.write("\n")
fileoutput.write(Ascii_Art)
fileoutput.write("\n\n")
fileoutput.write(version)
fileoutput.write("\n\n")

print("\n-------------------------")
print("Target:" + maininput)
print("-------------------------\n")
print("Processing...\n")

fileoutput.write("-------------------------\n")
fileoutput.write(f"Target: {maininput}\n")
fileoutput.write("-------------------------\n\n")
fileoutput.write("Processing...\n\n")

print("-------------------------")
print("Phone Number Informations")
print("-------------------------\n")

try:
    target = phonenumbers.parse(maininput, None)
except phonenumbers.NumberParseException as exc:
    print(f"[-] Invalid phone number: {exc}")
    fileoutput.write(f"[-] Invalid phone number: {exc}\n")
    fileoutput.close()
    raise SystemExit(1)

TZ = timezone.time_zones_for_number(target)
CC = region_code_for_number(target)
CR = carrier.name_for_number(target, "en")

print("Location: ", TZ)
print("Country Code: ", CC)
print("Carrier: ", CR)

fileoutput.write("-------------------------\n")
fileoutput.write("Phone Number Informations\n")
fileoutput.write("-------------------------\n\n")
fileoutput.write(f"Location: {TZ}\n")
fileoutput.write(f"Country Code: {CC}\n")
fileoutput.write(f"Carrier: {CR}\n\n")


def safe_search(query, num_results=10, sleep_interval=3, region=None):
    """Run a Google search without crashing the program on rate limits."""
    try:
        return list(
            search(
                query,
                num_results=num_results,
                sleep_interval=sleep_interval,
                region=region,
            )
        )
    except HTTPError as exc:
        status = getattr(exc.response, "status_code", None)
        if status == 429:
            print("[!] Google rate limit reached (HTTP 429). Skipping this search.")
            return []
        print(f"[!] Search HTTP error: {exc}")
        return []
    except Exception as exc:
        print(f"[!] Search error: {exc}")
        return []


print("\n--------------------------")
print("Phone Number Web Footprint")
print("--------------------------\n")

fileoutput.write("--------------------------\n")
fileoutput.write("Phone Number Web Footprint\n")
fileoutput.write("--------------------------\n\n")

footprint_results = safe_search(
    lookuptarget,
    num_results=10,
    sleep_interval=3,
    region=(CC.lower() if CC else None),
)

if footprint_results:
    for footprintsearch in footprint_results:
        print(f"[+] Result found on: {footprintsearch}")
        fileoutput.write(f"{footprintsearch}\n")
else:
    print("[-] No web footprint found")
    fileoutput.write("[-] No web footprint found\n")

print("\n--------------------------------------------------")
print("Targeted Searches on Online Phone Number Providers")
print("--------------------------------------------------\n")

fileoutput.write("\n------------------------------------------------\n")
fileoutput.write("Targeted Searches on Online Phone Number Providers\n")
fileoutput.write("------------------------------------------------\n\n")

try:
    with open("websites.txt", "r", encoding="utf-8") as extractedwebsites:
        varwebsites = [line.strip() for line in extractedwebsites if line.strip()]
except FileNotFoundError:
    varwebsites = []
    print("[!] websites.txt was not found. Skipping provider searches.")

found_provider_result = False
for site in varwebsites:
    query = f"allinurl:{site} {lookuptarget}"
    results = safe_search(
        query,
        num_results=1,
        sleep_interval=5,
        region=(CC.lower() if CC else None),
    )

    for querysearch in results:
        print(f"[+] Result found: {querysearch}")
        fileoutput.write(f"{querysearch}\n")
        found_provider_result = True

    # Extra delay between provider queries to reduce the chance of HTTP 429.
    time.sleep(5)

if not found_provider_result:
    print("[-] No result found")
    fileoutput.write("[-] No result found\n")

print("\n")
print(Ascii_Art)
print("\n")

fileoutput.write("\n\n")
fileoutput.write(Ascii_Art)
fileoutput.write("\n\n")
fileoutput.write(version)
fileoutput.write("\n\n")
fileoutput.close()

filepath = os.getcwd()
filename = f"{maininput}_results.txt"
print(f"{maininput} Logs saved in {filepath} as '{filename}'")
