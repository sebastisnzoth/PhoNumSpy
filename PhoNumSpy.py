import os
import shutil
import subprocess
import time

import phonenumbers
import pyfiglet
from phonenumbers import carrier, geocoder, timezone
from phonenumbers.phonenumberutil import region_code_for_number

VERSION = "Version 2.0"


def run_phoneinfoga(number):
    """Run an installed PhoneInfoga binary as an optional OSINT companion."""
    binary = shutil.which("phoneinfoga")
    if not binary:
        return None, "PhoneInfoga is not installed or is not in PATH."

    try:
        completed = subprocess.run(
            [binary, "scan", "-n", number],
            capture_output=True,
            text=True,
            timeout=90,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return None, "PhoneInfoga scan timed out."
    except OSError as exc:
        return None, f"Could not start PhoneInfoga: {exc}"

    output = (completed.stdout or "").strip()
    error = (completed.stderr or "").strip()
    if completed.returncode != 0:
        return None, error or f"PhoneInfoga exited with code {completed.returncode}."
    return output or "No additional results returned.", None


print("\n")
ascii_art = pyfiglet.figlet_format("PhoNumSpy")
print(ascii_art)
print(VERSION)
print("\n")
time.sleep(0.5)

maininput = input(
    "Input the phone number using international format: +(prefix)(phonenumber) "
    "ES: +447455869664\n-->"
).strip()

safe_name = "".join(ch for ch in maininput if ch.isdigit() or ch in "+-") or "phone"
report_name = f"{safe_name}_results.txt"

try:
    target = phonenumbers.parse(maininput, None)
except phonenumbers.NumberParseException as exc:
    print(f"[-] Invalid phone number: {exc}")
    raise SystemExit(1)

possible = phonenumbers.is_possible_number(target)
valid = phonenumbers.is_valid_number(target)
if not possible:
    print("[-] The supplied phone number is not possible according to numbering-plan metadata.")
    raise SystemExit(1)

TZ = timezone.time_zones_for_number(target)
CC = region_code_for_number(target) or "Unknown"
CR = carrier.name_for_number(target, "en") or "Unknown / unavailable"
AREA = geocoder.description_for_number(target, "en") or "Unknown / unavailable"
E164 = phonenumbers.format_number(target, phonenumbers.PhoneNumberFormat.E164)
INTERNATIONAL = phonenumbers.format_number(target, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
NATIONAL = phonenumbers.format_number(target, phonenumbers.PhoneNumberFormat.NATIONAL)

type_map = {
    phonenumbers.PhoneNumberType.FIXED_LINE: "Fixed line",
    phonenumbers.PhoneNumberType.MOBILE: "Mobile",
    phonenumbers.PhoneNumberType.FIXED_LINE_OR_MOBILE: "Fixed line or mobile",
    phonenumbers.PhoneNumberType.TOLL_FREE: "Toll free",
    phonenumbers.PhoneNumberType.PREMIUM_RATE: "Premium rate",
    phonenumbers.PhoneNumberType.VOIP: "VoIP",
    phonenumbers.PhoneNumberType.UNKNOWN: "Unknown",
}
number_type = type_map.get(phonenumbers.number_type(target), "Other")

info_lines = [
    f"Possible number: {possible}",
    f"Valid number: {valid}",
    f"Number type: {number_type}",
    f"Country/Region code: {CC}",
    f"Numbering-plan area: {AREA}",
    f"Time-zone metadata: {TZ}",
    f"Carrier metadata: {CR}",
    f"E.164 format: {E164}",
    f"International format: {INTERNATIONAL}",
    f"National format: {NATIONAL}",
]

print("\n-------------------------")
print("Phone Number Information")
print("-------------------------\n")
for line in info_lines:
    print(line)

print(
    "\n[!] Privacy notice: area, time-zone and carrier values are numbering-plan "
    "metadata, not live GPS/location data."
)

print("\n--------------------------")
print("Optional PhoneInfoga OSINT")
print("--------------------------\n")
phoneinfoga_output, phoneinfoga_error = run_phoneinfoga(E164)
if phoneinfoga_error:
    print(f"[!] {phoneinfoga_error}")
    print("    Install PhoneInfoga separately if you want the optional public-OSINT scan.")
else:
    print(phoneinfoga_output)

with open(report_name, "w", encoding="utf-8") as fileoutput:
    fileoutput.write(ascii_art + "\n")
    fileoutput.write(VERSION + "\n\n")
    fileoutput.write("Phone Number Information\n")
    fileoutput.write("-------------------------\n")
    for line in info_lines:
        fileoutput.write(line + "\n")
    fileoutput.write(
        "\nPrivacy notice: area, time-zone and carrier values are numbering-plan "
        "metadata, not live GPS/location data.\n"
    )
    fileoutput.write("\nOptional PhoneInfoga OSINT\n")
    fileoutput.write("--------------------------\n")
    if phoneinfoga_error:
        fileoutput.write(f"{phoneinfoga_error}\n")
    else:
        fileoutput.write(phoneinfoga_output + "\n")

print("\n")
print(ascii_art)
print(VERSION)
print(f"\n{E164} report saved in {os.getcwd()} as '{report_name}'")
print("Use only for lawful public-source research and numbers you are authorized to investigate.")
