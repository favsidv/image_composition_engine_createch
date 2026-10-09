# Image Composition Engine

This project is a Python \"application\" that composes image layers from a JSON or YAML configuration. Each layer can define filters, a blending mode and an opacity.

## Installation

Requirements: Python 3.13 or newer and uv.

Run the following commands from the project root:

```bash
uv sync
```

## Run the application

```bash
uv run image-composition-engine-createch
```

The application reads `conf.json` and saves the result to `output/result.png`. An existing output file is replaced.

To change these paths, edit `CONFIG_PATH` and `OUTPUT_PATH` in `src/image_composition_engine_createch/cli.py`.

## Configuration

Layers are processed in their listed order: the first layer is at the bottom.

Each layer accepts:

| Field | Purpose | Default |
| --- | --- | --- |
| image | Path to the source image | Required |
| filters | Ordered list of filters | Empty list |
| blend | Registered blending mode | normal |
| opacity | Layer opacity between 0 and 1 | 1.0 |

Each filter entry contains a name and, when needed, a params dictionary.

Image paths are relative to the configuration file's directory.
The output path is relative to the current working directory.

All layers must have matching dimensions. Images are not automatically resized.

## Available filters

Filters have been made by Brune, and revisited for more comprehension by Chat-GPT.

| Name | Parameters |
| --- | --- |
| brightness | level: finite number; 0 preserves brightness |
| contrast | level: nonnegative number; 1 preserves contrast |
| invert | No parameters |
| boxblur | window: nonnegative integer radius |
| gaussianblur | window: nonnegative integer radius; sigma: positive finite number |

Blur filters also accept radius instead of window. Do not provide both names.

A radius of 2 gives a maximum neighborhood width of 5 pixels. Blur weights are renormalized at image boundaries.

## Blending and transparency

Blendings have been made by Brune, and revisited for more comprehension by Chat-GPT.

The registry contains 29 blending modes. See [blending conventions](docs/blending.md) for their names and behavior.

Images are loaded as normalized float32 RGBA arrays. Filters process RGB while the pipeline preserves alpha.

Layer opacity multiplies the image's alpha. Dissolve, Behind and Clear have specific transparency behavior described in the blending documentation.

The engine saves 8-bit PNG files. EXIF orientation is not applied.

## Verification

Run the regression tests:

```bash
uv run python -m unittest discover -s tests -v
```

Also inspect the generated image and check the effect of changing layer order, filter order, blending modes and opacity.

Invalid configurations, unknown operations, unreadable images and incompatible dimensions produce error messages.

## Project organization

- config.py reads and validates configurations.
- image_io.py loads and saves images.
- filters.py and blends/ implement image operations.
- registry.py connects configuration names to operation classes.
- pipeline.py applies filters in order.
- compositing.py handles blending and transparency.
- engine.py prepares and combines layers.
- application.py connects configuration loading, processing and saving.
- cli.py provides the application entry point.

## Current scope

The project includes the five filters listed above. Other planned filters, including grayscale, are not implemented yet.

A real filter exchange with another group still needs to be demonstrated. See [filter exchange](docs/filter_exchange.md) for the remaining steps. The engine does not claim pixel-exact reproduction of Photoshop.
