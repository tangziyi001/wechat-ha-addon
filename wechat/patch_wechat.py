#!/usr/bin/env python3
"""Patch WeChat ARM64 binary: fix null function pointer at VA 0x81440dc.
Changes the indirect branch (br x0 with null x0) to mov x0,#1; ret.
"""
import struct
import sys

def va_to_file_offset(elf_path, va):
    with open(elf_path, 'rb') as f:
        # ELF header
        f.seek(0x20)
        phoff = struct.unpack('<Q', f.read(8))[0]
        f.seek(0x36)
        phentsize = struct.unpack('<H', f.read(2))[0]
        f.seek(0x38)
        phnum = struct.unpack('<H', f.read(2))[0]
        
        for i in range(phnum):
            f.seek(phoff + i * phentsize)
            p_type, p_flags = struct.unpack('<II', f.read(8))
            p_offset, p_vaddr = struct.unpack('<QQ', f.read(16))
            p_filesz = struct.unpack('<Q', f.read(8))[0]
            if p_type == 1:  # PT_LOAD
                if p_vaddr <= va < p_vaddr + p_filesz:
                    return p_offset + (va - p_vaddr)
    return None

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else '/opt/wechat/wechat'
    va = 0x81440dc
    
    offset = va_to_file_offset(path, va)
    if offset is None:
        print(f"VA {va:#x} not found in PT_LOAD segments", file=sys.stderr)
        sys.exit(1)
    
    print(f"VA {va:#x} -> file offset {offset:#x}")
    
    # ARM64: mov x0, #1 (D2800020) ; ret (D65F03C0)
    patch = bytes.fromhex('200080D2C0035FD6')
    
    with open(path, 'r+b') as f:
        f.seek(offset)
        orig = f.read(8)
        print(f"Original bytes: {orig.hex()}")
        f.seek(offset)
        f.write(patch)
    
    print("Patched successfully")

if __name__ == '__main__':
    main()
