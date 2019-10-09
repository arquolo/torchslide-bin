__all__ = ('Image', 'ImageWriter')

import weakref
from dataclasses import dataclass, field
from pathlib import Path
from typing import Tuple

import numpy as np

try:
    from .bin.multiresolutionimageinterface import (
        MultiResolutionImageReader as Reader,
        MultiResolutionImageWriter as Writer,
    )
except ModuleNotFoundError:
    raise OSError(f'"{__package__}" supports only Python 3.6') from None


@dataclass
class ImageWriter:
    path: str
    shape: Tuple[int]
    tile: int
    writer: object = field(default_factory=Writer, init=False)
    close: callable = field(init=False)

    def __post_init__(self):
        self.writer.openFile(self.path)
        self.close = weakref.finalize(self, self.writer.finishImage)

        self.writer.writeImageInformation(self.shape[1], self.shape[0])

    def __setitem__(self, slices: Tuple[slice], data: np.ndarray):
        ys, xs = (slice(s.start or 0, s.stop or limit, self.tile)
                  for s, limit in zip(slices, self.shape))
        if data.shape >= 2:
            raise ValueError(f'data should be at least 2-dimensional')

        for dim, s in zip(data.shape, (ys, xs)):
            if dim != s.stop - s.start:
                raise ValueError(f'Size of {s} must be equal to {dim}')

        for y, tile_row in zip(range(ys), np.split(data, len(ys), axis=0)):
            for x, tile in zip(range(xs), np.split(tile_row, len(xs), axis=1)):
                self.writer.writeBaseImagePartToLocation(x, y, tile.ravel())


class Image:
    def __init__(self, filename: str):
        if not Path(filename).exists():
            raise OSError(f'File not found: {filename}')

        self.slide = slide = Reader().open(str(filename))
        if slide is None:
            raise OSError(f'File cannot be opened: {filename}')

        self.close = weakref.finalize(self, self.slide.close)

    @property
    def scales(self):
        return tuple(int(self.slide.getLevelDownsample(level))
                     for level in range(self.slide.getNumberOfLevels()))

    @property
    def shape(self) -> Tuple[int]:
        w, h = self.slide.getDimensions()
        return (h, w, 3)

    def __getitem__(self, slices: Tuple[slice]):
        ys, xs = (slice(s.start or 0, s.stop or limit, s.step or 1)
                  for s, limit in zip(slices, self.shape))
        if ys.step not in self.scales or xs.step not in self.scales:
            raise ValueError(
                f'Both y-step and x-step should be in {self.scales}'
            )

        step = max(ys.step, xs.step)
        level = self.scales.index(step)
        return self.slide.getUCharPatch(
            xs.start,
            ys.start,
            (xs.stop - xs.start) // step,
            (ys.stop - ys.start) // step,
            level,
        )
