import os
import time

import phonenumbers
import pyfiglet
from phonenumbers import carrier, geocoder, timezone
from phonenumbers.phonenumberutil import region_code_for_number

print("\n")
Ascii_Art = pyfiglet.figlet_format("PhoNumSpy")
print(Ascii_Art)
version = "Version 1.3"
print(version)
print("\n")
time.sleep(1)

maininput = input(
    "Input the phone number using international format: +(prefix)(phonenumber) "
    "ES: +447455869664\n-->"
).strip()

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
print("Phone Number Information")
print("-------------------------\n")

try:
    target = phonenumbers.parse(maininput, None)
except phonenumbers.NumberParseException as exc:
    print(f"[-] Invalid phone number: {exc}")
    fileoutput.write(f"[-] Invalid phone number: {exc}\n")
    fileoutput.close()
    raise SystemExit(1)

possible = phonenumbers.is_possible_number(target)
valid = phonenumbers.is_valid_number(target)

if not possible:
    msg = "[-] The supplied phone number is not possible according to numbering-plan metadata."
    print(msg)
    fileoutput.write(msg + "\n")
    fileoutput.close()
    raise SystemExit(1)

TZ = timezone.time_zones_for_number(target)
CC = region_code_for_number(target) or "Unknown"
CR = carrier.name_for_number(target, "en") or "Unknown / unavailable"
AREA = geocoder.description_for_number(target, "en") or "Unknown / unavailable"
E164 = phonenumbers.format_number(target, phonenumbers.PhoneNumberFormat.E164)
INTERNATIONAL = phonenumbers.format_number(target, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
NATIONAL = phonenumbers.format_number(target, phonenumbers.PhoneNumberFormat.NATIONAL)

info_lines = [
    f"Possible number: {possible}",
    f"Valid number: {valid}",
    f"Country/Region code: {CC}",
    f"Numbering-plan area: {AREA}",
    f"Time-zone metadata: {TZ}",
    f"Carrier metadata: {CR}",
    f"E.164 format: {E164}",
    f"International format: {INTERNATIONAL}",
    f"National format: {NATIONAL}",
]

for line in info_lines:
    print(line)

fileoutput.write("-------------------------\n")
fileoutput.write("Phone Number Information\n")
fileoutput.write("-------------------------\n\n")
for line in info_lines:
    fileoutput.write(line + "\n")

notice = (
    "\n[!] Privacy notice: location, time-zone, area and carrier values are "
    "numbering-plan metadata. They are not live GPS/location data."
)
print(notice)
fileoutput.write(notice + "\n")

print("\n--------------------------")
print("Public Web Search")
print("--------------------------\n")

web_notice = (
    "[!] Phone-number web profiling is not enabled in PhoNumSpy 1.3. "
    "This version focuses on local numbering-plan metadata and report generation."
)
print(web_notice)
fileoutput.write("\n--------------------------\n")
fileoutput.write("Public Web Search\n")
fileoutput.write("--------------------------\n\n")
fileoutput.write(web_notice + "\n")

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
