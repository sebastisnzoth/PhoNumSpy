# PhoNumSpy

PhoNumSpy is a small phone-number metadata utility for inspecting numbering-plan information and generating a local TXT report.

## Features

- Validates whether a number is possible and valid
- Country/region code
- Numbering-plan area description when available
- Time-zone metadata
- Carrier metadata when available
- E.164, international and national formatting
- TXT report output
- Python 3 compatible

> Location, area, time-zone and carrier values are numbering-plan metadata. They are not live GPS/location data.

## Installation

```bash
git clone https://github.com/sebastisnzoth/PhoNumSpy.git
cd PhoNumSpy
python3 -m pip install -r requirements.txt
```

## Update an existing clone

```bash
cd /Volumes/Armazenamento/developer/PhoNumSpy
git pull
python3 -m pip install -r requirements.txt
```

## Run

```bash
python3 PhoNumSpy.py
```

Enter a number in international E.164-style format, for example:

```text
+447455869664
```

## Version 1.3

- Removed the Brave Search API dependency
- Removed direct phone-number web profiling
- Added possible/valid number checks
- Added local numbering-plan area metadata
- Added E.164, international and national formatting
- Simplified dependencies to `phonenumbers` and `pyfiglet`
- Clarified that metadata does not represent a phone's physical location

## Responsible use

Use PhoNumSpy only for lawful purposes and numbers you are authorized to inspect. Do not use the tool to harass, stalk, or invade another person's privacy.
