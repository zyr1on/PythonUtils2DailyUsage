#!/usr/bin/env python3

import sys
import os
from pathlib import Path

# Core modules
from core.binary_info import BinaryInfo
from core.security_checks import SecurityChecker
from core.entropy import EntropyAnalyzer
from core.packer_detector import PackerDetector

def analyze_binary(filepath):
    """Ana analiz fonksiyonu"""
    if not os.path.exists(filepath):
        print(f"[!] Error: File Not Found: {filepath}")
        return
    
    print(f"\n[*] Analyzing: {filepath}\n")

    print(f"Basic Information")
    print(f"{'='*60}")
    
    binary_info = BinaryInfo(filepath)
    binary_info.display()
    
    # 2. Sec checks
    print("")
    print(f"Security Checks")
    print(f"{'='*60}")
    
    security = SecurityChecker(filepath, binary_info.binary_type)
    security.display()
    print("")

    # 3. Entropi     
    print(f"Entropy Analysis")
    print(f"{'='*60}")
    
    entropy = EntropyAnalyzer(filepath)
    entropy.display()
    
    # 4. Packer 
    print("")
    print(f"Packer Detection")
    print(f"{'='*60}")
    
    packer = PackerDetector(filepath, binary_info.binary_type, entropy.entropy_value)
    packer.display()
    
    print(f"\n[✓] Analyze Complated!\n")

def main():    
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <binary_file>")
        print(f"ex:   {sys.argv[0]} a.exe")
        print(f"ex:   {sys.argv[0]} a.out")
        sys.exit(1)
    
    binary_path = sys.argv[1]
    analyze_binary(binary_path)

if __name__ == "__main__":
    main()
