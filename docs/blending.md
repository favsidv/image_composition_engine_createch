# MADE BY AI
# MADE BY AI
# MADE BY AI

# Filters and blending conventions

Images use straight-alpha RGBA values in [0, 1]. Filters and RGB blend modes receive three-channel arrays. Operations preserve dimensions, accept float32 and float64, and return independent arrays. RGB blend classes use a common floating dtype when their two inputs differ.

The five existing filters are Brightness, Contrast, Invert, Blur and GaussianBlur. They implement Filter and validate their own constructor parameters, including when used outside the registry. Brightness adds a level; Contrast scales distances from 0.5. Both clip their results to [0, 1].

Box and Gaussian blur use a radius, with a maximum kernel width of 2 * radius + 1. The registry also accepts window as an alias for radius. SciPy performs the spatial calculation without mixing channels. Dividing by the filtered image of ones renormalizes weights at the borders, preserving the original implementation's cropped-neighborhood behavior. Alpha is kept unchanged by the pipeline, including when blurring RGB.

## Registered mode names

| Family | Configuration names |
| --- | --- |
| Normal | normal, dissolve, behind, clear |
| Darken | darken, multiply, color_burn, linear_burn, darker_color |
| Lighten | lighten, screen, color_dodge, linear_dodge, lighter_color |
| Contrast | overlay, soft_light, hard_light, vivid_light, linear_light, pin_light, hard_mix |
| Comparative | difference, exclusion, subtract, divide |
| HSL | hue, saturation, color, luminosity |

Classes use PascalCase, for example Multiply and SoftLight. Earlier draft identifiers such as multiply, Softlight, substract and linear_right have been replaced. Configuration names already supported by the engine are unchanged.

## RGB calculations

RGB modes implement BlendMode.apply(base, layer). The compositor handles the layer alpha, opacity and source-over composition separately.

Darker Color and Lighter Color compare sums within each individual pixel and select that whole pixel. Equal sums keep the base pixel.

Color Burn and Color Dodge use the W3C endpoint rules. Color Burn preserves a white base even over a black layer; Color Dodge preserves a black base even over a white layer. Safe divisions avoid creating infinities before clipping.

Divide saturates at one. A zero divisor, including 0/0, returns one by project convention: Adobe's descriptive page does not specify that numerical case.

Hue, Saturation, Color and Luminosity use W3C nonseparable blend formulas. Their luminosity is 0.3R + 0.59G + 0.11B, rather than HSL lightness (maximum + minimum) / 2. Gamut adjustment preserves the target luminosity. Soft Light uses the W3C piecewise curve.

## Modes that change alpha

Dissolve, Behind and Clear implement AlphaBlendMode.compose(base, layer, opacity) because their behavior cannot be expressed by RGB mixing alone. The compositor dispatches these operations before the RGB blending path.

- Dissolve samples one binary mask per pixel, shared by all RGB channels. Coverage probability is layer alpha multiplied by opacity. Results vary between runs. Direct construction with Dissolve(seed=...) is reproducible.
- Behind places the incoming layer beneath the base using destination-over. Opaque base pixels are preserved.
- Clear uses the incoming layer alpha multiplied by opacity as an eraser mask. Layer RGB values are ignored. Fully erased pixels have zero RGB and alpha.

Adobe describes Behind and Clear as painting-tool modes. Their use with an image layer as a coverage mask is an explicit convention of this engine.

## References and scope

- [Adobe blending mode descriptions](https://helpx.adobe.com/photoshop/desktop/repair-retouch/adjust-light-tone/blending-mode-descriptions.html)
- [W3C compositing and blending formulas](https://www.w3.org/TR/compositing-1/)
- [SciPy Gaussian filtering](https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.gaussian_filter.html)
- [SciPy uniform filtering](https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.uniform_filter.html)

These normalized RGB formulas do not reproduce Photoshop's complete color management, bit-depth processing, Fill behavior or brush engine. Pixel-exact Photoshop parity is not claimed. Filters not yet written, including grayscale, are outside this correction of the existing filter classes.

## Verification

Run from the repository root:

```bash
uv run python -m unittest discover -s tests -v
```

Tests cover known numerical results, singular divisions, grayscale colors, per-pixel selection, alpha operations, filter edge neighborhoods, dtype, input preservation and direct parameter validation.