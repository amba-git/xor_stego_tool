# LSB XOR Steganography Project

I created a small basic script for hiding text data into image files.
# LSB Steganography Tool (PNG Image Format Only)

A lightweight Python script for hiding and extracting secret messages in PPM (PNG) images using **Least Significant Bit (LSB) steganography**, with **no external dependencies**.

---

# Features

 1. Encode secret messages in raw `.png` image files.
 2. Decode hidden messages from `.png` images.
 3. Uses only Python standard libraries.
 4. Command-line interface with simple flags.
    
---

# Requirements

- Python 3.x
- A `.ppm` image in **P6 binary format** (use GIMP or ImageMagick to convert if needed)
- You can also use https://www.iloveimg.com/jpg-to-image/jpg-to-png to convert
---

# Installation

No installation required. Just clone or download this repository.

```bash
git clone https://github.com/amba-git/xor_stego_tool
cd xor_stego_tool
```

## Encode a Message
```bash
python3 stegno.py -e -i input.png -m "Secret message" -k key -o output.png
```

## Decode a Message
```bash
python3 stego.py -d -i input.png -k key
```
## For options
```bash
python3 stego.py -h 
```
