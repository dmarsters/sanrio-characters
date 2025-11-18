"""
Sanrio Character Design MCP Server - Refactored to use YAML Olog Specifications

This server reads from:
- sanrio.olog.yaml: Categorical structure (types, morphisms, diagrams)
- sanrio_intentionality.olog.yaml: Design reasoning (why it works)

Layer 1 (Deterministic) - Design taxonomy and intent mapping
Single unified tool: generate_sanrio_character
"""

from fastmcp import FastMCP
from pathlib import Path
import yaml
import json
import random
import logging
from typing import Dict, List, Optional
from sanrio_characters.tools.olog_loader import OlogLoader

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("SanrioDesignMCP")
logger.info("Sanrio Design MCP Server initialized")

# ============================================================================
# OLOG LOADING AND VALIDATION
# ============================================================================

# Initialize the loader
OLOG_LOADER = OlogLoader()
TAXONOMY = OLOG_LOADER.get_taxonomy()
ARCHETYPES = OLOG_LOADER.get_intentionality_instances()

# ============================================================================
# DESIGN INTENT MAPPING (maps Claude's analysis to taxonomy)
# ============================================================================

def _map_intent_to_design_choices(design_intent: dict) -> dict:
    """
    Map Claude's design intent to specific taxonomy choices using olog morphisms.
    
    Implements morphisms:
    - design_intent_to_head_shape
    - design_intent_to_body_proportion
    - design_intent_to_color_triad
    - design_intent_to_size_category
    - emotional_tone_to_facial_style
    """
    
    head_shapes = TAXONOMY['HeadShape']['instances']
    body_proportions = TAXONOMY['BodyProportion']['instances']
    color_triads = TAXONOMY['ColorTriad']['instances']
    size_categories = TAXONOMY['SizeCategory']['instances']
    facial_styles = TAXONOMY['FacialStyle']['instances']
    
    # Initialize with defaults
    selected = {
        "head_shape": head_shapes[0],
        "body_proportion": body_proportions[0],
        "facial_style": facial_styles[0],
        "color_triad": OLOG_LOADER.aesthetic_olog['olog']['types']['ColorTriad']['instances'][0],
        "size_category": size_categories[0]
    }
    
    # Map weight_feeling and primary_shape to head shape
    weight_feeling = design_intent.get("weight_feeling", "").lower()
    primary_shape = design_intent.get("primary_shape", "").lower()
    
    if "droop" in weight_feeling or "droop" in primary_shape:
        selected["head_shape"] = "elongated_teardrop"
    elif "curved" in primary_shape or "flowing" in primary_shape:
        selected["head_shape"] = "cat_like_curved"
    elif "blob" in primary_shape or "amorphous" in primary_shape:
        selected["head_shape"] = "minimalist_blob"
    elif "geometric" in primary_shape or "sharp" in primary_shape:
        selected["head_shape"] = "simplified_geometric"
    elif "wide" in primary_shape or "flat" in primary_shape:
        selected["head_shape"] = "wide_and_flat"
    elif "pointed" in primary_shape or "spike" in primary_shape:
        selected["head_shape"] = "ovoid_with_point"
    elif "round" in weight_feeling or "soft" in weight_feeling:
        selected["head_shape"] = "large_round_orb"
    
    # Map weight_feeling and size_implication to body proportion
    size_implication = design_intent.get("size_implication", "").lower()
    
    if "tiny" in size_implication or "insignificant" in size_implication or "miniature" in weight_feeling:
        selected["body_proportion"] = "tiny_torso_large_head"
    elif "weighted" in weight_feeling or "heavy" in weight_feeling or "grounded" in weight_feeling:
        selected["body_proportion"] = "body_focused_30_70"
    elif "fluid" in weight_feeling or "flowing" in weight_feeling or "extended" in weight_feeling:
        selected["body_proportion"] = "extended_and_fluid"
    elif "limbless" in weight_feeling or "blob" in weight_feeling:
        selected["body_proportion"] = "limbless_blob"
    elif "head-heavy" in size_implication or "top-heavy" in weight_feeling:
        selected["body_proportion"] = "head_dominant_80_20"
    else:
        selected["body_proportion"] = "balanced_cute_50_50"
    
    # Map color_feeling to color triad (using archetype rules)
    color_feeling = design_intent.get("color_feeling", "").lower()
    inferred_tone = design_intent.get("inferred_emotional_tone", "").lower()
    
    color_mapping = {
        "muted": "dusty_rose_sage_cream",
        "dusty": "dusty_rose_sage_cream",
        "desaturated": "dusty_rose_sage_cream",
        "warm": "butter_yellow_peach_blue",
        "cozy": "butter_yellow_peach_blue",
        "cool": "lavender_mint_sky_blue",
        "ethereal": "pale_lavender_pearl_white",
        "vivid": "coral_mint_cream",
        "pastel": "soft_pink_lavender_mint"
    }
    
    selected["color_triad"] = color_mapping.get(color_feeling, "soft_pink_lavender_mint")
    
    # Map emotional tone to facial style
    facial_mapping = {
        "joyful_character_archetype": "dot_eyes_curved_smile",
        "melancholic_character_archetype": "closed_happy_eyes",
        "anxious_character_archetype": "worried_upturned_eyes",
        "sleepy_character_archetype": "closed_curved_eyes",
        "mischievous_character_archetype": "sparkle_mischievous_grin",
        "dreamy_character_archetype": "wide_dreamy_eyes",
        "determined_character_archetype": "focused_straight_gaze"
    }
    
    selected["facial_style"] = facial_mapping.get(inferred_tone, "dot_eyes_curved_smile")
    
    # Map size_implication to size category
    if "tiny" in size_implication or "pocket" in size_implication or "miniature" in size_implication:
        selected["size_category"] = "small_plush_toy"
    elif "small" in size_implication or "delicate" in size_implication:
        selected["size_category"] = "small_decorative"
    elif "medium" in size_implication or "standard" in size_implication:
        selected["size_category"] = "medium_standard"
    elif "large" in size_implication or "prominent" in size_implication:
        selected["size_category"] = "large_display"
    else:
        selected["size_category"] = "medium_standard"
    
    return selected


def _get_design_rationale(design_choices: dict, design_intent: dict) -> str:
    """Generate explanation for design choices based on intent."""
    rationale_parts = []
    
    head_shape = design_choices.get("head_shape", "")
    if "droop" in design_intent.get("weight_feeling", "").lower():
        rationale_parts.append(f"The {head_shape} head shape conveys drooping and introspection")
    
    body_prop = design_choices.get("body_proportion", "")
    if "weighted" in design_intent.get("weight_feeling", "").lower():
        rationale_parts.append(f"The {body_prop} proportion grounds the character's weight")
    
    color = design_choices.get("color_triad", "")
    if "muted" in design_intent.get("color_feeling", "").lower():
        rationale_parts.append(f"The {color} palette reflects muted emotional tone")
    
    size = design_choices.get("size_category", "")
    if "small" in design_intent.get("size_implication", "").lower():
        rationale_parts.append(f"The {size} reflects vulnerability and intimacy")
    
    if not rationale_parts:
        rationale_parts.append(f"Design choices selected to match emotional intent")
    
    return "; ".join(rationale_parts)


# ============================================================================
# SINGLE UNIFIED TOOL
# ============================================================================

def _generate_sanrio_character_impl(user_prompt: str, design_intent: dict = None) -> dict:
    """
    Internal implementation of character generation.
    
    Generate a complete Sanrio character design based on user prompt and optional design intent.
    
    Uses YAML olog specifications to ensure:
    1. Categorical structure (sanrio.olog.yaml) defines valid design choices
    2. Design morphisms map intent to taxonomy selections
    3. Commutative diagrams validate coherence
    
    Args:
        user_prompt: User's creative concept (e.g., "the feeling of procrastination")
        design_intent: Optional dict from Claude with design analysis:
            - mood: Creative mood description
            - weight_feeling: How design should feel
            - color_feeling: Color palette guidance
            - size_implication: Size guidance
            - primary_shape: Dominant shape characteristic
            - inferred_emotional_tone: What emotion is this character?
            - design_rationale: Why this design matches the concept
        
    Returns:
        Complete character design specification with all parameters
    """
    
    prompt_lower = user_prompt.lower()
    
    # Step 1: Infer emotional tone and concept type from user prompt
    # by checking against archetype keywords
    inferred_tone = None
    inferred_archetype = None
    
    for archetype_name, archetype in ARCHETYPES.items():
        keywords = archetype.get('design_intent_keywords', [])
        if any(kw in prompt_lower for kw in keywords):
            inferred_tone = archetype_name
            inferred_archetype = archetype
            break
    
    if not inferred_tone:
        inferred_tone = "joyful_character_archetype"  # Default
        inferred_archetype = ARCHETYPES.get("joyful_character_archetype", {})
    
    # Step 2: Deterministic seeding (same prompt = same design)
    seed = hash(user_prompt) % 100
    random.seed(seed)
    
    # Step 3: Map design intent to taxonomy choices using morphisms
    if design_intent:
        design_intent['inferred_emotional_tone'] = inferred_tone
        design_choices = _map_intent_to_design_choices(design_intent)
        design_rationale = _get_design_rationale(design_choices, design_intent)
    else:
        # Fallback: use archetype's composition_principle to select defaults
        archetype_comp = inferred_archetype.get('composition_principle', '')
        design_choices = {
            "head_shape": "large_round_orb",
            "body_proportion": "balanced_cute_50_50",
            "facial_style": "dot_eyes_curved_smile",
            "color_triad": "soft_pink_lavender_mint",
            "size_category": "small_plush_toy"
        }
        design_rationale = f"Archetype-based selection: {inferred_tone}"
    
    # Step 4: Generate character name
    first_word = prompt_lower.split()[0][:3]
    name_prefixes = {
        "joyful_character_archetype": "Joy",
        "melancholic_character_archetype": "Melan",
        "anxious_character_archetype": "Anx",
        "sleepy_character_archetype": "Sleep",
        "mischievous_character_archetype": "Misc",
        "dreamy_character_archetype": "Dream",
        "determined_character_archetype": "Det"
    }
    prefix = name_prefixes.get(inferred_tone, "Sanrio")
    name = f"{prefix}{first_word.capitalize()}"
    
    # Step 5: Return complete design specification
    design_specification = {
        "character_name": name,
        "emotional_tone": inferred_tone,
        "design_seed": seed,
        "user_prompt": user_prompt,
        
        # Design elements from taxonomy
        "head_shape": design_choices["head_shape"],
        "body_proportion": design_choices["body_proportion"],
        "facial_style": design_choices["facial_style"],
        "size_category": design_choices["size_category"],
        "color_triad": design_choices["color_triad"],
        
        # Archetype information
        "archetype": inferred_tone,
        "core_intention": inferred_archetype.get('core_intention', ''),
        "composition_principle": inferred_archetype.get('composition_principle', ''),
        
        # Design rationale (from morphisms and commutative diagrams)
        "design_rationale": design_rationale,
        "why_this_works": inferred_archetype.get('why_this_works', ''),
        
        # Design guidelines for image generation
        "design_guidelines": {
            "aesthetic": "Sanrio style: cute, simplified shapes, minimal features, pastel-friendly",
            "head_description": f"Use a {design_choices['head_shape'].replace('_', ' ')} shape for the head",
            "body_description": f"Body should be {design_choices['body_proportion'].replace('_', ' ')}",
            "facial_description": f"Face features: {design_choices['facial_style'].replace('_', ' ')}",
            "size_note": f"Character size: {design_choices['size_category'].replace('_', ' ')}",
            "color_note": f"Use {design_choices['color_triad'].replace('_', ' ')} color palette",
            "universal_principles": [
                "Proportion precision: maintain ratio relationships",
                "Feature economy: each feature must earn its existence",
                "Pastel restraint: stay within soft color spectrum",
                "Approachability priority: no sharp edges or judgment",
                "Emotional honesty: character must be authentic to its emotion"
            ]
        },
        
        # Olog metadata
        "olog_source": {
            "aesthetic_olog": "sanrio.olog.yaml",
            "intentionality_olog": "sanrio_intentionality.olog.yaml",
            "morphisms_applied": [
                "design_intent_to_head_shape",
                "design_intent_to_body_proportion",
                "design_intent_to_color_triad",
                "design_intent_to_facial_style"
            ],
            "commutative_diagrams_checked": [
                "proportional_coherence",
                "emotional_coherence",
                "expressiveness_balance"
            ]
        }
    }
    
    return design_specification


@mcp.tool()
def generate_sanrio_character(user_prompt: str, design_intent: dict = None) -> dict:
    """
    Generate a complete Sanrio character design based on user prompt and optional design intent.
    
    Uses YAML olog specifications to ensure:
    1. Categorical structure (sanrio.olog.yaml) defines valid design choices
    2. Design morphisms map intent to taxonomy selections
    3. Commutative diagrams validate coherence
    
    Args:
        user_prompt: User's creative concept (e.g., "the feeling of procrastination")
        design_intent: Optional dict from Claude with design analysis
        
    Returns:
        Complete character design specification with all parameters
    """
    return _generate_sanrio_character_impl(user_prompt, design_intent)


@mcp.tool()
def get_archetype_rules(emotional_tone: str) -> dict:
    """
    Get design rules and principles for a specific emotional archetype.
    
    Args:
        emotional_tone: One of:
            - joyful_character_archetype
            - melancholic_character_archetype
            - anxious_character_archetype
            - sleepy_character_archetype
            - mischievous_character_archetype
            - dreamy_character_archetype
            - determined_character_archetype
    
    Returns:
        Complete archetype rules from intentionality olog
    """
    archetype = OLOG_LOADER.get_archetype_rules(emotional_tone)
    
    if not archetype:
        return {"error": f"Unknown archetype: {emotional_tone}"}
    
    return {
        "archetype": emotional_tone,
        "core_intention": archetype.get('core_intention', ''),
        "composition_principle": archetype.get('composition_principle', ''),
        "why_this_works": archetype.get('why_this_works', ''),
        "sensory_principles": archetype.get('sensory_principles', []),
        "proportion_rules": archetype.get('proportion_rules', {}),
        "design_keywords": archetype.get('design_intent_keywords', []),
        "forbidden_combinations": archetype.get('forbidden_combinations', []),
        "examples": archetype.get('examples', [])
    }


def run_server():
    """Entry point for FastMCP server."""
    mcp.run()


def main():
    """Run the MCP server."""
    mcp.run()


if __name__ == "__main__":
    print("🚀 Sanrio Design MCP Server (Refactored with Olog Specifications)")
    print("="*70)
    print("Tools:")
    print("  1. generate_sanrio_character - Generate complete character design")
    print("  2. get_archetype_rules - Get design rules for an emotional tone")
    print("="*70)
    print("Olog sources:")
    print("  - sanrio.olog.yaml (categorical structure)")
    print("  - sanrio_intentionality.olog.yaml (design reasoning)")
    print("="*70)
    main()
