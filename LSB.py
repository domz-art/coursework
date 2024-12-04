def message_to_binary(message):
    """Convert a string message to binary format."""
    return ''.join(format(ord(char), '08b') for char in message)

def binary_to_message(binary_data):
    """Convert binary data back to a string."""
    chars = [binary_data[i:i + 8] for i in range(0, len(binary_data), 8)]
    return ''.join(chr(int(char, 2)) for char in chars)

def hide_message(input_image, output_image, secret_message):
    """Hide a message in the BMP image."""
    with open(input_image, 'rb') as img:
        data = bytearray(img.read())

    binary_message = message_to_binary(secret_message) + '1111111111111110'  # Add delimiter
    binary_index = 0

    for i in range(54, len(data)):  # Skip BMP header
        if binary_index < len(binary_message):
            data[i] = (data[i] & 254) | int(binary_message[binary_index])
            binary_index += 1

    with open(output_image, 'wb') as img:
        img.write(data)
    print(f"Message hidden in {output_image}.")

def extract_message(stego_image):
    """Extract a hidden message from the BMP image."""
    with open(stego_image, 'rb') as img:
        data = bytearray(img.read())

    binary_message = ''
    for i in range(54, len(data)):  # Skip BMP header
        binary_message += str(data[i] & 1)

        if binary_message[-16:] == '1111111111111110':
            binary_message = binary_message[:-16]
            break

    return binary_to_message(binary_message)

# Main execution
if __name__ == "__main__":
    print("1: Hide a message in an image")
    print("2: Extract a message from an image")
    choice = input("Enter your choice (1/2): ")

    if choice == '1':
        input_image = input("Enter the input BMP image file name (e.g., input.bmp): ")
        output_image = input("Enter the output BMP image file name (e.g., output.bmp): ")
        secret_message = input("Enter the secret message: ")
        hide_message(input_image, output_image, secret_message)
    elif choice == '2':
        stego_image = input("Enter the stego BMP image file name (e.g., output.bmp): ")
        extracted_message = extract_message(stego_image)
        print(f"Extracted message: {extracted_message}")
    else:
        print("Invalid choice.")
