def get_base_can_id():
    """Prompt user for base CAN ID in hex or decimal."""
    while True:
        try:
            user_input = input("Enter base CAN ID (hex with '0x' prefix or decimal): ").strip()
            if user_input.lower().startswith('0x'):
                return int(user_input, 16)
            else:
                return int(user_input, 10)
        except ValueError:
            print("Invalid input. Please enter a valid hex (0x...) or decimal number.")

def get_commands():
    """Prompt user to enter commands and their byte values.
    
    Supports three input modes:
    1. Interactive single-entry mode (one at a time)
    2. Paste mode with multiple lines (one command per line)
    3. Comma-separated entries (all on one line)
    """
    commands = {}
    print("\nEnter commands (name and byte value). Options:")
    print("  • Single entry: CommandName 0xBB (type 'done' when finished)")
    print("  • Bulk paste: Paste multiple lines (one command per line), then type 'done'")
    print("  • Comma-separated: Command1 0x64, Command2 0x92, Command3 0x80")
    
    first_input = input("\nEnter command(s): ").strip()
    
    # Check if user entered comma-separated values (single line with commas)
    if ',' in first_input:
        entries = [e.strip() for e in first_input.split(',')]
        for entry in entries:
            if entry.lower() == 'done':
                continue
            parsed = _parse_command_entry(entry, commands)
            if parsed:
                commands[parsed[0]] = parsed[1]
        return commands if commands else _interactive_command_entry(commands)
    
    # Check if first input is a valid command or if user started bulk mode
    parsed = _parse_command_entry(first_input, commands)
    if parsed:
        commands[parsed[0]] = parsed[1]
        # Continue in interactive mode
        return _interactive_command_entry(commands)
    elif first_input.lower() == 'done':
        if commands:
            return commands
        print("Please add at least one command.")
        return get_commands()
    else:
        # Invalid format, assume bulk paste mode
        print("(Bulk paste mode - enter one command per line, type 'done' when finished)")
        _parse_bulk_commands(first_input, commands)
        return _bulk_command_entry(commands)

def _parse_command_entry(entry, existing_commands):
    """Parse a single command entry and return (name, byte) tuple or None."""
    if not entry or entry.lower() == 'done':
        return None
    
    parts = entry.rsplit(maxsplit=1)
    if len(parts) != 2:
        print(f"Invalid format: '{entry}'. Use: CommandName 0xBB")
        return None
    
    command_name, command_byte_str = parts
    
    # Check for duplicate names
    if command_name in existing_commands:
        print(f"Duplicate command name: '{command_name}' (skipped)")
        return None
    
    try:
        if command_byte_str.lower().startswith('0x'):
            command_byte = int(command_byte_str, 16)
        else:
            command_byte = int(command_byte_str, 10)
        
        if 0 <= command_byte <= 0xFF:
            print(f"Added: {command_name} = 0x{command_byte:02X}")
            return (command_name, command_byte)
        else:
            print(f"Command byte out of range: 0x{command_byte:02X} (must be 0x00–0xFF)")
            return None
    except ValueError:
        print(f"Invalid command byte in '{entry}'. Use hex (0xBB) or decimal.")
        return None

def _interactive_command_entry(commands):
    """Continue in interactive single-entry mode."""
    while True:
        user_input = input("Enter command (or 'done'): ").strip()
        if user_input.lower() == 'done':
            if commands:
                break
            else:
                print("Please add at least one command.")
                continue
        
        parsed = _parse_command_entry(user_input, commands)
        if parsed:
            commands[parsed[0]] = parsed[1]
    
    return commands

def _parse_bulk_commands(line, commands):
    """Parse a single line of bulk input (may be one or comma-separated commands)."""
    # Check if line contains commas (comma-separated format)
    if ',' in line:
        entries = [e.strip() for e in line.split(',')]
    else:
        entries = [line]
    
    for entry in entries:
        if entry.lower() == 'done':
            continue
        parsed = _parse_command_entry(entry, commands)
        if parsed:
            commands[parsed[0]] = parsed[1]

def _bulk_command_entry(commands):
    """Continue in bulk paste mode (multiple lines)."""
    print("(Paste commands, one per line. Type 'done' to finish.)")
    while True:
        user_input = input("").strip()
        if user_input.lower() == 'done':
            if commands:
                break
            else:
                print("Please add at least one command.")
                continue
        
        if user_input:
            _parse_bulk_commands(user_input, commands)
    
    return commands

def get_output_format():
    """Prompt user to choose output format: hex or binary."""
    while True:
        user_choice = input("\nChoose output format:\n  1. Hexadecimal (0x...)\n  2. Binary (0b...)\nEnter choice (1 or 2): ").strip()
        if user_choice == '1':
            return 'hex'
        elif user_choice == '2':
            return 'binary'
        else:
            print("Invalid choice. Please enter 1 or 2.")

def get_combined_29bit(can_base, motor, cmd_byte):
    combined_can = can_base + motor
    combined_29bit = (combined_can << 8) | cmd_byte
    return combined_29bit

def print_can_table(base_can_id, commands, num_motors=8, output_format='hex'):
    """Print a table of CAN IDs for all motors and commands.
    
    Args:
        base_can_id: The base CAN identifier
        commands: Dictionary of {command_name: command_byte}
        num_motors: Number of motors to display (default 8)
        output_format: 'hex' or 'binary' (default 'hex')
    """
    # Column widths
    command_width = 50
    motor_width = 14 if output_format == 'binary' else 10
    
    # Determine formatting function based on output_format
    if output_format == 'binary':
        format_value = lambda val: f"0b{val:029b}"  # 29-bit binary
    else:
        format_value = lambda val: f"0x{val:06X}"   # hex with 6 digits
    
    # Print table header
    header = f"{'Command':<{command_width}}"
    for motor_id in range(1, num_motors + 1):
        header += f" M{motor_id:<{motor_width-2}}"
    print(header)
    print("-" * (command_width + motor_width * num_motors))
    
    # Print each command row
    for name, cmd_byte in commands.items():
        row = f"{name:<{command_width}}"
        for motor_id in range(1, num_motors + 1):
            combined_value = get_combined_29bit(base_can_id, motor_id, cmd_byte)
            formatted_value = format_value(combined_value)
            row += f" {formatted_value:<{motor_width}}"
        print(row)

def main():
    """Main entry point: prompt for inputs and display CAN ID table."""
    print("=== CAN Identifier Generator ===")
    base_can_id = get_base_can_id()
    print(f"Base CAN ID set to: 0x{base_can_id:03X}")
    
    commands = get_commands()
    print(f"\nLoaded {len(commands)} command(s).\n")
    
    output_format = get_output_format()
    print(f"\nOutput format: {output_format.upper()}\n")
    
    print_can_table(base_can_id, commands, output_format=output_format)

if __name__ == "__main__":
    main()
