import time
import base64


def generate_token(username: str, role: str = "user", verified: bool = False) -> str:
    """Create a session token.

    The token layout is: ``username:timestamp:role:verified`` encoded using
    base64. ``verified`` is ``1`` when the user has completed 2FA and ``0``
    otherwise.
    """

    raw = f"{username}:{int(time.time())}:{role}:{1 if verified else 0}"
    return base64.b64encode(raw.encode()).decode()


def decode_token(token: str):
    """Decode a session token produced by :func:`generate_token`."""

    try:
        decoded = base64.b64decode(token.encode()).decode()
        parts = decoded.split(":")
        username, timestamp, role = parts[:3]
        verified = len(parts) > 3 and parts[3] == "1"
        return {
            "username": username,
            "timestamp": int(timestamp),
            "role": role,
            "verified": verified,
        }
    except Exception:
        return None
