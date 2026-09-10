# PhoNumSpy

PhoNumSpy is a small OSINT utility for inspecting public metadata and web references associated with a phone number.

## Features

- Phone-number metadata (country/region, time zones, carrier when available)
- Public web-footprint search
- Targeted searches against the domains listed in `websites.txt`
- TXT report output
- Graceful handling of Google HTTP 429 rate limits
- Python 3 compatible

> Location data shown by the tool is numbering-plan/time-zone metadata. It is not live GPS tracking.

## Installation

```bash
git clone https://github.com/sebastisnzoth/PhoNumSpy.git
cd PhoNumSpy
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

## Google rate limits

PhoNumSpy uses `googlesearch-python` for public web searches. Google may return HTTP 429 when automated searches are rate-limited. Version 1.1 handles this condition without terminating the program and adds delays between targeted searches. A skipped search does not prove that no public result exists.

## Responsible use

Use PhoNumSpy only for lawful OSINT, research, or numbers you are authorized to investigate. Do not use the tool to harass, stalk, or invade another person's privacy.
