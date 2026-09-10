"""Public/authorized Instagram profile lookup for PhoNumSpy.

This module intentionally limits itself to profile metadata that Instagram makes
available through Instaloader. It does not bypass private profiles, obtain DMs,
session cookies, passwords, or hidden content.
"""

import json
from dataclasses import asdict, dataclass
from typing import Optional

import instaloader


@dataclass
class InstagramProfile:
    username: str
    user_id: Optional[int]
    full_name: str
    biography: str
    followers: Optional[int]
    followees: Optional[int]
    posts: Optional[int]
    is_private: bool
    is_verified: bool
    is_business_account: bool
    business_category_name: Optional[str]
    external_url: Optional[str]
    profile_pic_url: Optional[str]


def get_public_profile(username: str) -> InstagramProfile:
    """Return public profile metadata for an Instagram username.

    No login is performed. Private-profile content is not enumerated.
    """
    username = username.strip().lstrip("@")
    if not username:
        raise ValueError("Instagram username is required.")

    loader = instaloader.Instaloader(
        download_pictures=False,
        download_videos=False,
        download_video_thumbnails=False,
        download_geotags=False,
        download_comments=False,
        save_metadata=False,
        compress_json=False,
        quiet=True,
    )

    profile = instaloader.Profile.from_username(loader.context, username)

    return InstagramProfile(
        username=profile.username,
        user_id=getattr(profile, "userid", None),
        full_name=getattr(profile, "full_name", "") or "",
        biography=getattr(profile, "biography", "") or "",
        followers=getattr(profile, "followers", None),
        followees=getattr(profile, "followees", None),
        posts=getattr(profile, "mediacount", None),
        is_private=bool(getattr(profile, "is_private", False)),
        is_verified=bool(getattr(profile, "is_verified", False)),
        is_business_account=bool(getattr(profile, "is_business_account", False)),
        business_category_name=getattr(profile, "business_category_name", None),
        external_url=getattr(profile, "external_url", None),
        profile_pic_url=str(getattr(profile, "profile_pic_url", "") or "") or None,
    )


def render_profile(profile: InstagramProfile) -> str:
    data = asdict(profile)
    lines = ["Instagram Public Profile", "------------------------"]
    for key, value in data.items():
        lines.append(f"{key}: {value}")
    if profile.is_private:
        lines.append(
            "note: account is private; no private posts, followers/followees, "
            "messages, or hidden content are accessed by this module."
        )
    return "\n".join(lines)


def save_profile_json(profile: InstagramProfile, path: str) -> None:
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(asdict(profile), handle, ensure_ascii=False, indent=2)
