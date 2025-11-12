# Design Configuration Guide

## Overview

The `design_config.json` file defines visual themes for card generation. Each design can specify partial configurations—missing fields automatically inherit from the "simple" default design.

---

## Configuration Structure

```json
{
    "design_name": {
        "front": { ... },
        "back": { ... }
    }
}
```

---

## Front Card Configuration

### `colors` (object)

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `background` | list[string] | `["#FFFFFF"]` | Background colors (hex). Random selection. |
| `text` | list[string] | `["#000000"]` | Text colors for title, artist, and year. Same color applied uniformly. |

**Example:**
```json
"colors": {
    "background": ["#FFFFFF", "#F5F5F5"],
    "text": ["#000000", "#333333"]
}
```

---

### `typography` (object)

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `font_family` | string | `"fonts/..."` | Path to TrueType font file (relative to assets dir) |
| `title_size_ratio` | float | `0.08` | Initial title font size as ratio of card size |
| `title_min_size_ratio` | float | `0.04` | Minimum title font size (auto-scaling) |
| `year_size_ratio` | float | `0.3` | Initial year font size as ratio of card size |
| `year_min_size_ratio` | float | `0.15` | Minimum year font size (auto-scaling) |
| `artist_size_ratio` | float | `0.08` | Initial artist font size as ratio of card size |
| `artist_min_size_ratio` | float | `0.04` | Minimum artist font size (auto-scaling) |

**Notes:**
- Font sizes automatically scale down if text doesn't fit
- `*_min_size_ratio` prevents text from becoming unreadable
- All ratios are relative to `card_size` (default 800px)

**Example:**
```json
"typography": {
    "font_family": "fonts/Roboto/Roboto-Bold.ttf",
    "title_size_ratio": 0.1,
    "artist_size_ratio": 0.07
}
```

---

### `layout` (object)

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `title_y_ratio` | float | `0.15` | Vertical position of title center (0.0 = top, 1.0 = bottom) |
| `title_max_height_ratio` | float | `0.25` | Maximum height for title text block |
| `year_y_ratio` | float | `0.5` | Vertical position of year center |
| `artist_y_ratio` | float | `0.85` | Vertical position of artist center |
| `artist_max_height_ratio` | float | `0.25` | Maximum height for artist text block |
| `text_max_width_ratio` | float | `0.9` | Maximum text width (0.9 = 90% of card width) |
| `line_height_multiplier` | float | `1.2` | Line spacing (1.0 = tight, 1.5 = loose) |

**Notes:**
- Y ratios position the **center** of text blocks
- `*_max_height_ratio` used for auto-scaling (text must fit within height)
- Positions are relative to card edges

**Example:**
```json
"layout": {
    "title_y_ratio": 0.2,
    "artist_y_ratio": 0.8,
    "line_height_multiplier": 1.3
}
```

---

### `images` (object)

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `backgrounds` | list[string] | `[]` | Paths to background images or directories. Random selection. |

**Notes:**
- If path is a **directory**, random image is selected from it
- If path is a **file**, that specific image is used
- Empty list = solid color background only
- Images are resized to card size and composited over background color

**Example:**
```json
"images": {
    "backgrounds": [
        "designs/theme1/bg1.png",
        "designs/theme1/bg2.png",
        "designs/theme1/backgrounds"  // directory: random file selected
    ]
}
```

---

## Back Card Configuration

### `colors` (object)

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `background` | list[string] | `["#000000"]` | Background colors (hex). Random selection. |
| `qr_border` | list[string] | `["#FFFFFF"]` | QR code border colors. Random selection. |

---

### `layout` (object)

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `qr_size_ratio` | float | `0.5` | QR code size as ratio of card size (0.5 = 50%) |
| `qr_border_ratio` | float | `0.01` | QR border thickness as ratio of card size |

**Example:**
```json
"layout": {
    "qr_size_ratio": 0.6,
    "qr_border_ratio": 0.02
}
```

---

### `images` (object)

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `qr_backgrounds` | list[string] | `[]` | Background images behind QR code. Random selection. |
| `qr_center_logos` | list[string] | `[]` | Logo/icon overlaid on QR center. Random selection. |

**Notes:**
- `qr_backgrounds`: Full card backgrounds (behind QR)
- `qr_center_logos`: Small icon in QR center (25% of QR size)
- Empty lists = no images used

**Example:**
```json
"images": {
    "qr_backgrounds": ["designs/gradient.png"],
    "qr_center_logos": ["designs/spotify_icon.png"]
}
```

---

## Design Inheritance

Designs inherit missing fields from the `"simple"` design. This allows minimal configs:

**Minimal custom design:**
```json
"my_design": {
    "front": {
        "colors": {
            "text": ["#FF0000"]
        }
    }
}
```

This inherits all other fields (fonts, layouts, sizes) from `"simple"` but uses red text.

---

## Creating Custom Designs

### 1. Start with partial config
```json
"my_theme": {
    "front": {
        "colors": {
            "background": ["#1a1a1a"],
            "text": ["#00ff00"]
        },
        "typography": {
            "font_family": "fonts/MyFont/MyFont-Bold.ttf"
        }
    },
    "back": {
        "colors": {
            "background": ["#1a1a1a"]
        }
    }
}
```

### 2. Test the design
```bash
spoticards create --design my_theme --playlist <URL>
```

### 3. Validate (future feature)
```bash
spoticards validate-config --design my_theme
```

---

## Best Practices

### Color Selection
- Use lists even for single colors: `["#FFFFFF"]` not `"#FFFFFF"`
- Use hex format: `#RRGGBB`
- Ensure sufficient contrast (text vs background)

### Font Paths
- Use relative paths from `assets/` directory
- Ensure fonts support your character sets
- Test with long artist names and special characters

### Layout Ratios
- Keep `text_max_width_ratio` < 1.0 for margins
- Ensure vertical positions don't overlap:
  - Title: ~0.15
  - Year: ~0.5
  - Artist: ~0.85

### Image Paths
- Use directories for variety: `"designs/my_theme/backgrounds"`
- Use specific files for consistent look: `"designs/logo.png"`
- Optimize image sizes (recommended: 800x800px)

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Text doesn't fit | Reduce `*_size_ratio` or increase `*_max_height_ratio` |
| Text too small | Increase `*_min_size_ratio` |
| Lines too close | Increase `line_height_multiplier` |
| QR code too small/large | Adjust `qr_size_ratio` (0.4-0.7 recommended) |
| Font not loading | Check path relative to `assets/` dir |
| Image not appearing | Verify path and file format (PNG recommended) |

---

## Example: Complete Custom Design

```json
"retro": {
    "front": {
        "colors": {
            "background": ["#FFF8DC", "#FAEBD7"],
            "text": ["#8B4513", "#A0522D"]
        },
        "typography": {
            "font_family": "fonts/Courier/CourierPrime-Bold.ttf",
            "title_size_ratio": 0.07,
            "artist_size_ratio": 0.06
        },
        "layout": {
            "title_y_ratio": 0.12,
            "year_y_ratio": 0.5,
            "artist_y_ratio": 0.88,
            "line_height_multiplier": 1.3
        },
        "images": {
            "backgrounds": ["designs/retro/vinyl_texture.png"]
        }
    },
    "back": {
        "colors": {
            "background": ["#8B4513"],
            "qr_border": ["#FFF8DC"]
        },
        "layout": {
            "qr_size_ratio": 0.55
        },
        "images": {
            "qr_backgrounds": ["designs/retro/paper_texture.png"],
            "qr_center_logos": ["designs/retro/vinyl_icon.png"]
        }
    }
}
```