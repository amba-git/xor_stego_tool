import argparse
from PIL import Image
EOF_MARKER = b'\x00\xff'

def to_binary(data: bytes):
    return ''.join(f'{b:08b}' for b in data)

def from_binary(binary):
    return bytes(int(binary[i:i+8], 2) for i in range(0, len(binary), 8))

def xor_encrypt_decrypt(data: bytes, key: bytes):
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))

def encode(image_path, message, key, output_path=None):
    key_bytes = key.encode()
    encrypted = xor_encrypt_decrypt(message.encode(), key_bytes) + EOF_MARKER
    data_bin = to_binary(encrypted)

    img = Image.open(image_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')

    pixels = list(img.getdata())
    new_pixels = []
    data_index = 0

    for pixel in pixels:
        r, g, b = pixel
        if data_index < len(data_bin):
            r = (r & ~1) | int(data_bin[data_index])
            data_index += 1
        if data_index < len(data_bin):
            g = (g & ~1) | int(data_bin[data_index])
            data_index += 1
        if data_index < len(data_bin):
            b = (b & ~1) | int(data_bin[data_index])
            data_index += 1
        new_pixels.append((r, g, b))
        if data_index >= len(data_bin):
            break

    new_pixels += pixels[len(new_pixels):]
    encoded_img = Image.new(img.mode, img.size)
    encoded_img.putdata(new_pixels)
    if not output_path:
        output_path = "encoded_"+image_path
    encoded_img.save(output_path)
    print(f"[+] Message encoded and saved to {output_path}")

def decode(image_path, key):
    img = Image.open(image_path)
    pixels = list(img.getdata())
    binary = ''

    for pixel in pixels:
        for color in pixel[:3]:
            binary += str(color & 1)

    byte_data = from_binary(binary)

    end = byte_data.find(EOF_MARKER)
    if end == -1:
        print("[-] EOF marker not found. Possibly corrupted or wrong image.")
        return

    encrypted = byte_data[:end]
    key_bytes = key.encode()
    decrypted = xor_encrypt_decrypt(encrypted, key_bytes)

    try:
        message = decrypted.decode('utf-8')
        print(f"[+] Hidden message: {message}")
    except UnicodeDecodeError as e:
        print(f"[-] Failed to decrypt. Reason: {e}")

def main():
    parser = argparse.ArgumentParser(description="LSB Steganography with XOR encryption")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-e', '--encode', action='store_true', help='Encode a message')
    group.add_argument('-d', '--decode', action='store_true', help='Decode a message')
    parser.add_argument('-i', '--image', required=True, help='Image file path')
    parser.add_argument('-m', '--message', help='Secret message to hide')
    parser.add_argument('-k', '--key', required=True, help='Encryption key')
    parser.add_argument('-o', '--output', help='Outputing image path')

    args = parser.parse_args()

    if args.encode:
        if not args.message:
            print("[-] Please provide a message using -m")
            return
        encode(args.image, args.message, args.key, args.output)
    elif args.decode:
        decode(args.image, args.key)

if __name__ == '__main__':
    main()