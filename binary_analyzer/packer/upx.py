#!/usr/bin/env python3

"""
UPX (Ultimate Packer for eXecutables) Detector
"""

def detect(filepath, binary_type, entropy):
    confidence = 0
    try:
        with open(filepath, "rb") as f:
            data = f.read()
            
            # UPX signature 
            if b'UPX!' in data or b'UPX0' in data or b'UPX1' in data:
                confidence += 80
            
            # Section names
            if b'.UPX0' in data or b'.UPX1' in data or b'UPX2' in data:
                confidence += 15
            
            # "This file is packed with the UPX" 
            if b'This file is packed with the UPX' in data:
                confidence = 100
            
            # Import table 
            if binary_type == "PE":
                import_count = data.count(b'.dll\x00')
                if import_count < 5:
                    confidence += 5
            
            # high entropy 
            if entropy and entropy >= 7.0:
                confidence += 10
            
            # Section size ratio
            if binary_type == "ELF" or binary_type == "PE":
                # basic heuristik: unusual section sizes
                if len(data) > 100000:
                    confidence += 5
        
        if confidence >= 50:
            return {
                'name': 'UPX',
                'confidence': min(confidence, 100)
            }
        
    except Exception as e:
        pass
    
    return None
