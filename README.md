# Binary Static Analysis Tool

The tool is organized into a modular architecture to separate core analysis logic from specific packer detection signatures:

## Overview

This tool automates the process of gathering technical metadata from a binary file. It helps in identifying security features, potential obfuscation, and structural characteristics without the need to execute the file in a sandbox.

## Key Features

* **Static Triage:** Analyze binaries without execution to ensure safety..
* **Security Auditing:** Identify if a file lacks modern protections like Stack Canaries, NX bits, or ASLR.:
* **Obfuscation Detection:** Use high entropy values and signature matching to find hidden payloads..
* **Multi-Packer Support:** Built-in detection for industry-standard packers like Themida, UPX, and ASPack..


## USAGE
```text
# General usage
python3 binary_analyzer.py <path_to_binary>

# Example: Analyzing a Windows executable
python3 binary_analyzer.py samples/test_file.exe

# Example: Analyzing a Linux ELF file
python3 binary_analyzer.py samples/my_app.out
```

## 📁 Project Structure

The tool relies on a modular architecture located in the `core/` directory:

```text
├── binary_analyzer.py       # Main entry point and orchestrator
├── core/                    # Fundamental analysis modules
│   ├── binary_info.py       # Extracts file metadata and architecture
│   ├── entropy.py           # Calculates Shannon Entropy for data density
│   ├── packer_detector.py   # Main logic for identifying packed files
│   └── security_checks.py   # Audits mitigation flags (ASLR, DEP, etc.)
└── packer/                  # Specialized detection signatures
    ├── aspack.py            # ASPack protection signatures
    ├── pecompact.py         # PECompact signatures
    ├── themida.py           # Themida/WinLicense signatures
    └── upx.py               # UPX compression signatures

```

## ⚙️ Analysis Flow

```text
Binary File
   ↓
Basic Information
   ↓
Security Checks
   ↓
Entropy Analysis
   ↓
Packer Detection
