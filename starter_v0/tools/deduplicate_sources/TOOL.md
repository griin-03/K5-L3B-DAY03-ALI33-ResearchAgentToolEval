---
name: deduplicate_sources
track: core
kind: local_formatter
provider: Python standard library
requires_env: []
inputs: [items]
outputs: [items, input_count, unique_count, duplicate_count, duplicates]
side_effect: false
---
# deduplicate_sources

Remove repeated source URLs from a supplied list before formatting a digest.
Use when the user requests deduplication and supplies source objects. Ask for the
list if it is missing. Do not use for discovery, fact checking or semantic merging.

Input: at most 100 objects, each containing a nonempty public HTTP(S) URL. An empty
list is valid. Keep the first source and metadata unchanged. Normalize scheme/host,
default ports and known tracking parameters (`utm_*`, `fbclid`, `gclid`). Preserve
paths, fragments, non-tracking query values and their order: these can affect content.
This does not establish semantic equivalence or source quality.

No network, API key, file write or confirmation is required. Invalid input and
unexpected implementation failures return an error dict without partial results.

Reference: [Python urllib.parse](https://docs.python.org/3/library/urllib.parse.html).
