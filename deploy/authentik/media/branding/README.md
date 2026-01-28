# Branding Assets

This directory contains branding assets for Authentik.

## Required Files

- `logo.svg` - Main logo displayed on login/signup pages (256x256 viewBox)
- `favicon.png` - Browser favicon (64x64 pixels)

## Generating favicon.png

To generate a favicon from the SVG logo:

```bash
# Using ImageMagick
convert -background none logo.svg -resize 64x64 favicon.png

# Or using Inkscape
inkscape logo.svg -w 64 -h 64 -o favicon.png

# Or using librsvg
rsvg-convert -w 64 -h 64 logo.svg > favicon.png
```

## Customization

Replace these files with your own branding assets. The Nordic theme CSS in
`07-branding.yaml` uses colors that complement the default assets:

- Primary: `#0f172a` (nordic-900)
- Accent: `#0284c7` (accent-600)
- Light accent: `#38bdf8` (accent-400)
