# Sanrio Characters

A categorical specification of Sanrio character design aesthetics using **ologs** (ontology logs from category theory).

## What Is This?

**Sanrio Characters** formalizes how to create adorable characters by mapping **design intent** (mood, weight, color, size) to **design choices** (head shapes, proportions, colors, expressions) through categorical morphisms.

Rather than "draw something cute," this system says: **"Cute is mathematical. If you nail the proportions, colors, and features precisely, cuteness emerges."**

## The Three-Layer Framework

### Layer 1: Categorical Structure (`sanrio.olog.yaml`)
- **Types**: HeadShape, BodyProportion, FacialStyle, ColorTriad, SizeCategory, EmotionalTone
- **Morphisms**: design_intent → design_choice transformations
- **Commutative Diagrams**: Coherence constraints (proportional, emotional, sensory)

### Layer 2: Intentionality (`sanrio_intentionality.olog.yaml`)
- **7 Emotional Archetypes**: Joyful, Melancholic, Anxious, Sleepy, Mischievous, Dreamy, Determined
- **Sensory Principles**: Why each archetype works using psychology
- **Universal Principles**: 5 hard constraints all characters must follow

### Layer 3: Execution (`server.py`)
- **MCP Server**: Reads from YAML ologs (not hardcoded)
- **Two Tools**:
  - `generate_sanrio_character()` - Creates complete character specifications
  - `get_archetype_rules()` - Returns design rules for each archetype

## The 7 Emotional Archetypes

| Archetype | Composition | Why It Works |
|-----------|-------------|--------------|
| **Joyful** | Round shapes + expressive faces + warm colors | Roundness = safe, warmth = optimistic |
| **Melancholic** | Drooping shapes + closed eyes + muted colors | Drooping = sadness, muted = authentic |
| **Anxious** | Slight angles + head-heavy + cool colors + small | Tension without threat, small = vulnerable |
| **Sleepy** | Drooping + limbless + warm-muted + closed eyes | Drooping = relaxation, limbless = melting |
| **Mischievous** | Slight angles + warm colors + expressive + small-med | Angles = sharpness without menace, warm = kind |
| **Dreamy** | Organic impossible shapes + ethereal colors | Organic = unreality, ethereal = otherworldly |
| **Determined** | Upright + balanced + focused + saturated + med-large | Upright = confident, saturated = energy |

## Universal Design Principles

Every character must follow these (hard constraints):

1. **Proportion Precision** - Ratios matter more than size
2. **Feature Economy** - Each feature must earn its existence
3. **Pastel Restraint** - Stay within soft color spectrum
4. **Approachability Priority** - No sharp edges or judgment
5. **Emotional Honesty** - Never pretend to emotions the character doesn't have

## Installation

### From GitHub
```bash
pip install git+https://github.com/lushy/sanrio-characters.git
```

### Local Development
```bash
git clone https://github.com/lushy/sanrio-characters.git
cd sanrio-characters
pip install -e ".[dev]"
```

## Quick Start

### Generate a Character

```python
from sanrio_characters.server import mcp

result = mcp.run_tool("generate_sanrio_character", {
    "user_prompt": "the feeling of procrastination",
    "design_intent": {
        "mood": "sluggish, heavy, time-slipping",
        "weight_feeling": "drooping, weighted",
        "color_feeling": "muted, dusty, desaturated",
        "size_implication": "small, insignificant",
        "primary_shape": "drooping or curved"
    }
})
```

### Get Archetype Rules

```python
result = mcp.run_tool("get_archetype_rules", {
    "emotional_tone": "melancholic_character_archetype"
})
```

## Example: Procrastination Character

**User Intent:**
```
mood: "sluggish, heavy, time-slipping"
weight_feeling: "drooping, weighted"
color_feeling: "muted, dusty, desaturated"
size_implication: "small, insignificant"
primary_shape: "drooping or curved"
```

**Morphism Application:**
- drooping → `elongated_teardrop` (head shape)
- weighted → `body_focused_30_70` (body proportion)
- muted, dusty → `dusty_rose_sage_cream` (color)
- small → `tiny_torso_large_head` (proportion)
- melancholic mood → `closed_happy_eyes` (facial style)

**Result:** A character that **feels like procrastination** because every design choice expresses sadness and heaviness.

## Architecture

```
sanrio_characters/
├── __init__.py
├── server.py                 # MCP server with OlogLoader
├── data/
│   ├── ologs/
│   │   ├── sanrio.olog.yaml
│   │   └── sanrio_intentionality.olog.yaml
│   └── legacy/              # For future compatibility
└── tools/
    └── __init__.py
```

## How It Works

1. **User submits concept** (e.g., "procrastination")
2. **Claude analyzes design intent** (mood, weight, color, size, shape)
3. **Morphisms apply transformations** (intent → design choices)
4. **Commutative diagrams validate coherence** (proportional, emotional, sensory)
5. **Character specification returned** (ready for image generation)

## Composition with Other Domains

The ologs are designed to compose with other aesthetic frameworks:

- **Sanrio + Slapstick Comedy** (both use exaggeration and character)
- **Sanrio + Magazine Photography** (both use authentic aesthetics)
- **Sanrio + Game Shows** (both use visual spectacle)

Identify shared categorical structure and implement natural transformations.

## Key Insight

**The system separates three concerns:**

- **Layer 1 (Structure)**: What CAN compose? (Mathematical)
- **Layer 2 (Intentionality)**: Why DOES it work? (Psychological)
- **Layer 3 (Execution)**: How DO we use it? (Mechanical)

This means anyone can:
- Read Layer 2 and understand Sanrio's design philosophy
- Read Layer 1 and see the formal structure
- Use Layer 3 and generate authentic characters

## Files

- **sanrio.olog.yaml** (14 KB) - Categorical structure
- **sanrio_intentionality.olog.yaml** (20 KB) - Design reasoning
- **server.py** (20 KB) - MCP server implementation
- **pyproject.toml** - Package configuration
- **README.md** - This file

## Testing

```bash
pip install -e ".[dev]"
pytest tests/ -v
```

## License

MIT License - see LICENSE file for details

## Contact

For questions, issues, or contributions:
- GitHub: https://github.com/lushy/sanrio-characters
- Email: contact@lushy.ai
