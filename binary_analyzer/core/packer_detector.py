#!/usr/bin/env python3

import importlib.util
from pathlib import Path

class PackerDetector:
    def __init__(self, filepath, binary_type, entropy):
        self.filepath = filepath
        self.binary_type = binary_type
        self.entropy = entropy
        self.detected_packer = None
        self.confidence = 0
        
        self._load_packer_modules()
        self._detect()
    
    def _load_packer_modules(self):
        
        self.packer_modules = []
        packer_dir = Path(__file__).parent.parent / "packer"
        
        if not packer_dir.exists():
            return
        
        for packer_file in packer_dir.glob("*.py"):
            if packer_file.name.startswith("__"):
                continue
            
            try:
                module_name = packer_file.stem
                spec = importlib.util.spec_from_file_location(module_name, packer_file)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # all module should have detect
                if hasattr(module, 'detect'):
                    self.packer_modules.append(module)
            except Exception as e:
                pass
    
    def _detect(self):
        
        if not self.packer_modules:
            return
        
        best_match = None
        best_confidence = 0
        
        for module in self.packer_modules:
            try:
                result = module.detect(self.filepath, self.binary_type, self.entropy)
                if result and 'confidence' in result:
                    if result['confidence'] > best_confidence:
                        best_confidence = result['confidence']
                        best_match = result
            except Exception as e:
                pass
        
        if best_match and best_confidence >= 50:
            self.detected_packer = best_match.get('name', 'Unknown')
            self.confidence = best_confidence
    
    def display(self):
        if not self.packer_modules:
            print(f"[!] The packer/ folder was either not found or is empty.")
            print(f"Status: Module missing")
            return
        
        if self.detected_packer:
            print(f"Status: Packaged")
            print(f"Packer: {self.detected_packer}")
            print(f"Confidence: {self.confidence}%")
        else:
            # Entropi bazlı genel değerlendirme
            if self.entropy and self.entropy >= 7.5:
                print(f"Status: Probably packaged")
                print(f"Packer: Not detected (High entropy)")
            else:
                print(f"Status: Unpackaged")
                print(f"Packer: Not found")
