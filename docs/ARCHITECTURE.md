# Sanrio Characters - Architecture

## Overview

Sanrio Characters is an MCP (Model Context Protocol) server that generates authentic Sanrio character designs using a three-layer categorical framework.

The system uses **ologs** (categorical ontologies) to formalize the aesthetic knowledge embedded in Sanrio character design, making it reproducible, composable, and extensible.

## Three-Layer Architecture

### Layer 1: Categorical Structure (`sanrio.olog.yaml`)

**What composes?** - Formal mathematical structure

This layer defines the design vocabulary and transformation rules using category theory:

- **Types**: Eight fundamental design categories
  - `HeadShape` - 8 silhouettes (round orb, teardrop, curved, blob, etc.)
  - `BodyProportion` - 6 head-to-body ratios
  - `FacialStyle` - 7 expression patterns
  - `ColorTriad` - 8 pastel color schemes
  - `SizeCategory` - 5 functional sizes
  - `EmotionalTone` - 7 emotional archetypes
  - `ConceptType` - 5 concept categories

- **Morphisms**: Transformations between types
  - `design_intent_to_head_shape` - Maps design intent to head silhouette
  - `design_intent_to_body_proportion` - Maps intent to body ratio
  - `design_intent_to_color_triad` - Maps intent to color palette
  - `design_intent_to_facial_style` - Maps intent to facial expression
  - `emotional_tone_to_facial_style` - Maps emotion to expression

- **Commutative Diagrams**: Coherence constraints
  - `proportional_coherence` - Head weight must be grounded by body
  - `emotional_coherence` - All choices must express same emotion
  - `color_saturation_precision` - Saturation must match emotional intensity
  - `expressiveness_balance` - Simple head allows complex face

### Layer 2: Intentionality (`sanrio_intentionality.olog.yaml`)

**Why does it work?** - Design reasoning and psychology

This layer explains the sensory and psychological principles underlying each design category:

**Seven Emotional Archetypes:**

1. **Joyful** - Happiness through proportion exuberance
   - Round shapes + expressive faces + warm colors
   - "This makes me smile"

2. **Melancholic** - Approachability through acknowledged sadness
   - Drooping shapes + closed eyes + muted colors
   - "You're not alone in sadness"

3. **Anxious** - Nervous energy that's still lovable
   - Angular + head-heavy + cool colors + pocket-sized
   - "Worry is relatable"

4. **Sleepy** - Cozy acceptance of rest
   - Drooping + limbless + warm-muted + closed eyes
   - "Rest is precious"

5. **Mischievous** - Harmless trouble-making
   - Slight angles + balanced + expressive + warm + small-medium
   - "Personality and spunk"

6. **Dreamy** - Escape into imagination
   - Organic shapes + ethereal colors + curious expressions
   - "Magic is real"

7. **Determined** - Cute confidence and strength
   - Upright + balanced + focused + saturated + medium-large
   - "You can be powerful and small"

**Universal Design Principles** (hard constraints for all characters):

1. **Proportion Precision** - Ratios matter more than size
2. **Feature Economy** - Each feature must earn its existence
3. **Pastel Restraint** - Stay within soft color spectrum
4. **Approachability Priority** - No sharp edges or threat
5. **Emotional Honesty** - Never pretend to emotions the character doesn't have

### Layer 3: Execution (`server.py`)

**How do we use it?** - Mechanical application

This layer reads from Layers 1 and 2 and generates character designs:

```
User Prompt
    ↓
OlogLoader (reads YAML)
    ↓
Design Intent Mapping (applies morphisms)
    ↓
Coherence Validation (checks diagrams)
    ↓
Character Specification (output)
```

**Key Components:**

- `OlogLoader` - Loads and caches YAML olog specifications
- `_map_intent_to_design_choices()` - Applies morphisms to map intent to taxonomy
- `_get_design_rationale()` - Generates explanation for design choices
- `_generate_sanrio_character_impl()` - Core implementation
- `generate_sanrio_character()` - MCP tool wrapper
- `get_archetype_rules()` - Retrieves archetype design rules

## Data Flow

```
YAML Ologs (Structure + Reasoning)
    ↓
OlogLoader (parse & validate)
    ↓
TAXONOMY + ARCHETYPES (in-memory cache)
    ↓
User Input (user_prompt + design_intent)
    ↓
Emotional Tone Inference (keyword matching)
    ↓
Morphism Application (map intent to choices)
    ↓
Coherence Validation (check diagrams)
    ↓
Character Specification (complete design)
    ↓
Design Guidelines (for image generation)
```

## Design Intent Mapping

The system maps qualitative design intent to specific taxonomy choices:

### Head Shape Morphism
```
"drooping" → elongated_teardrop
"curved" → cat_like_curved
"blob" → minimalist_blob
"geometric" → simplified_geometric
"wide" → wide_and_flat
"pointed" → ovoid_with_point
"round" → large_round_orb
```

### Body Proportion Morphism
```
"tiny" → tiny_torso_large_head
"weighted" → body_focused_30_70
"fluid" → extended_and_fluid
"limbless" → limbless_blob
"head-heavy" → head_dominant_80_20
→ balanced_cute_50_50 (default)
```

### Color Palette Morphism
```
"muted" → dusty_rose_sage_cream
"warm" → butter_yellow_peach_blue
"cool" → lavender_mint_sky_blue
"ethereal" → pale_lavender_pearl_white
"vivid" → coral_mint_cream
→ soft_pink_lavender_mint (default)
```

## Reproducibility

The system is **deterministic**: same user prompt + design intent always produces same design.

This is achieved through:
1. Seeding: `seed = hash(user_prompt) % 100`
2. Consistent morphism application
3. Deterministic archetype matching

## Extensibility

To add a new emotional archetype:

1. Add to `sanrio_intentionality.olog.yaml`:
   ```yaml
   new_emotion_character_archetype:
     core_intention: "..."
     composition_principle: "..."
     why_this_works: "..."
     sensory_principles: [...]
     proportion_rules: {...}
     design_intent_keywords: [...]
     forbidden_combinations: [...]
   ```

2. Update `server.py` name mappings:
   ```python
   name_prefixes["new_emotion_character_archetype"] = "Prefix"
   facial_mapping["new_emotion_character_archetype"] = "facial_style"
   ```

3. Test with the new archetype

## Key Insight

**The three-layer framework separates three concerns:**

- **Layer 1 (Structure)**: What CAN compose? (mathematical)
- **Layer 2 (Reasoning)**: Why DOES it work? (psychological)
- **Layer 3 (Execution)**: How DO we use it? (mechanical)

This separation allows:
- Domain experts to understand design principles (Layer 2)
- Researchers to study formal structure (Layer 1)
- Developers to generate authentic characters (Layer 3)
- Anyone to extend the system with new archetypes

## Files

- `sanrio.olog.yaml` - Categorical structure (14 KB)
- `sanrio_intentionality.olog.yaml` - Design reasoning (20 KB)
- `server.py` - MCP server (480 lines)
- `tools/olog_loader.py` - YAML loading utility
- `tests/test_server.py` - Unit tests
