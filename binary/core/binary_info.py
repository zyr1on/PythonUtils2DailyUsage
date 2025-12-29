#!/usr/bin/env python3

import os
import hashlib
import struct
from pathlib import Path

class BinaryInfo:
    def __init__(self, filepath):
        self.filepath = filepath
        self.filesize = os.path.getsize(filepath)
        self.sha256 = self._calculate_sha256()
        self.binary_type = self._detect_binary_type()
        self.architecture = self._detect_architecture()
        self.stripped = self._is_stripped()
        self.section_count = self._count_sections()
        self.strings_count = self._count_strings()
        
    def _calculate_sha256(self):
        """SHA256 hash hesapla"""
        sha256_hash = hashlib.sha256()
        with open(self.filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    
    def _detect_binary_type(self):
        """Binary tipini tespit et (ELF veya PE)"""
        with open(self.filepath, "rb") as f:
            magic = f.read(4)
            if magic[:4] == b'\x7fELF':
                return "ELF"
            elif magic[:2] == b'MZ':
                return "PE"
            else:
                return "UNKNOWN"
    
    def _detect_architecture(self):
        """Mimari tespit et"""
        try:
            with open(self.filepath, "rb") as f:
                if self.binary_type == "ELF":
                    f.seek(0x12)
                    e_machine = struct.unpack('<H', f.read(2))[0]
                    arch_map = {
                        0x03: "x86",
                        0x3E: "x86-64",
                        0x28: "ARM",
                        0xB7: "AArch64"
                    }
                    return arch_map.get(e_machine, f"Unknown (0x{e_machine:x})")
                
                elif self.binary_type == "PE":
                    f.seek(0x3C)
                    pe_offset = struct.unpack('<I', f.read(4))[0]
                    f.seek(pe_offset + 4)
                    machine = struct.unpack('<H', f.read(2))[0]
                    arch_map = {
                        0x014c: "x86",
                        0x8664: "x86-64",
                        0x01c0: "ARM",
                        0xAA64: "AArch64"
                    }
                    return arch_map.get(machine, f"Unknown (0x{machine:x})")
        except:
            return "Unknown"
        
        return "Unknown"
    
    def _is_stripped(self):
        """Binary stripped mi kontrol et"""
        if self.binary_type == "ELF":
            try:
                import subprocess
                result = subprocess.run(['file', self.filepath], 
                                      capture_output=True, text=True)
                return 'stripped' in result.stdout.lower()
            except:
                return None
        return None
    
    def _count_sections(self):
        """Section sayısını say"""
        try:
            if self.binary_type == "ELF":
                with open(self.filepath, "rb") as f:
                    f.seek(0x30)
                    e_shnum = struct.unpack('<H', f.read(2))[0]
                    return e_shnum
            elif self.binary_type == "PE":
                with open(self.filepath, "rb") as f:
                    f.seek(0x3C)
                    pe_offset = struct.unpack('<I', f.read(4))[0]
                    f.seek(pe_offset + 6)
                    num_sections = struct.unpack('<H', f.read(2))[0]
                    return num_sections
        except:
            return None
        return None
    
    def _count_strings(self):
        """Okunabilir string sayısını say (min 4 karakter)"""
        try:
            count = 0
            with open(self.filepath, "rb") as f:
                data = f.read()
                current_string = []
                for byte in data:
                    if 32 <= byte <= 126:
                        current_string.append(chr(byte))
                    else:
                        if len(current_string) >= 4:
                            count += 1
                        current_string = []
                if len(current_string) >= 4:
                    count += 1
            return count
        except:
            return None
    
    def display(self):
        """Bilgileri ekrana yazdır"""
        print(f"File: {self.filepath}")
        print(f"Type: {self.binary_type}")
        print(f"Size: {self.filesize:,} bytes ({self.filesize / 1024:.2f} KB)")
        print(f"SHA256: {self.sha256}")
        print(f"Arch: {self.architecture}")
        
        if self.stripped is not None:
            status = f"Yes" if self.stripped else f"No"
            print(f"Stripped: {status}")
        
        if self.section_count is not None:
            print(f"Section: {self.section_count}")
        
        if self.strings_count is not None:
            print(f"Strings: {self.strings_count:,}")
