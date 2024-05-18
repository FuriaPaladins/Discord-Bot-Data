import os
from dataclasses import dataclass


def format_name(name):
    text = name.lower()
    for old, new in {" ": "_", "'": "", ",": "", "!": ""}:
        text = text.replace(old, new)
    return text.strip()


@dataclass
class LegendIcons:
    image: str
    coloured_image: str


class PickrateAssets:
    NEGATIVE = "src/assets/apex/pickrate_assets/negative.png"
    POSITIVE = "src/assets/apex/pickrate_assets/positive.png"
    PICKRATE_BASE = "src/assets/apex/pickrate_assets/pickrate_base.png"
    PICKRATE_SNIPPET = "src/assets/apex/pickrate_assets/pickrate_snippet.png"


class ApexImages:
    """A class that fetches images from the assets folder."""

    empty_image = "src/assets/general/blank.png"
    base = "src/assets/apex/"

    @classmethod
    def legend(cls, legend):
        """Returns the legend icon for a legend"""
        return LegendIcons(cls._if_exists(f"{cls.base}legend_icons/{format_name(legend)}.png"), cls._if_exists(f"{cls.base}legend_icons/{format_name(legend)}_recoloured.png"))

    @classmethod
    def _if_exists(cls, path: str) -> str:
        if os.path.exists(path):
            return path
        return cls.empty_image
