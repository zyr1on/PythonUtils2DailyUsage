#!/usr/bin/env python3

import struct
import subprocess

class SecurityChecker:
    def __init__(self, filepath, binary_type):
        self.filepath = filepath
        self.binary_type = binary_type
        self.checks = {}
        
        if binary_type == "ELF":
            self._check_elf_security()
        elif binary_type == "PE":
            self._check_pe_security()
    
    def _check_elf_security(self):
        # NX (No-Execute)
        self.checks['NX'] = self._check_elf_nx()
        
        # PIE (Position Independent Executable)
        self.checks['PIE'] = self._check_elf_pie()
        
        # RELRO (Relocation Read-Only)
        self.checks['RELRO'] = self._check_elf_relro()
        
        # Stack Canary
        self.checks['CANARY'] = self._check_elf_canary()
        
        # Interpreter
        self.checks['INTERPRETER'] = self._get_elf_interpreter()
    
    def _check_elf_nx(self):
        """ELF NX flag kontrolü"""
        try:
            with open(self.filepath, "rb") as f:
                
                f.seek(0)
                e_ident = f.read(16)
                ei_class = e_ident[4]  # 1=32bit, 2=64bit
                
                if ei_class == 2:  # 64-bit
                    f.seek(0x20)
                    e_phoff = struct.unpack('<Q', f.read(8))[0]
                    f.seek(0x38)
                    e_phnum = struct.unpack('<H', f.read(2))[0]
                    ph_size = 56
                else:  # 32-bit
                    f.seek(0x1C)
                    e_phoff = struct.unpack('<I', f.read(4))[0]
                    f.seek(0x2C)
                    e_phnum = struct.unpack('<H', f.read(2))[0]
                    ph_size = 32
                
                
                for i in range(e_phnum):
                    offset = e_phoff + (i * ph_size)
                    f.seek(offset)
                    p_type = struct.unpack('<I', f.read(4))[0]
                    
                    if p_type == 0x6474e551:  # PT_GNU_STACK
                        f.seek(offset + (4 if ei_class == 1 else 8))
                        p_flags = struct.unpack('<I', f.read(4))[0]
                        # PF_X (execute) = 0x1
                        return not (p_flags & 0x1)
                
                return False
        except:
            return None
    
    def _check_elf_pie(self):
        
        try:
            with open(self.filepath, "rb") as f:
                f.seek(0x10)
                e_type = struct.unpack('<H', f.read(2))[0]
                # ET_DYN (3) = PIE or shared library
                return e_type == 3
        except:
            return None
    
    def _check_elf_relro(self):
       
        try:
            result = subprocess.run(['readelf', '-l', self.filepath],
                                  capture_output=True, text=True)
            output = result.stdout
            
            if 'GNU_RELRO' in output:
                
                result2 = subprocess.run(['readelf', '-d', self.filepath],
                                       capture_output=True, text=True)
                if 'BIND_NOW' in result2.stdout:
                    return "Full"
                return "Partial"
            return "No"
        except:
            return None
    
    def _check_elf_canary(self):
        try:
            result = subprocess.run(['readelf', '-s', self.filepath],
                                  capture_output=True, text=True)
            return '__stack_chk_fail' in result.stdout
        except:
            return None
    
    def _get_elf_interpreter(self):
        """ELF interpreter bilgisi"""
        try:
            result = subprocess.run(['readelf', '-l', self.filepath],
                                  capture_output=True, text=True)
            for line in result.stdout.split('\n'):
                if 'interpreter' in line.lower():
                    parts = line.split('[')
                    if len(parts) > 1:
                        return parts[1].split(']')[0]
            return None
        except:
            return None
    
    def _check_pe_security(self):
        # ASLR (Address Space Layout Randomization)
        self.checks['ASLR'] = self._check_pe_aslr()
        
        # DEP/NX (Data Execution Prevention)
        self.checks['DEP'] = self._check_pe_dep()
        
        # CFG (Control Flow Guard)
        self.checks['CFG'] = self._check_pe_cfg()
        
        # SafeSEH
        self.checks['SafeSEH'] = self._check_pe_safeseh()
    
    def _check_pe_aslr(self):
        try:
            with open(self.filepath, "rb") as f:
                f.seek(0x3C)
                pe_offset = struct.unpack('<I', f.read(4))[0]
                f.seek(pe_offset + 0x16)
                characteristics = struct.unpack('<H', f.read(2))[0]
                
                # DllCharacteristics offset
                f.seek(pe_offset + 0x5E)
                dll_chars = struct.unpack('<H', f.read(2))[0]
                
                # IMAGE_DLLCHARACTERISTICS_DYNAMIC_BASE = 0x0040
                return bool(dll_chars & 0x0040)
        except:
            return None
    
    def _check_pe_dep(self):
        
        try:
            with open(self.filepath, "rb") as f:
                f.seek(0x3C)
                pe_offset = struct.unpack('<I', f.read(4))[0]
                f.seek(pe_offset + 0x5E)
                dll_chars = struct.unpack('<H', f.read(2))[0]
                
                # IMAGE_DLLCHARACTERISTICS_NX_COMPAT = 0x0100
                return bool(dll_chars & 0x0100)
        except:
            return None
    
    def _check_pe_cfg(self):
        
        try:
            with open(self.filepath, "rb") as f:
                f.seek(0x3C)
                pe_offset = struct.unpack('<I', f.read(4))[0]
                f.seek(pe_offset + 0x5E)
                dll_chars = struct.unpack('<H', f.read(2))[0]
                
                # IMAGE_DLLCHARACTERISTICS_GUARD_CF = 0x4000
                return bool(dll_chars & 0x4000)
        except:
            return None
    
    def _check_pe_safeseh(self):
        
        try:
            
            with open(self.filepath, "rb") as f:
                f.seek(0x3C)
                pe_offset = struct.unpack('<I', f.read(4))[0]
                f.seek(pe_offset + 4)
                machine = struct.unpack('<H', f.read(2))[0]
                
                if machine != 0x014c:  
                    return "N/A"
                
                f.seek(pe_offset + 0xD8)
                load_config_rva = struct.unpack('<I', f.read(4))[0]
                
                return load_config_rva != 0
        except:
            return None
    
    def display(self):
        
        if self.binary_type == "ELF":
            self._display_elf()
        elif self.binary_type == "PE":
            self._display_pe()
    
    def _display_elf(self):
        
        nx = self.checks.get('NX')
        pie = self.checks.get('PIE')
        relro = self.checks.get('RELRO')
        canary = self.checks.get('CANARY')
        interpreter = self.checks.get('INTERPRETER')
        
        print(f"NX: {self._format_bool(nx)}")
        print(f"PIE: {self._format_bool(pie)}")
        print(f"RELRO: {self._format_relro(relro)}")
        print(f"CANARY: {self._format_bool(canary)}")
        if interpreter:
            print(f"Interpreter: {interpreter}")
    
    def _display_pe(self):
       
        aslr = self.checks.get('ASLR')
        dep = self.checks.get('DEP')
        cfg = self.checks.get('CFG')
        safeseh = self.checks.get('SafeSEH')
        
        print(f"ASLR: {self._format_bool(aslr)}")
        print(f"DEP (NX): {self._format_bool(dep)}")
        print(f"CFG: {self._format_bool(cfg)}")
        print(f"SafeSEH: {self._format_safeseh(safeseh)}")
    
    def _format_bool(self, value):
        """Boolean değeri formatla"""
        if value is None:
            return f" Unknown"
        elif value:
            return f" Enabled"
        else:
            return f" Disabled"
    
    def _format_relro(self, value):
        """RELRO değerini formatla"""
        if value is None:
            return f" Unknown"
        elif value == " Full":
            return f" Full RELRO"
        elif value == " Partial":
            return f" Partial RELRO"
        else:
            return f" No RELRO"
    
    def _format_safeseh(self, value):
        """SafeSEH değerini formatla"""
        if value == " N/A":
            return f" N/A (64-bit)"
        return self._format_bool(value)
