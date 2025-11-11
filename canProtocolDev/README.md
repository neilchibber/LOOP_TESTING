# CAN Identifier Generator

A Python script that generates CAN (Controller Area Network) identifiers by combining a base CAN ID with motor numbers and command bytes.

## Overview

This tool allows you to:
- Input a base CAN identifier (in hex or decimal)
- Define a list of commands with their corresponding byte values
- Generate a table of 29-bit CAN identifiers for all motor IDs (1–8) and commands

## Usage

Run the script:
```bash
python canDev.py
```

### Workflow

1. **Enter Base CAN ID**: Provide the base identifier in hex (e.g., `0x160`) or decimal (e.g., `352`)
2. **Add Commands**: Enter command names and their byte values (hex or decimal)
   - Format: `CommandName 0xBB` (or `CommandName 100` for decimal)
   - Type `done` when finished
3. **Choose Output Format**: Select how to display CAN IDs:
   - **1. Hexadecimal** (0x...) — compact, human-readable hex format
   - **2. Binary** (0b...) — full 29-bit binary representation
4. **View Output**: The script displays a table of all generated CAN IDs in your chosen format

### Example Session

```
=== CAN Identifier Generator ===
Enter base CAN ID (hex with '0x' prefix or decimal): 0x160
Base CAN ID set to: 0x160

Enter commands (name and byte value). Type 'done' when finished.
Format: CommandName 0xBB (or decimal byte value)
Enter command (or 'done'): SetZero 0x64
Added: SetZero = 0x64
Enter command (or 'done'): ReadAngle 0x92
Added: ReadAngle = 0x92
Enter command (or 'done'): Shutdown 0x80
Added: Shutdown = 0x80
Enter command (or 'done'): done

Loaded 3 command(s).

Choose output format:
  1. Hexadecimal (0x...)
  2. Binary (0b...)
Enter choice (1 or 2): 1

Output format: HEX

Command                                            M1        M2        M3        M4        M5        M6        M7        M8
---------------------------------------------------------------------------------------
SetZero                                            0x016164 0x016264 0x016364 0x016464 0x016564 0x016664 0x016764 0x016864
ReadAngle                                          0x016192 0x016292 0x016392 0x016492 0x016592 0x016692 0x016792 0x016892
Shutdown                                           0x016180 0x016280 0x016380 0x016480 0x016580 0x016680 0x016780 0x016880
```

### Binary Output Example

If you choose option 2 (Binary), the output displays full 29-bit binary values:

```
Command                                            M1                          M2                          M3
-------------------------------------------------------------------------------------------------------------------
SetZero                                            0b00000000000010110000101100100 0b00000000000010110001001100100 0b00000000000010110001101100100
ReadAngle                                          0b00000000000010110000110010010 0b00000000000010110001010010010 0b00000000000010110001110010010
Shutdown                                           0b00000000000010110000110000000 0b00000000000010110001010000000 0b00000000000010110001110000000
```

## How It Works

The script combines the CAN components as follows:

```python
combined_can = base_can_id + motor_id
combined_29bit = (combined_can << 8) | command_byte
```

**Bit Layout:**
- **Bits [7:0]** (lower 8 bits): Command byte
- **Bits [8+]** (higher bits): Base CAN ID + Motor ID

### Example
- Base CAN ID: `0x160`
- Motor ID: `1`
- Command byte: `0x64`
- Result: `(0x160 + 1) << 8 | 0x64` = `0x161 << 8 | 0x64` = `0x16164`

## Files

- `canDev.py` — Main script (interactive)
- `test_canDev.py` — Unit tests for core functions

## Running Tests

```bash
python test_canDev.py
```

## Customization

You can modify the number of motors by editing the `num_motors` parameter in the `print_can_table()` function call within `main()`. For example, to use 4 motors instead of 8:

```python
print_can_table(base_can_id, commands, num_motors=4, output_format=output_format)
```

You can also programmatically choose output format:

```python
print_can_table(base_can_id, commands, num_motors=8, output_format='binary')
# or
print_can_table(base_can_id, commands, num_motors=8, output_format='hex')
```

## Input Validation

- **Base CAN ID**: Accepts hex (`0x...`) or decimal values
- **Command bytes**: Must be in range `0x00–0xFF` (0–255)
- **Command names**: Any string (spaces are not supported in names; use single words)
