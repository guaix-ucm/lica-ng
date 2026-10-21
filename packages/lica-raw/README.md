# lica-raw

## Introduction

`lica-raw` is a lightweight utility for reading metadata and raw Bayer pixel data from astronomical camera images. It defines minimal reader interfaces using `typing.Protocol` and provides adapters for FITS images and camera RAW files with EXIF metadata.

The package supports Bayer colour-filter-array layouts, per-channel black levels, optional rectangular regions of interest, and automatic selection of a reader from the image file extension. Application code depends only on the `ImageReader`, `ImageReaderFactory`, and `RawPixels` protocols, while the concrete image-format behaviour is supplied by adapters.

Objects returned by `read_pixels()` own the underlying image resource. They can be used as context managers, or closed explicitly with `close()` when batch processing makes a `with` block inconvenient.

## Installation

Install `lica-raw` directly from the `lica-ng` Git repository:

```bash
pip install lica-raw
```

or add it to your `pyproject.toml`:

```toml
[project]
dependencies = [
    "lica-raw",
]
```

For FITS image support, `lica-raw[fits]` installs the needed dependency on `astropy`:

```toml
[project]
dependencies = [
    "lica-raw[fits]",
]
```

For camera RAW file support,  `lica-raw[exif]` installs the needed dependencies `rawpy`, `exifread`, and `numpy`:

```toml
[project]
dependencies = [
    "lica-raw[exif]",
]
```

## Interfaces

`lica-raw` defines its image-access contracts using `typing.Protocol`. Adapters do not need to inherit from these protocols explicitly; they only need to provide the required methods and attributes.

### Image reader

```python
from typing import Protocol

from lica_raw import HeaderType, ImageMetadata
from lica_raw.ports import RawPixels


class ImageReader(Protocol):
    def header_type(self) -> HeaderType: ...

    def read_metadata(self, path: str) -> ImageMetadata: ...

    def read_pixels(self, path: str) -> RawPixels: ...
```

### Raw pixels

`RawPixels` objects support the context-manager protocol. Entering the context returns the pixel-data object; leaving it closes the underlying image resource, even if an exception occurs.

```python
from collections.abc import Generator
from types import TracebackType
from typing import Protocol, Self

from lica_raw import IntArray2D, Rect


class RawPixels(Protocol):
    def r(self, section: Rect | None) -> IntArray2D: ...
    def gr(self, section: Rect | None) -> IntArray2D: ...
    def gb(self, section: Rect | None) -> IntArray2D: ...
    def b(self, section: Rect | None) -> IntArray2D: ...

    def red_black_level(self) -> int: ...
    def gred_black_level(self) -> int: ...
    def gblue_black_level(self) -> int: ...
    def blue_black_level(self) -> int: ...

    def close(self) -> None: ...

    def __enter__(self) -> Self: ...

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None: ...
```

`close()` is idempotent and can be called explicitly. This is useful in batch-processing loops where wrapping every image in a `with` block would make the client code unnecessarily nested.

### Reader factory

```python
from typing import Protocol

from lica_raw.ports import ImageReader


class ImageReaderFactory(Protocol):
    def get_reader(self, path: str) -> ImageReader: ...
```

## Adapters

| Adapter | Module | Extra | Description |
|---|---|---|---|
| `FitsReader` | `lica_raw.adapters.fits` | `astropy` | Reads metadata and raw Bayer pixels from FITS images. |
| `ExifReader` | `lica_raw.adapters.exif` | `rawpy`, `exifread`, `numpy` | Reads metadata and raw Bayer pixels from camera RAW files using EXIF metadata and `rawpy`. |
| `ImageReaderFactoryImpl` | `lica_raw.adapters` | — | Selects `FitsReader` for FITS extensions and `ExifReader` otherwise. |

The factory recognises the following extensions as FITS:

- `.fit`
- `.fits`
- `.fts`

All other files are handled by `ExifReader`.

```python
from lica_raw.adapters import ImageReaderFactoryImpl

factory = ImageReaderFactoryImpl()
reader = factory.get_reader("image_001.fits")
```

## Image metadata

`read_metadata()` returns an `ImageMetadata` dataclass:

```python
from datetime import datetime

from lica_raw import BayerPattern, HeaderType, ImageType


@dataclass
class ImageMetadata:
    width: int
    height: int
    make: str | None
    model: str | None
    exptime: float | None
    iso: int | None
    gain: float | None
    black_level: int | None
    bayer: BayerPattern
    imagetyp: ImageType | None
    timestamp: datetime | None
    focal_len: float | None
    f_number: float | None
    header_type: HeaderType
    extension: str
```

The supported Bayer patterns are defined in the `BayerPattern` enum as follows:

- `RGGB`
- `BGGR`
- `GRBG`
- `GBRG`

The supported image types are defined in the `ImageType` enum as follows:

- `BIAS`
- `DARK`
- `FLAT`
- `LIGHT`

For non-FITS images, `image_type_by_path()` infers the image type from the file name or immediate parent-directory name. Names containing `FLAT`, `DARK` or `OSCURO`, or `BIAS` are classified accordingly; all other images are treated as `LIGHT`.

## FITS support

`FitsReader` requires the following mandatory FITS keywords:

- `NAXIS1`
- `NAXIS2`
- `BAYERPAT`

It also reads optional metadata from these keywords:

| Metadata | FITS keyword |
|---|---|
| Instrument or camera model | `INSTRUME` |
| Exposure time | `EXPTIME` |
| Gain | `LOG-GAIN` |
| Black level | `PEDESTAL` |
| Image type | `IMAGETYP` |
| Observation date | `DATE-OBS` |
| Focal length | `FOCALLEN` |
| Aperture diameter | `APTDIA` |

If `FOCALLEN` and `APTDIA` are both present, the focal ratio is calculated as `FOCALLEN / APTDIA`.

The observation timestamp is interpreted in UTC. `FitsRawPixels` uses `PEDESTAL` as the black level for all four Bayer channels.

## Camera RAW support

`ExifReader` reads EXIF metadata with `exifread` and raw image data with `rawpy`. It extracts manufacturer, model, focal length, focal ratio, ISO, exposure time, observation date, image dimensions, black levels, and the Bayer pattern.

The adapter currently requires a `RGBG` colour-filter-array description from `rawpy`. Other CFA layouts raise `UnsupportedCFAError`.

The observation date is read from `Image DateTime` or `EXIF DateTimeOriginal`, interpreted in UTC, and accepts the following formats:

- `%Y:%m:%d %H:%M:%S`
- `%Y-%m-%dT%H:%M:%S`
- `%Y-%m-%dT%H:%M:%S%z`

## Regions of interest

The `red()`, `greenr()`, `greenb()`, and `blue()` methods return a two-dimensional NumPy array containing the pixels of one Bayer colour channel.

If `section` is `None`, the full image is used. Otherwise, `section` must be a `Rect` expressed in output-channel coordinates; it is validated against the available image area and converted internally to the corresponding full-resolution Bayer coordinates.

```python
from lica_raw import Rect

section = Rect(0, 0, 100, 100)

red = pixels.red(section)
green_red = pixels.greenr(section)
green_blue = pixels.greenb(section)
blue = pixels.blue(section)
```

A section outside the valid area raises `OutOfBoundsError`.

## Resource management

`read_pixels()` returns an object that owns an open image resource. Prefer a context manager when the lifetime of the pixels is limited to a local block:

```python
with reader.read_pixels(path) as pixels:
    red = pixels.red(None)
```

For batch processing, explicit closing is equally valid:

```python
for path in image_paths:
    pixels = reader.read_pixels(path)
    try:
        red = pixels.red(None)
        ...
    finally:
        pixels.close()
```

After `close()`, the pixel object must not be used to access image data.

## Errors

All package-specific errors derive from `RawBaseError`.

| Error | Description |
|---|---|
| `UnsupportedCFAError` | The camera RAW file uses an unsupported colour-filter-array layout. |
| `ReadMetadataError` | EXIF metadata could not be read. |
| `UnknownDateTimeFormatError` | The observation-date string uses an unsupported format. |
| `OutOfBoundsError` | The requested rectangular section lies outside the image. |
| `MissingImageError` | The image path does not exist. |
| `MissingMandatoryFitsError` | One or more mandatory FITS keywords are missing. |
| `AlreadyClosedError` | Attempt to close an already closed FITS/EXIF image. |

## Usage example

```python
from lica_raw import ImageReaderFactory, Rect
from lica_raw.adapters import ImageReaderFactoryImpl

path = "light_001.fits"

factory: ImageReaderFactory = ImageReaderFactoryImpl()
reader = factory.get_reader(path)

metadata = reader.read_metadata(path)
print(metadata.model, metadata.raw_width, metadata.raw_height)
print(metadata.bayer, metadata.exptime, metadata.timestamp)

with reader.read_pixels(path) as pixels:
    # Gets the whole channel when section is None.
    red = pixels.red(None)
    green_red = pixels.greenr(Rect(0, 0, 256, 256))
    green_blue = pixels.greenb(Rect(0, 0, 256, 256))
    blue = pixels.blue(Rect(0, 0, 256, 256))

    print(
        pixels.red_black_level(),
        pixels.greenr_black_level(),
        pixels.greenb_black_level(),
        pixels.blue_black_level(),
    )
```

## Usage example, with lica-cli package

```python
import sys
from argparse import ArgumentParser, Namespace

from lica_cli import parse_args, run_cli
from lica_raw import ImageReaderFactory
from lica_raw.adapters import ImageReaderFactoryImpl

from myprog import __version__

DESCRIPTION = "My program short description"


def add_args(parser: ArgumentParser) -> None:
    parser.add_argument("image", help="FITS or camera RAW image path")


def cli_main(args: Namespace) -> None:
    factory: ImageReaderFactory = ImageReaderFactoryImpl()
    reader = factory.get_reader(args.image)

    metadata = reader.read_metadata(args.image)
    print(metadata)

    with reader.read_pixels(args.image) as pixels:
        # Gets the whole channel when section is None.
        print("Red channel shape:", pixels.red(None).shape)


def main():
    args = parse_args(add_args, __name__, __version__, DESCRIPTION)
    return_code = run_cli(cli_main, args, __name__, __version__)
    sys.exit(return_code)


if __name__ == "__main__":
    main()
```
