import os
import time

import phonenumbers
import pyfiglet
import requests
from phonenumbers import carrier, timezone
from phonenumbers.phonenumberutil import region_code_for_number

BRAVE_ENDPOINT = "https://api.search.brave.com/res/v1/web/search"

print("\n")
Ascii_Art = pyfiglet.figlet_format("PhoNumSpy")
print(Ascii_Art)
version = "Version 1.2"
print(version)
print("\n")
time.sleep(1)

maininput = input(
    "Input the target phone number using this format: +(prefix)(phonenumber) "
    "ES: +447455869664\n-->"
).strip()

lookuptarget = maininput.lstrip("+")
report_name = f"{maininput}_results.txt"
fileoutput = open(report_name, "w", encoding="utf-8")

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

if not phonenumbers.is_possible_number(target):
    print("[-] The supplied phone number is not possible according to numbering-plan metadata.")
    fileoutput.write("[-] The supplied phone number is not possible according to numbering-plan metadata.\n")
    fileoutput.close()
    raise SystemExit(1)

TZ = timezone.time_zones_for_number(target)
CC = region_code_for_number(target)
CR = carrier.name_for_number(target, "en")

print("Location metadata: ", TZ)
print("Country Code: ", CC)
print("Carrier: ", CR or "Unknown / unavailable")

fileoutput.write("-------------------------\n")
fileoutput.write("Phone Number Informations\n")
fileoutput.write("-------------------------\n\n")
fileoutput.write(f"Location metadata: {TZ}\n")
fileoutput.write(f"Country Code: {CC}\n")
fileoutput.write(f"Carrier: {CR or 'Unknown / unavailable'}\n\n")


def brave_search(query, count=10, country=None):
    """Search the public web using Brave Search API.

    Requires BRAVE_SEARCH_API_KEY in the environment. Returns a list of
    dictionaries with title, url and description. If the key is not set or
    the API request fails, an empty list is returned and the program continues.
    """
    api_key = os.getenv("BRAVE_SEARCH_API_KEY", "").strip()
    if not api_key:
        return []

    params = {
        "q": query,
        "count": max(1, min(int(count), 20)),
        "search_lang": "en",
        "safesearch": "moderate",
    }
    if country:
        params["country"] = country.upper()

    headers = {
        "Accept": "application/json",
        "X-Subscription-Token": api_key,
    }

    try:
        response = requests.get(
            BRAVE_ENDPOINT,
            params=params,
            headers=headers,
            timeout=15,
        )
        response.raise_for_status()
        payload = response.json()
    except requests.RequestException as exc:
        print(f"[!] Brave Search API error: {exc}")
        return []
    except ValueError:
        print("[!] Brave Search API returned an invalid JSON response.")
        return []

    web = payload.get("web") or {}
    results = web.get("results") or []

    cleaned = []
    for item in results:
        url = item.get("url")
        if not url:
            continue
        cleaned.append(
            {
                "title": item.get("title") or "Untitled result",
                "url": url,
                "description": item.get("description") or "",
            }
        )
    return cleaned


api_configured = bool(os.getenv("BRAVE_SEARCH_API_KEY", "").strip())

print("\n--------------------------")
print("Phone Number Web Footprint")
print("--------------------------\n")

fileoutput.write("--------------------------\n")
fileoutput.write("Phone Number Web Footprint\n")
fileoutput.write("--------------------------\n\n")

if not api_configured:
    msg = "[!] Web search disabled: BRAVE_SEARCH_API_KEY is not configured."
    print(msg)
    fileoutput.write(msg + "\n")
else:
    footprint_results = brave_search(
        f'"{maininput}" OR "{lookuptarget}"',
        count=10,
        country=CC,
    )

    if footprint_results:
        for item in footprint_results:
            print(f"[+] {item['title']}: {item['url']}")
            fileoutput.write(f"[+] {item['title']}\n{item['url']}\n")
            if item["description"]:
                fileoutput.write(f"    {item['description']}\n")
    else:
        print("[-] No public web results returned")
        fileoutput.write("[-] No public web results returned\n")

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

if not api_configured:
    print("[!] Provider searches skipped because BRAVE_SEARCH_API_KEY is not configured.")
    fileoutput.write(
        "[!] Provider searches skipped because BRAVE_SEARCH_API_KEY is not configured.\n"
    )
else:
    for site in varwebsites:
        query = f'site:{site} ("{maininput}" OR "{lookuptarget}")'
        results = brave_search(query, count=3, country=CC)

        for item in results:
            print(f"[+] {site}: {item['url']}")
            fileoutput.write(f"[+] {site}: {item['url']}\n")
            found_provider_result = True

        # Keep API usage modest and predictable.
        time.sleep(1)

    if not found_provider_result:
        print("[-] No provider-domain result returned")
        fileoutput.write("[-] No provider-domain result returned\n")

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
print(f"{maininput} Logs saved in {filepath} as '{report_name}'")
