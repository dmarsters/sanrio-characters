"""
OlogLoader - Load and validate YAML olog specifications

This module handles loading categorical ontologies (ologs) from YAML files,
validating their structure, and providing access to taxonomy and intentionality data.
"""

from pathlib import Path
import yaml
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class OlogLoader:
    """Load and cache olog specifications from YAML files."""
    
    def __init__(self, olog_dir: Path = None):
        """
        Initialize the OlogLoader.
        
        Args:
            olog_dir: Path to directory containing olog YAML files.
                     If None, looks for data/ologs relative to sanrio_characters package.
        """
        if olog_dir is None:
            # __file__ is sanrio_characters/tools/olog_loader.py
            # Parent: sanrio_characters/tools/
            # Parent.parent: sanrio_characters/
            package_dir = Path(__file__).parent.parent
            olog_dir = package_dir / "data" / "ologs"
        
        self.olog_dir = olog_dir
        self.aesthetic_olog = None
        self.intentionality_olog = None
        self.taxonomy_cache = None
        self.intent_mapping_cache = None
        
        self._load_ologs()
    
    def _load_ologs(self):
        """Load and validate olog YAML files."""
        try:
            # Load aesthetic olog
            aesthetic_path = self.olog_dir / "sanrio.olog.yaml"
            with open(aesthetic_path, 'r') as f:
                self.aesthetic_olog = yaml.safe_load(f)
            logger.info(f"✓ Loaded aesthetic olog from {aesthetic_path}")
            
            # Load intentionality olog
            intentionality_path = self.olog_dir / "sanrio_intentionality.olog.yaml"
            with open(intentionality_path, 'r') as f:
                self.intentionality_olog = yaml.safe_load(f)
            logger.info(f"✓ Loaded intentionality olog from {intentionality_path}")
            
        except FileNotFoundError as e:
            logger.error(f"Olog files not found: {e}")
            raise
        except yaml.YAMLError as e:
            logger.error(f"YAML parsing error: {e}")
            raise
    
    def get_taxonomy(self) -> Dict:
        """Get flattened taxonomy from aesthetic olog."""
        if self.taxonomy_cache is not None:
            return self.taxonomy_cache
        
        # Extract and flatten the types from the olog
        olog = self.aesthetic_olog['olog']
        types_dict = olog.get('types', {})
        
        taxonomy = {}
        
        # Extract instances from each type
        for type_name, type_def in types_dict.items():
            if 'instances' in type_def and isinstance(type_def['instances'], list):
                taxonomy[type_name] = {
                    'description': type_def.get('description', ''),
                    'instances': type_def['instances'],
                    'properties': type_def.get('properties', {})
                }
        
        self.taxonomy_cache = taxonomy
        return self.taxonomy_cache
    
    def get_intentionality_instances(self) -> Dict:
        """Get character archetype instances from intentionality olog."""
        if self.intent_mapping_cache is not None:
            return self.intent_mapping_cache
        
        olog = self.intentionality_olog['olog']
        instances = olog.get('instances', {})
        
        self.intent_mapping_cache = instances
        return self.intent_mapping_cache
    
    def get_commutative_diagrams(self) -> Dict:
        """Get coherence constraints from aesthetic olog."""
        olog = self.aesthetic_olog['olog']
        return olog.get('commutative_diagrams', {})
    
    def get_archetype_rules(self, archetype_name: str) -> Optional[Dict]:
        """Get design rules for a specific archetype."""
        instances = self.get_intentionality_instances()
        return instances.get(archetype_name)
