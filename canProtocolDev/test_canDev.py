#!/usr/bin/env python3
"""Test script for canDev.py — validates core functions without user input."""

import sys
sys.path.insert(0, '.')

from canDev import get_combined_29bit, print_can_table

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
    test_print_can_table()
    print("=== All tests passed! ===")
