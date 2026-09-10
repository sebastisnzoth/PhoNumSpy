#!/usr/bin/env python3

from pathlib import Path

import instaloader

from instagram_osint import get_public_profile, render_profile, save_profile_json


def main() -> None:
    username = input("Instagram username (public or authorized): @").strip()
    try:
        profile = get_public_profile(username)
    except (instaloader.exceptions.InstaloaderException, ValueError) as exc:
        print(f"[-] Instagram lookup failed: {exc}")
        raise SystemExit(1)

    print()
    print(render_profile(profile))

    safe_username = "".join(ch for ch in profile.username if ch.isalnum() or ch in "._-")
    output = Path(f"instagram_{safe_username}.json")
    save_profile_json(profile, str(output))
    print(f"\n[+] JSON report saved to: {output.resolve()}")
    print("[!] Public/authorized use only. No private content or messages are accessed.")


if __name__ == "__main__":
    main()
