#!/usr/bin/env python3
import sys
import struct

def build_mmcboot(txt_file, payload_file, out_file):
    nsih_bin = bytearray()
    
    # 1. 解析 NSIH 文本文件
    with open(txt_file, 'r') as f:
        for line in f:
            line = line.strip()
            # 忽略空行和纯注释行
            if not line or line.startswith('//'):
                continue
            
            # 提取第一列的十六进制数值
            hex_str = line.split()[0]
            if len(hex_str) == 8:
                try:
                    # 按照小端序 (Little-Endian) 压入 4 字节
                    nsih_bin.extend(struct.pack('<I', int(hex_str, 16)))
                except ValueError:
                    pass

    # 2. 补齐或截断到严格的 512 字节
    if len(nsih_bin) < 512:
        nsih_bin.extend(b'\x00' * (512 - len(nsih_bin)))
    nsih_bin = nsih_bin[:512]

    # 3. 读取编译出来的裸 BL1 载荷
    with open(payload_file, 'rb') as f:
        bl1_payload = f.read()

    # 4. 拼接生成最终的烧录文件
    with open(out_file, 'wb') as f:
        f.write(nsih_bin)
        f.write(bl1_payload)
    
    print(f"Successfully packed {txt_file} and {payload_file} into {out_file}")

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python3 pack_nsih.py <nsih.txt> <input.bin> <output.bin>")
        sys.exit(1)
    
    build_mmcboot(sys.argv[1], sys.argv[2], sys.argv[3])
