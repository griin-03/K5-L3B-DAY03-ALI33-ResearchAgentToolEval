from __future__ import annotations

from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
from tools._shared import err


def _normalize_url(url: str) -> str:
    if not isinstance(url, str) or not url.strip():
        raise ValueError('Every source must have a nonempty URL string.')
    parts = urlsplit(url.strip())
    if parts.scheme.lower() not in ('http', 'https') or not parts.hostname or parts.username or parts.password:
        raise ValueError('Use public HTTP(S) source URLs without embedded credentials.')
    port = parts.port
    host = parts.hostname.lower()
    if ':' in host:
        host = '[' + host + ']'
    if port and not (parts.scheme.lower() == 'http' and port == 80 or parts.scheme.lower() == 'https' and port == 443):
        host += ':' + str(port)
    query = [(key, value) for key, value in parse_qsl(parts.query, keep_blank_values=True)
             if not key.lower().startswith('utm_') and key.lower() not in ('fbclid', 'gclid')]
    return urlunsplit((parts.scheme.lower(), host, parts.path or '/', urlencode(query), parts.fragment))


def deduplicate_sources(items: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    """Keep the first source for each normalized URL, without fetching or rewriting it."""
    try:
        if not isinstance(items, list) or len(items) > 100:
            raise ValueError('items must be a list containing at most 100 source objects.')
        unique: list[dict[str, Any]] = []
        duplicates: list[dict[str, str]] = []
        seen: dict[str, str] = {}
        for item in items:
            if not isinstance(item, dict):
                raise ValueError('Every source must be an object.')
            key = _normalize_url(item.get('url'))
            if key in seen:
                duplicates.append({'url': item['url'], 'kept_url': seen[key]})
            else:
                seen[key] = item['url']
                unique.append(dict(item))
        return {'tool': 'deduplicate_sources', 'items': unique, 'input_count': len(items),
                'unique_count': len(unique), 'duplicate_count': len(duplicates), 'duplicates': duplicates}
    except Exception as exc:
        return err('deduplicate_sources', exc)
