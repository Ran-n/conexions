#! /usr/bin/env python3
# ------------------------------------------------------------------------------
# + Authors:	Ran#
# + Created:	2026/03/16 14:48:22.031905
# + Revised:	2026/03/16 14:48:22.031905
# ------------------------------------------------------------------------------

from enum import StrEnum

# ------------------------------------------------------------------------------


class Anonymity(StrEnum):
    """Proxy anonymity level.

    ELITE       — Level 1. The website cannot detect a proxy is in use.
    ANONYMOUS   — Level 2. The website knows a proxy is in use but not the real IP.
    TRANSPARENT — Level 3. The website knows a proxy is in use and sees the real IP.
    """

    ELITE = "elite proxy"
    ANONYMOUS = "anonymous"
    TRANSPARENT = "transparent"


# ------------------------------------------------------------------------------
