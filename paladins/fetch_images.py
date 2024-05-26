import json
import logging
import os
import random
import asyncio

logger = logging.getLogger(__name__.split('.')[-1])

def __replace_all__(text, replacements):
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def __format_name__(name):
    """Formats the name to be lowercase. Replace ' ' with '_' and ' with ."""
    return __replace_all__(str(name).lower(), {" ": "_", "'": "", ",": "", "!": ""}).strip()


def __format_map_name__(name):
    """Formats the map name and removes () and (payload)"""
    return __replace_all__(__format_name__(name), {"_(payload)": "", "(": "", ")": ""})


MAP_FLAIRS = {
  "dragon": {"maps": ["dragon_arena", "dawnforge", "warders_gate"], "sprites": ["endofmatchlobby_i1f1", "endofmatchlobby_i1ef"]},
  "ice": {"maps": ["ice_mines", "frozen_guard", "frostbite_cavern", "glacier_keep", "snowfall_junction"], "sprites": ["endofmatchlobby_i1d1", "endofmatchlobby_i1d3"]},
  "io": {"maps": ["bazaar", "shattered_desert"], "sprites": ["endofmatchlobby_i1df", "endofmatchlobby_i1e1"]},
  "nature": {"maps": ["frog_isle", "serpent_beach", "jaguar_falls", "temple_ruins", "primal_court"], "sprites": ["endofmatchlobby_i1e3", "endofmatchlobby_i1e5", "endofmatchlobby_i1e7"]},
  "magistrate": {"maps": ["trade_district", "stone_keep", "stone_keep_day", "stone_keep_night", "stone_keep_v2_day", "stone_keep_v2_night"], "sprites": ["endofmatchlobby_i1cb", "endofmatchlobby_i1cd", "endofmatchlobby_i1e9", "endofmatchlobby_i1d5"]},
  "abyss": {"maps": ["marauders_port", "abyss", "throne", "magistrates_archives"], "sprites": ["endofmatchlobby_i1f3", "endofmatchlobby_i1f5", "endofmatchlobby_i1f7", "endofmatchlobby_i1f9"]},
  "forest": {"maps": ["splitstone_quarry", "foremans_rise", "timber_mill", "fish_market", "greenwood_outpost", "enchanted_forest"], "sprites": ["endofmatchlobby_i1ed", "endofmatchlobby_i1eb", "endofmatchlobby_i1cf"]},
  "pip": {"maps": ["brightmarsh", "hidden_temple"], "sprites": ["endofmatchlobby_i1d7", "endofmatchlobby_i1d9", "endofmatchlobby_i1db"]},
  "jenos": {"maps": ["ascension_peak"], "sprites": ["endofmatchlobby_i1dd"]}
}


class MatchCustomisationImages:
    def __init__(self, base: str):
        self.background = f"{base}background.png"
        self.defeat = f"{base}defeat.png"
        self.dont_touch = f"{base}donttouch.png"
        self.info_text = f"{base}infotext.png"
        self.not_selected = f"{base}notselected.png"
        self.selected = f"{base}selected.png"
        self.snippet_1 = f"{base}snippet1.png"
        self.snippet_2 = f"{base}snippet2.png"
        self.victory = f"{base}victory.png"


class MatchImages:
    def __init__(self, base: str):
        self.base_image = f"{base}base_image.png"
        self.base_image_ranked = f"{base}base_image_ranked.png"
        self.base_image = f"{base}base_image_1.png"
        self.alt_image = f"{base}base_image_2.png"

        self.item_pane_0 = f"{base}item_pane_0.png"
        self.item_pane_1 = f"{base}item_pane_1.png"
        self.item_pane_2 = f"{base}item_pane_2.png"
        self.item_pane_3 = f"{base}item_pane_3.png"

        self.loadout_pane = f"{base}loadout_pane.png"
        self.player_sliver = f"{base}player_sliver.png"
        self.squire_sliver = f"{base}squire_sliver.png"

        self.stat_text_casual = f"{base}stat_text_casual.png"
        self.stat_text = f"{base}stat_text.png"


class ChampionIcon:
    def __init__(self, base: str, champion: str):
        if "omen" in champion and random.randint(0, 5) == 1:
            self.no_bg = f"{base}no_background/{champion}_goofy.png"
            self.bg = f"{base}background/{champion}_goofy.png"
            self.url = f"https://raw.githubusercontent.com/FuriaPaladins/Itto-Bot-Data/dev/paladins/champion_icons/no_background/{champion.replace(' ', '%20')}_goofy.png"
        else:
            self.no_bg = f"{base}no_background/{champion}.png"
            self.bg = f"{base}background/{champion}.png"
            self.url = f"https://raw.githubusercontent.com/FuriaPaladins/Itto-Bot-Data/dev/paladins/champion_icons/no_background/{champion.replace(' ', '%20')}.png"


class Talent:
    def __init__(self, if_exists, base, champion, talent):
        self._if_exists = if_exists
        self._base = base
        self._champion = champion
        self._talent = talent

    @property
    def full(self):
        return self._if_exists(f"{self._base}full/{self._champion}/{self._talent}.png")

    @property
    def flat(self):
        return self._if_exists(f"{self._base}flat/{self._champion}/{self._talent}.png")


class Passive:
    def __init__(self, if_exists, base, passive):
        self.full = if_exists(f"{base}full/{passive}.png")
        self.flat = if_exists(f"{base}flat/{passive}.png")


class PaladinsImages:
    """A class that fetches image from the assets folder."""

    empty_image = "src/assets/general/blank.png"
    base = "src/assets/paladins/"

    @classmethod
    def match_image_customisation(cls):
        return MatchCustomisationImages(
            f"{cls.base}.match_images/base_customisation_images/layer_"
        )

    @classmethod
    def match_image_base(cls):
        return MatchImages(f"{cls.base}.match_images/")

    @classmethod
    def card(cls, champion, card=None):
        """Returns all the cards for a champion. If a card is provided, it will return that card instead"""
        if card is None:
            return cls._if_exists(f"{cls.base}cards/{__format_name__(champion)}/")
        return cls._if_exists(
            f"{cls.base}cards/{__format_name__(champion)}/{__format_name__(card)}.png"
        )

    @classmethod
    def card_borders(
        cls, level: int = None, gold: bool = False, cooldown: bool = False
    ):
        """Returns a loadout border"""
        if cooldown:
            return cls._if_exists(f"{cls.base}cards/.borders/card_timer.png")
        if gold:
            return cls._if_exists(
                f"{cls.base}cards/.borders/legendary_lvl_{level if 5 > level > 0 else 5}.png"
            )
        return cls._if_exists(
            f"{cls.base}cards/.borders/card_lvl_{level if 5 > level > 0 else 5}.png"
        )

    @classmethod
    def background(cls, champion):
        """Returns the background for a champion"""
        return cls._if_exists(
            f"{cls.base}champion_backgrounds/{__format_name__(champion)}.png"
        )

    @classmethod
    def champion(cls, champion):
        """Returns the champion icon for a champion"""
        return ChampionIcon(f"{cls.base}champion_icons/", __format_name__(champion))

    @classmethod
    def champion_alt(cls, alt_name):
        """Returns the champion alt funny image"""
        return cls._if_exists(
            f"{cls.base}champion_icons/alt/{__format_name__(alt_name)}.png"
        )

    @classmethod
    def item(cls, item):
        """Returns the item icon for an item"""
        return cls._if_exists(f"{cls.base}items/{__format_name__(item)}.png")

    @classmethod
    def map(cls, map_name):
        """Returns the map icons"""
        path = f"{cls.base}maps/{__format_map_name__(map_name)}.png"
        if os.path.exists(path):
            return path
        return f"{cls.base}maps/test_maps.png"

    @classmethod
    def map_icon(cls, map_name):
        """Returns the alt map icon if it exists, else returns any """
        for map_types in MAP_FLAIRS:
            if __format_map_name__(map_name) in MAP_FLAIRS[map_types]["maps"]:
                return cls._if_exists(f"{cls.base}maps_sprites/{random.choice(MAP_FLAIRS[map_types]['sprites'])}.png")

        return cls._if_exists(f"{cls.base}maps_sprites/{random.choice(os.listdir(f'{cls.base}maps_sprites/'))}.png")

    @classmethod
    def talent(cls, champion, talent):
        """Returns the talent icon"""
        return Talent(
            cls._if_exists,
            f"{cls.base}talents/",
            __format_name__(champion),
            __format_name__(talent),
        )

    @classmethod
    def passive(cls, passive):
        """Returns the passive icon"""
        return Passive(
            cls._if_exists, f"{cls.base}passives/", __format_name__(passive)
        )

    @classmethod
    def platform(cls, platform):
        """Returns the platform icon"""
        return cls._if_exists(f"{cls.base}platforms/{__format_name__(platform)}.png")

    @classmethod
    def rank(cls, rank, centered=True):
        """Returns the rank icon for a rank"""
        return cls._if_exists(
            f"{cls.base}ranks/{'centered' if centered else 'default'}/{__format_name__(rank)}.png"
        )

    @classmethod
    def avatar(cls, avatar_id):
        """Returns the avatar icon for an avatar"""
        ## Search for avatars and get the extension
        avatar_id = str(avatar_id)
        for file in os.listdir(f"{cls.base}avatars/"):
            if avatar_id in file:
                return cls._if_exists(f"{cls.base}avatars/{file}")
        logger.warning(f"Found weird avatar ({avatar_id})")
        return None

    @classmethod
    def _if_exists(cls, path: str) -> str:
        if os.path.exists(path):
            return path
        return cls.empty_image
