#!/usr/bin/env python3
"""Patch WeChat ARM64 binary at file offset 135545057.
Fixes null function pointer crash. Patch bytes derived from
binary diff of working chroot patched binary.
"""
import sys

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else '/opt/wechat/wechat'
    offset = 135545057
    
    # ARM64: mov x0, #1 (20 00 80 D2) ; ret (C0 03 5F D6)
    patch = bytes.fromhex('200080D2C0035FD6')
    
    with open(path, 'r+b') as f:
        f.seek(offset)
        orig = f.read(8)
        print(f"Offset {offset:#x}, original: {orig.hex()}")
        f.seek(offset)
        f.write(patch)
    
    print("Patched successfully")

if __name__ == '__main__':
    main()
