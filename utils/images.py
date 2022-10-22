from typing import Callable, Any, Union

import pygame
from pygame.surface import SurfaceType

IMAGE_LOADER: Callable[[Any], Union[pygame.Surface, SurfaceType]] = lambda x: pygame.image.load(f"resource/images/{x}")
