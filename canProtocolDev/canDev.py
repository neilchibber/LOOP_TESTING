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
    """Prompt user to enter commands and their byte values."""
    commands = {}
    print("\nEnter commands (name and byte value). Type 'done' when finished.")
    print("Format: CommandName 0xBB (or decimal byte value)")
    
    while True:
        user_input = input("Enter command (or 'done'): ").strip()
        if user_input.lower() == 'done':
            if commands:
                break
            else:
                print("Please add at least one command.")
                continue
        
        parts = user_input.rsplit(maxsplit=1)
        if len(parts) != 2:
            print("Invalid format. Use: CommandName 0xBB")
            continue
        
        command_name, command_byte_str = parts
        try:
            if command_byte_str.lower().startswith('0x'):
                command_byte = int(command_byte_str, 16)
            else:
                command_byte = int(command_byte_str, 10)
            
            if 0 <= command_byte <= 0xFF:
                commands[command_name] = command_byte
                print(f"Added: {command_name} = 0x{command_byte:02X}")
            else:
                print(f"Command byte must be 0x00–0xFF (got 0x{command_byte:02X})")
        except ValueError:
            print("Invalid command byte. Please enter hex (0xBB) or decimal.")
    
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
