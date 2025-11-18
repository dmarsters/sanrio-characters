# Sanrio Characters - Usage Guide

## Installation

```bash
git clone https://github.com/dmarsters/sanrio-characters.git
cd sanrio-characters
pip install -e .
```

## Quick Start

### Direct Function Call

```python
from sanrio_characters.server import _generate_sanrio_character_impl

result = _generate_sanrio_character_impl(
    user_prompt="the feeling of procrastination",
    design_intent={
        "mood": "sluggish, heavy, time-slipping",
        "weight_feeling": "drooping, weighted",
        "color_feeling": "muted, dusty, desaturated",
        "size_implication": "small, insignificant",
        "primary_shape": "drooping or curved"
    }
)

print(f"Character: {result['character_name']}")
print(f"Emotional Tone: {result['emotional_tone']}")
print(f"Head Shape: {result['head_shape']}")
print(f"Body Proportion: {result['body_proportion']}")
print(f"Color Triad: {result['color_triad']}")
print(f"Design Rationale: {result['design_rationale']}")
```

### MCP Server

Start the server:

```bash
python -m sanrio_characters.server
```

Then call via MCP client:

```python
# Initialize MCP connection
# Call generate_sanrio_character tool with parameters
# Call get_archetype_rules tool to retrieve archetype rules
```

## Function Reference

### `_generate_sanrio_character_impl(user_prompt, design_intent=None)`

Generate a complete Sanrio character design.

**Parameters:**
- `user_prompt` (str): User's creative concept (e.g., "the feeling of procrastination")
- `design_intent` (dict, optional): Design analysis with keys:
  - `mood`: Creative mood description
  - `weight_feeling`: How design should feel (drooping, weighted, etc.)
  - `color_feeling`: Color palette guidance (muted, warm, ethereal, etc.)
  - `size_implication`: Size guidance (tiny, small, medium, large)
  - `primary_shape`: Dominant shape characteristic (drooping, curved, blob, etc.)

**Returns:**
Dictionary with keys:
- `character_name`: Generated name
- `emotional_tone`: Detected emotional archetype
- `head_shape`: Head silhouette
- `body_proportion`: Head-to-body ratio
- `facial_style`: Expression pattern
- `color_triad`: Color palette
- `size_category`: Functional size
- `design_guidelines`: Instructions for image generation
- `design_rationale`: Why these choices were made
- `olog_source`: Metadata about which ologs were used

### `get_archetype_rules(emotional_tone)`

Get design rules for a specific emotional archetype.

**Parameters:**
- `emotional_tone`: One of:
  - `joyful_character_archetype`
  - `melancholic_character_archetype`
  - `anxious_character_archetype`
  - `sleepy_character_archetype`
  - `mischievous_character_archetype`
  - `dreamy_character_archetype`
  - `determined_character_archetype`

**Returns:**
Dictionary with:
- `core_intention`: The emotional promise
- `composition_principle`: Design rules
- `sensory_principles`: Why this archetype works
- `design_keywords`: Keywords that trigger this archetype
- `forbidden_combinations`: What contradicts this emotion
- `examples`: Real Sanrio characters that embody this

## Design Intent Keywords

The system recognizes these keywords to infer emotional tone:

### Melancholic
- "sad", "melancholy", "introspection", "withdrawn", "quiet", "alone"
- "procrastination", "regret", "nostalgia"

### Joyful
- "happy", "joy", "celebration", "playful", "energetic", "excited"

### Anxious
- "worried", "nervous", "tense", "anxious", "scared", "uncertain"

### Sleepy
- "sleepy", "tired", "cozy", "lazy", "rest", "nap"

### Mischievous
- "mischievous", "playful", "naughty", "cheeky", "trouble"

### Dreamy
- "dreamy", "magical", "ethereal", "fantasy", "wonder"

### Determined
- "strong", "determined", "powerful", "confident", "brave"

## Design Intent Mappings

### Weight Feeling → Head Shape
```
"drooping" → elongated_teardrop
"curved" / "flowing" → cat_like_curved
"blob" / "amorphous" → minimalist_blob
"geometric" / "sharp" → simplified_geometric
"wide" / "flat" → wide_and_flat
"pointed" / "spike" → ovoid_with_point
"round" / "soft" → large_round_orb
```

### Weight Feeling → Body Proportion
```
"tiny" / "insignificant" → tiny_torso_large_head
"weighted" / "heavy" / "grounded" → body_focused_30_70
"fluid" / "flowing" / "extended" → extended_and_fluid
"limbless" / "blob" → limbless_blob
"head-heavy" / "top-heavy" → head_dominant_80_20
(default) → balanced_cute_50_50
```

### Color Feeling → Color Palette
```
"muted" / "dusty" / "desaturated" → dusty_rose_sage_cream
"warm" / "cozy" → butter_yellow_peach_blue
"cool" → lavender_mint_sky_blue
"ethereal" → pale_lavender_pearl_white
"vivid" → coral_mint_cream
(default) → soft_pink_lavender_mint
```

### Size Implication → Size Category
```
"tiny" / "pocket" / "miniature" → small_plush_toy
"small" / "delicate" → small_decorative
"medium" / "standard" → medium_standard
"large" / "prominent" → large_display
(default) → medium_standard
```

## Examples

### Example 1: Procrastination Character

```python
result = _generate_sanrio_character_impl(
    user_prompt="the feeling of procrastination",
    design_intent={
        "mood": "sluggish, heavy, time-slipping",
        "weight_feeling": "drooping, weighted",
        "color_feeling": "muted, dusty",
        "size_implication": "small, insignificant",
        "primary_shape": "drooping"
    }
)

# Result:
# character_name: "MelanPro"
# emotional_tone: "melancholic_character_archetype"
# head_shape: "elongated_teardrop"
# body_proportion: "body_focused_30_70"
# color_triad: "dusty_rose_sage_cream"
# size_category: "small_plush_toy"
```

### Example 2: Joy Character

```python
result = _generate_sanrio_character_impl(
    user_prompt="pure happiness and celebration",
    design_intent={
        "mood": "bubbly, energetic",
        "weight_feeling": "light, bouncy",
        "color_feeling": "warm, vivid",
        "size_implication": "medium",
        "primary_shape": "round"
    }
)

# Result:
# character_name: "JoyPur"
# emotional_tone: "joyful_character_archetype"
# head_shape: "large_round_orb"
# body_proportion: "balanced_cute_50_50"
# color_triad: "soft_pink_lavender_mint"
# size_category: "medium_standard"
```

### Example 3: Dreamy Character (No Design Intent)

```python
result = _generate_sanrio_character_impl("magical forest spirit")

# Result uses archetype defaults for dreamy emotion
# character_name: "DreamMag"
# emotional_tone: "dreamy_character_archetype"
# Design guidelines included for image generation
```

## Design Guidelines Output

Each generated character includes `design_guidelines` with:

```python
{
    "aesthetic": "Sanrio style: cute, simplified shapes, minimal features, pastel-friendly",
    "head_description": "Use a elongated teardrop shape for the head",
    "body_description": "Body should be body focused 30 70",
    "facial_description": "Face features: closed happy eyes",
    "size_note": "Character size: small plush toy",
    "color_note": "Use dusty rose sage cream color palette",
    "universal_principles": [
        "Proportion precision: maintain ratio relationships",
        "Feature economy: each feature must earn its existence",
        "Pastel restraint: stay within soft color spectrum",
        "Approachability priority: no sharp edges or judgment",
        "Emotional honesty: character must be authentic to its emotion"
    ]
}
```

Use these guidelines when creating images or refining character specifications.

## Testing

Run the test suite:

```bash
pytest tests/
```

Run specific test class:

```bash
pytest tests/test_server.py::TestCharacterGeneration
```

Run with verbose output:

```bash
pytest -v tests/
```

## Architecture

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed explanation of:
- The three-layer framework (structure, intentionality, execution)
- How ologs define design space
- How morphisms map intent to choices
- How commutative diagrams enforce coherence
