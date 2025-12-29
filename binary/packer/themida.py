#!/usr/bin/env python3
"""
Themida / WinLicense Detector
"""

def detect(filepath, binary_type, entropy):
    if binary_type != "PE":
        return None
    
    confidence = 0
    
    try:
        with open(filepath, "rb") as f:
            data = f.read()
            
            # Themida section names
            themida_sections = [
                b'.themida',
                b'.winlice',
                b'.boot',
                b'.shared'
            ]
            
            for section in themida_sections:
                if section in data:
                    confidence += 30
            
            # Themida strings
            themida_strings = [
                b'Themida',
                b'WinLicense',
                b'Oreans',
                b'SecureEngine'
            ]
            
            for string in themida_strings:
                if string in data:
                    confidence += 25
            
            if entropy and entropy >= 7.8:
                confidence += 15
            
            # Anti-debug ve VM detection
            anti_strings = [
                b'IsDebuggerPresent',
                b'CheckRemoteDebuggerPresent',
                b'NtQueryInformationProcess'
            ]
            
            anti_count = sum(1 for s in anti_strings if s in data)
            if anti_count >= 2:
                confidence += 10
        
        if confidence >= 50:
            name = 'Themida' if b'Themida' in data else 'WinLicense'
            return {
                'name': name,
                'confidence': min(confidence, 100)
            }
        
    except Exception as e:
        pass
    
    return None
