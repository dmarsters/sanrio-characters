"""
Tests for Sanrio Characters MCP Server

Run with: pytest tests/
"""

import pytest
from pathlib import Path
from sanrio_characters.server import (
    _generate_sanrio_character_impl,
    get_archetype_rules,
    OLOG_LOADER,
    TAXONOMY,
    ARCHETYPES
)


class TestOlogLoading:
    """Test YAML olog loading and validation."""
    
    def test_olog_loader_initialization(self):
        """Test that OlogLoader initializes without errors."""
        assert OLOG_LOADER is not None
        assert OLOG_LOADER.aesthetic_olog is not None
        assert OLOG_LOADER.intentionality_olog is not None
    
    def test_taxonomy_loading(self):
        """Test that taxonomy loads correctly."""
        assert TAXONOMY is not None
        assert len(TAXONOMY) > 0
        assert 'HeadShape' in TAXONOMY
        assert 'BodyProportion' in TAXONOMY
        assert 'ColorTriad' in TAXONOMY
        assert 'FacialStyle' in TAXONOMY
        assert 'SizeCategory' in TAXONOMY
    
    def test_archetypes_loading(self):
        """Test that archetypes load correctly."""
        assert ARCHETYPES is not None
        assert len(ARCHETYPES) == 7
        
        expected_archetypes = {
            'joyful_character_archetype',
            'melancholic_character_archetype',
            'anxious_character_archetype',
            'sleepy_character_archetype',
            'mischievous_character_archetype',
            'dreamy_character_archetype',
            'determined_character_archetype'
        }
        assert set(ARCHETYPES.keys()) == expected_archetypes


class TestCharacterGeneration:
    """Test character generation functionality."""
    
    def test_generate_character_basic(self):
        """Test basic character generation without design intent."""
        result = _generate_sanrio_character_impl("happy character")
        
        assert result is not None
        assert 'character_name' in result
        assert 'emotional_tone' in result
        assert 'head_shape' in result
        assert 'body_proportion' in result
        assert 'color_triad' in result
        assert 'facial_style' in result
        assert 'size_category' in result
    
    def test_generate_character_with_design_intent(self):
        """Test character generation with design intent."""
        design_intent = {
            "mood": "sluggish, heavy",
            "weight_feeling": "drooping, weighted",
            "color_feeling": "muted, dusty",
            "size_implication": "small, insignificant",
            "primary_shape": "drooping or curved"
        }
        
        result = _generate_sanrio_character_impl(
            "the feeling of procrastination",
            design_intent=design_intent
        )
        
        assert result is not None
        assert result['character_name'] is not None
        assert result['head_shape'] == 'elongated_teardrop'
        assert result['body_proportion'] == 'body_focused_30_70'
        assert result['color_triad'] == 'dusty_rose_sage_cream'
    
    def test_deterministic_generation(self):
        """Test that same prompt generates same design."""
        result1 = _generate_sanrio_character_impl("procrastination")
        result2 = _generate_sanrio_character_impl("procrastination")
        
        assert result1['character_name'] == result2['character_name']
        assert result1['head_shape'] == result2['head_shape']
        assert result1['body_proportion'] == result2['body_proportion']
        assert result1['design_seed'] == result2['design_seed']
    
    def test_character_has_design_guidelines(self):
        """Test that generated character includes design guidelines."""
        result = _generate_sanrio_character_impl("test character")
        
        assert 'design_guidelines' in result
        guidelines = result['design_guidelines']
        assert 'aesthetic' in guidelines
        assert 'head_description' in guidelines
        assert 'body_description' in guidelines
        assert 'facial_description' in guidelines
        assert 'universal_principles' in guidelines
    
    def test_character_has_olog_metadata(self):
        """Test that generated character includes olog source metadata."""
        result = _generate_sanrio_character_impl("test character")
        
        assert 'olog_source' in result
        olog_source = result['olog_source']
        assert olog_source['aesthetic_olog'] == 'sanrio.olog.yaml'
        assert olog_source['intentionality_olog'] == 'sanrio_intentionality.olog.yaml'
        assert 'morphisms_applied' in olog_source
        assert 'commutative_diagrams_checked' in olog_source


class TestArchetypeRules:
    """Test archetype rules retrieval."""
    
    def test_get_melancholic_archetype_rules(self):
        """Test retrieving melancholic archetype rules."""
        rules = get_archetype_rules("melancholic_character_archetype")
        
        assert 'error' not in rules
        assert rules['archetype'] == 'melancholic_character_archetype'
        assert 'core_intention' in rules
        assert 'composition_principle' in rules
        assert 'why_this_works' in rules
        assert 'sensory_principles' in rules
        assert 'design_keywords' in rules
    
    def test_get_joyful_archetype_rules(self):
        """Test retrieving joyful archetype rules."""
        rules = get_archetype_rules("joyful_character_archetype")
        
        assert 'error' not in rules
        assert rules['archetype'] == 'joyful_character_archetype'
        assert len(rules['design_keywords']) > 0
    
    def test_invalid_archetype(self):
        """Test error handling for invalid archetype."""
        rules = get_archetype_rules("nonexistent_archetype")
        
        assert 'error' in rules
        assert 'Unknown archetype' in rules['error']


class TestDesignChoices:
    """Test design choice mapping."""
    
    def test_drooping_maps_to_elongated_teardrop(self):
        """Test that 'drooping' maps to elongated_teardrop head shape."""
        result = _generate_sanrio_character_impl(
            "drooping",
            design_intent={
                "weight_feeling": "drooping",
                "primary_shape": "drooping"
            }
        )
        assert result['head_shape'] == 'elongated_teardrop'
    
    def test_muted_maps_to_dusty_palette(self):
        """Test that 'muted' maps to dusty color palette."""
        result = _generate_sanrio_character_impl(
            "muted",
            design_intent={
                "color_feeling": "muted",
                "weight_feeling": "heavy",
                "primary_shape": "round"
            }
        )
        assert result['color_triad'] == 'dusty_rose_sage_cream'
    
    def test_tiny_maps_to_small_category(self):
        """Test that 'tiny' maps to small size category."""
        result = _generate_sanrio_character_impl(
            "tiny",
            design_intent={
                "size_implication": "tiny",
                "weight_feeling": "light",
                "primary_shape": "round"
            }
        )
        assert result['size_category'] == 'small_plush_toy'
