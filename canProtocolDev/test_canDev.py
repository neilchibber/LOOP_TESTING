#!/usr/bin/env python3
"""Test script for canDev.py — validates core functions without user input."""

import sys
sys.path.insert(0, '.')

from canDev import get_combined_29bit, print_can_table, _parse_command_entry, _parse_bulk_commands

def test_get_combined_29bit():
    """Test the CAN ID combining function with known values."""
    print("Testing get_combined_29bit()...")
    
    # Test case 1: base=0x160, motor=1, cmd=0x64
    result = get_combined_29bit(0x160, 1, 0x64)
    expected = 0x16164
    assert result == expected, f"Expected 0x{expected:06X}, got 0x{result:06X}"
    print(f"  ✓ Test 1: 0x160 + motor 1 + cmd 0x64 = 0x{result:06X}")
    
    # Test case 2: base=0x160, motor=8, cmd=0x92
    result = get_combined_29bit(0x160, 8, 0x92)
    expected = 0x16892
    assert result == expected, f"Expected 0x{expected:06X}, got 0x{result:06X}"
    print(f"  ✓ Test 2: 0x160 + motor 8 + cmd 0x92 = 0x{result:06X}")
    
    # Test case 3: motor 0 (edge case)
    result = get_combined_29bit(0x160, 0, 0xFF)
    expected = 0x160FF
    assert result == expected, f"Expected 0x{expected:06X}, got 0x{result:06X}"
    print(f"  ✓ Test 3: 0x160 + motor 0 + cmd 0xFF = 0x{result:06X}")
    
    print("✓ All get_combined_29bit tests passed!\n")

def test_parse_command_entry():
    """Test command entry parsing."""
    print("Testing _parse_command_entry()...")
    
    commands = {}
    
    # Test valid hex entry
    result = _parse_command_entry("SetZero 0x64", commands)
    assert result == ("SetZero", 0x64), f"Expected ('SetZero', 0x64), got {result}"
    commands["SetZero"] = 0x64
    print("  ✓ Hex entry parsed: SetZero 0x64")
    
    # Test valid decimal entry
    result = _parse_command_entry("ReadAngle 146", commands)
    assert result == ("ReadAngle", 146), f"Expected ('ReadAngle', 146), got {result}"
    commands["ReadAngle"] = 146
    print("  ✓ Decimal entry parsed: ReadAngle 146")
    
    # Test invalid format (should print error)
    result = _parse_command_entry("InvalidEntry", commands)
    assert result is None, f"Expected None for invalid format, got {result}"
    print("  ✓ Invalid format rejected: InvalidEntry")
    
    # Test duplicate name
    result = _parse_command_entry("SetZero 0x80", commands)
    assert result is None, f"Expected None for duplicate, got {result}"
    print("  ✓ Duplicate name rejected")
    
    print("✓ All _parse_command_entry tests passed!\n")

def test_parse_bulk_commands():
    """Test bulk command parsing."""
    print("Testing _parse_bulk_commands()...")
    
    commands = {}
    
    # Test comma-separated commands
    _parse_bulk_commands("Cmd1 0x64, Cmd2 0x92, Cmd3 0x80", commands)
    assert len(commands) == 3, f"Expected 3 commands, got {len(commands)}"
    assert commands["Cmd1"] == 0x64
    assert commands["Cmd2"] == 0x92
    assert commands["Cmd3"] == 0x80
    print("  ✓ Comma-separated commands parsed: 3 commands added")
    
    # Test single line
    commands_2 = {}
    _parse_bulk_commands("SingleCmd 0xFF", commands_2)
    assert len(commands_2) == 1
    assert commands_2["SingleCmd"] == 0xFF
    print("  ✓ Single command parsed")
    
    print("✓ All _parse_bulk_commands tests passed!\n")

def test_print_can_table():
    """Test the table printing function with both formats."""
    print("Testing print_can_table()...")
    
    base_can_id = 0x160
    commands = {
        "SetZero": 0x64,
        "ReadAngle": 0x92,
        "Shutdown": 0x80
    }
    
    print("\nGenerated CAN ID table (HEX format):")
    print("-" * 70)
    print_can_table(base_can_id, commands, num_motors=4, output_format='hex')
    print("-" * 70)
    print("✓ Hex table printed successfully!")
    
    print("\nGenerated CAN ID table (BINARY format):")
    print("-" * 70)
    print_can_table(base_can_id, commands, num_motors=4, output_format='binary')
    print("-" * 70)
    print("✓ Binary table printed successfully!\n")

if __name__ == "__main__":
    test_get_combined_29bit()
    test_parse_command_entry()
    test_parse_bulk_commands()
    test_print_can_table()
    print("=== All tests passed! ===")

