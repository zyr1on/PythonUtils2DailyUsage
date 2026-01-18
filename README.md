# Binary Static Analysis Tool

A lightweight, modular Python-based tool designed for security researchers and malware analysts to perform initial static triage on executable files (PE and ELF).

## Overview

This tool automates the process of gathering technical metadata from a binary file. It helps in identifying security features, potential obfuscation, and structural characteristics without the need to execute the file in a sandbox.

## Key Features

* **File Identification:** Detects binary type (Windows EXE/DLL, Linux ELF) and architecture.
* **Security Mitigations Check:** Analyzes the binary for security flags such as:
    * **ASLR** (Address Space Layout Randomization)
    * **DEP/NX** (Data Execution Prevention)
    * **Stack Canaries** (Buffer overflow protection)
* **Entropy Calculation:** Computes the Shannon Entropy value to identify encrypted or compressed data sections (common in malware).
* **Packer Detection:** Uses heuristics and entropy data to detect known packers like UPX or custom obfuscators.

## 📁 Project Structure

The tool relies on a modular architecture located in the `core/` directory:

```text
├── main.py                # Main entry point and orchestration logic
└── core/                  # Analysis engine modules
    ├── binary_info.py     # Module for file headers and metadata
    ├── security_checks.py # Module for security flag verification
    ├── entropy.py         # Module for statistical data analysis
    └── packer_detector.py # Module for packer signature matching
