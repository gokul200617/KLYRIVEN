"""
app/core/security.py
--------------------
Lightweight input-sanitization utilities.

These helpers are NOT a substitute for proper SQL parameterisation
(handled by SQLAlchemy) or HTML escaping (handled by the frontend).
They provide a first-pass defence against control characters and
excessively long strings reaching the database.
"""

from __future__ import annotations

import re
import unicodedata

# Characters we strip: all C0/C1 control characters except ordinary
# whitespace (space, tab, newline, carriage-return).
_CONTROL_CHAR_RE = re.compile(
    r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]"
)

# Maximum length we allow for any single sanitised string (safety ceiling).
_MAX_DEFAULT_LENGTH = 5_000


def sanitize_string(
    value: str,
    *,
    max_length: int = _MAX_DEFAULT_LENGTH,
    normalize: bool = True,
) -> str:
    """Return a sanitised copy of *value*.

    Steps applied in order:
    1. Strip leading / trailing whitespace.
    2. Remove C0/C1 control characters (keeps tab, LF, CR).
    3. Optionally normalise to NFC Unicode form.
    4. Truncate to *max_length* characters.

    Args:
        value:      Input string to sanitise.
        max_length: Hard ceiling on the returned string length.
                    Defaults to 5,000 characters.
        normalize:  When True (default) apply NFC normalisation so that
                    visually identical characters share the same code points.

    Returns:
        The sanitised string.
    """
    if not isinstance(value, str):
        raise TypeError(f"sanitize_string expected str, got {type(value).__name__!r}")

    cleaned = value.strip()
    cleaned = _CONTROL_CHAR_RE.sub("", cleaned)

    if normalize:
        cleaned = unicodedata.normalize("NFC", cleaned)

    if len(cleaned) > max_length:
        cleaned = cleaned[:max_length]

    return cleaned


def sanitize_optional(
    value: str | None,
    **kwargs,
) -> str | None:
    """Like :func:`sanitize_string` but passes *None* through unchanged."""
    if value is None:
        return None
    return sanitize_string(value, **kwargs)
