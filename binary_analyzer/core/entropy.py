#!/usr/bin/env python3

import math
from collections import Counter

class EntropyAnalyzer:
    def __init__(self, filepath):
        self.filepath = filepath
        self.entropy_value = self._calculate_entropy()
        self.assessment = self._assess_entropy()
    
    def _calculate_entropy(self):
        try:
            with open(self.filepath, "rb") as f:
                data = f.read()
            if len(data) == 0:
                return 0.0
            # Byte freqs
            byte_counts = Counter(data)
            
            # Shannon entropy 
            entropy = 0.0
            length = len(data)
            
            for count in byte_counts.values():
                probability = count / length
                if probability > 0:
                    entropy -= probability * math.log2(probability)
            
            return entropy
        except Exception as e:
            return None
    
    def _assess_entropy(self):
        if self.entropy_value is None:
            return "Could not calculate"
        
        if self.entropy_value >= 7.5:
            return "Very High (Possibly packaged/encrypted)"
        elif self.entropy_value >= 7.0:
            return "High (May be packaged or compressed)"
        elif self.entropy_value >= 6.0:
            return "Medium (Normal compiled binary)"
        elif self.entropy_value >= 4.0:
            return "Low (Contains plain text or simple data)"
        else:
            return "Very Low (Mostly Repeated Data)"
    
    def display(self):
        if self.entropy_value is None:
            print(f"Entropy: Could not calculate")
            return
                
        print(f"Entropy: {self.entropy_value:.4f} / 8.000")
        print(f"Assessment: {self.assessment}")
        
        bar_length = 40
        filled = int((self.entropy_value / 8.0) * bar_length)
        bar = "█" * filled + "░" * (bar_length - filled)
        print(f"\nEntropy Graph: [{bar}]")
