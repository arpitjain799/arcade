from pathlib import Path
from typing import Union, Optional

import arcade
from arcade.hitbox import HitBoxAlgorithm
from arcade.texture import Texture
from arcade.cache import (
    TextureCache,
    ImageDataCache,
    HitBoxCache,
)
from . import SpriteSheet


class TextureManager:
    """
    This class is used to manage textures. It is used to keep track of
    textures that have been loaded, and to make sure we don't load the
    same texture twice.

    Textures loaded through this manager is cached internally.
    """
    def __init__(self):
        self._sprite_sheets = {}
        self._textures = {}
        self._hit_box_cache = HitBoxCache()
        self._image_data_cache = ImageDataCache()
        self._texture_cache = TextureCache()

    def texture(
        self,
        path: Union[str, Path],
        hit_box_algorithm: Optional[HitBoxAlgorithm] = None,
        cache: bool = True,
    ) -> Texture:
        """
        Loads a texture or returns a cached version.

        :param path: Path to the file to load.
        :param hit_box_algorithm: Algorithm to use to create a hit box for the texture.
        """
        # TODO: DON'T CALL arcade.load_texture?
        texture = arcade.load_texture(path, hit_box_algorithm=hit_box_algorithm)
        # Do caching here
        return texture

    def spritesheet(self, path: Union[str, Path], cache: bool = True) -> SpriteSheet:
        """
        Loads a spritesheet or returns a cached version.

        :param path: Path to the file to load.
        :param cache: If ``True``, the spritesheet will be cached. If ``False``, the
            spite sheet will not be cached or returned from the cache.
        """
        path = arcade.resources.resolve_resource_path(path)
        if path in self._sprite_sheets and cache:
            return self._sprite_sheets[path]

        sprite_sheet = SpriteSheet(path)
        if cache:
            self._sprite_sheets[path] = sprite_sheet
        return sprite_sheet

    def flush(self, textures: bool = True, sprite_sheets: bool = True):
        """
        Remove contents from the texture manager.
        """
        if textures:
            self._textures.clear()
        if sprite_sheets:
            self._sprite_sheets.clear()
