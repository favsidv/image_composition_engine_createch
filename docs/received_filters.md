# Filter exchange with Paul LAMOUR and Ryan Fihr HULTON

The teacher requires an exchange of at least one filter: copy the received
source file, add its import and registry declaration, and use it without changing
the filter's code or the engine's processing logic.

On October 9, 2026, we integrated four filters received from **Paul LAMOUR and
Ryan Fihr HULTON**. Their authorship is also recorded in the `external_filters`
package docstring. These filters are separate from Brune's built-in filters.

## Received files

The original `pixelate.py`, `glitch.py`, `hue.py` and `bubble_pop.py` files are
stored in `src/image_composition_engine_createch/external_filters/`. Their bytes,
including original comments and line endings, match the received files exactly.
The regression tests record and verify their original SHA-256 hashes.
A local `.gitattributes` prevents Git from converting their original line endings.

All four files import `Filter` from `.base`. The original `base.py` was not
provided, so we added a local `base.py` containing an import of our existing
Filter interface. This import bridge was written for this integration and is
not attributed to the filter authors. No received source file was edited.

The remaining integration consists of imports and factories in `registry.py`.
The Hue filter is imported as HueFilter to distinguish it from the Hue blend.
The pipeline, compositor, image I/O, application and main entry point are unchanged.
NumPy and SciPy were already project dependencies; colorsys is in Python's
standard library.

## Configurations using the teacher's photograph

| Filter | Parameters | Configuration |
| --- | --- | --- |
| pixelate | size=24 | [pixelate.json](../configurations/filter_exchange/pixelate.json) |
| glitch | intensity=0.6, slices=12 | [glitch.json](../configurations/filter_exchange/glitch.json) |
| hue | angle=60 degrees | [hue.json](../configurations/filter_exchange/hue.json) |
| bubble_pop | amount=12, average_size=150, opacity=0.5 | [bubble_pop.json](../configurations/filter_exchange/bubble_pop.json) |

Each configuration uses `images/layers/0_photo.jpg` at its original resolution
of 1908 by 1272 pixels. The main `conf.json` keeps the composition matching the
teacher's reference image.

To run one received filter from the repository root:

```bash
uv run python -c "from image_composition_engine_createch.application import compose_from_file; compose_from_file('configurations/filter_exchange/pixelate.json', 'output/filter_exchange/pixelate.png')"
```

Replace `pixelate` in both paths with `glitch`, `hue` or `bubble_pop` to run the
other configurations. Outputs are generated locally and ignored by Git.

## Verification

```bash
uv run python -m unittest discover -s tests -v
```

The exchange tests check unchanged source hashes, registration, RGB shape and
float32/float64 preservation, independent output arrays, finite normalized
values and alpha preservation by the existing pipeline. They also verify
partial pixelation blocks, a known hue rotation and a complete application run
on the teacher's photograph.

All four configurations have also been executed at the original resolution.
The generated files are `output/filter_exchange/pixelate.png`, `glitch.png`,
`hue.png` and `bubble_pop.png`. Glitch and BubblePop use fresh randomness on each
run, so their outputs vary. Only the regression tests substitute a fixed random
generator; the received implementations remain unchanged.

This demonstrates integration of the received files under the normalized RGB
contract. It does not claim that these files are standalone or compatible with
arbitrary image formats or every possible parameter value.
