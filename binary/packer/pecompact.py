#!/usr/bin/env python3
"""
PECompact Detector Module
"""

def detect(filepath, binary_type, entropy):
    if binary_type != "PE":
        return None

    confidence = 0
    
    try:
        with open(filepath, "rb") as f:
            data = f.read()
            
            # 1. String signs
            pecompact_markers = [
                b'PECompact2', 
                b'PEC2', 
                b'PECompact V',
                b'Bitsum Technologies' # Yapımcı firma
            ]
            
            for marker in pecompact_markers:
                if marker in data:
                    confidence += 70
                    break

            pec_sections = [b'.pec1', b'.pec2', b'PEC2', b'PEC2VSD']
            for section in pec_sections:
                if section in data:
                    confidence += 25
            
            # JMP/PUSH/RET gibi tipik unpacker starts
            if b'\xeb\x06\xff\xff\xff\xff\x00\x00' in data[:2048]:
                confidence += 20

            if entropy and entropy >= 7.2:
                confidence += 10

            if b'LoadLibraryA' in data and b'GetProcAddress' in data:
                confidence += 5

        if confidence >= 40:
            return {
                'name': 'PECompact',
                'confidence': min(confidence, 100)
            }
            
    except Exception:
        pass
    
    return None
