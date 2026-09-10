# PhoNumSpy

PhoNumSpy is a small OSINT utility for inspecting public metadata and public web references associated with a phone number.

## Features

- Phone-number metadata (country/region, time zones, carrier when available)
- Public web-footprint search through Brave Search API
- Targeted searches against domains listed in `websites.txt`
- TXT report output
- Python 3 compatible
- Continues to work even when no search API key is configured

> Location data shown by the tool is numbering-plan/time-zone metadata. It is not live GPS tracking.

## Installation

```bash
git clone https://github.com/sebastisnzoth/PhoNumSpy.git
cd PhoNumSpy
python3 -m pip install -r requirements.txt
```

## Configure web search

PhoNumSpy 1.2 no longer scrapes Google directly. It can use Brave Search API for public web searches.

Create a Brave Search API key and export it in your terminal:

```bash
export BRAVE_SEARCH_API_KEY="YOUR_API_KEY_HERE"
```

Do not commit your API key to GitHub.

To make the variable available in future Terminal sessions on zsh:

```bash
echo 'export BRAVE_SEARCH_API_KEY="YOUR_API_KEY_HERE"' >> ~/.zshrc
source ~/.zshrc
```

## Run

```bash
python3 PhoNumSpy.py
```

Enter a number in international E.164-style format, for example:

```text
+447455869664
```

If `BRAVE_SEARCH_API_KEY` is not configured, PhoNumSpy still prints the phone-number metadata and saves a report, but web searches are skipped.

## Version 1.2

- Replaced `googlesearch-python` scraping with Brave Search API
- Removed the old Google 429 failure path
- Added API-key detection and graceful fallback
- Added request timeout and API-error handling
- Clarified that location output is metadata, not a physical GPS location

## Responsible use

Use PhoNumSpy only for lawful OSINT, research, or numbers you are authorized to investigate. Do not use the tool to harass, stalk, or invade another person's privacy.
