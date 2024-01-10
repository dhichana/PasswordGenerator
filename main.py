import os
import string
import secrets
import subprocess
import platform
import csv

desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

def generate_password(length=8, complexity='strong'):
    if complexity == 'strong':
        characters = string.ascii_letters + string.digits + string.punctuation
    elif complexity == 'medium':
        characters = string.ascii_letters + string.digits
    elif complexity == 'weak':
        characters = string.ascii_lowercase + string.digits

    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password

def copy_to_clipboard(password):
    system_platform = platform.system().lower()
    if system_platform == 'darwin':
        subprocess.run(['pbcopy'], input=password.encode('utf-8'), check=True)
    elif system_platform == 'linux':
        subprocess.run(['xclip', '-selection', 'clipboard'], input=password.encode('utf-8'), check=True)
    elif system_platform == 'windows':
        subprocess.run(['clip'], input=password.encode('utf-8'), check=True)
    else:
        print("Clipboard functionality is not supported on this platform.")

def save_to_csv(username, password):
    file_path = os.path.join(desktop_path, 'passwords.csv')
    file_exists = os.path.isfile(file_path)
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Username', 'Password'])

        writer.writerow([username, password])

def print_colored(text, color='reset'):
    color_mapping = {
        'reset': '\033[0m',
        'green': '\033[92m',
        'cyan': '\033[96m',
        'yellow': '\033[93m',
    }
    print(f"{color_mapping[color]}{text}{color_mapping['reset']}")

def main():
    print_colored("--------------------", 'green')
    print_colored("| Password Generator |", 'green')
    print_colored("--------------------", 'green')

    while True:
        try:
            length = int(input("Enter the desired length of the password: "))
        except ValueError:
            print_colored("Invalid input. Please enter a valid integer.", 'yellow')
            continue

        if length <= 0:
            print_colored("Password length should be greater than 0.", 'yellow')
            continue

        print()
        complexity = input("Choose the complexity of the password (weak, medium, strong): ").lower()
        if complexity not in ['weak', 'medium', 'strong']:
            print_colored("Invalid complexity. Please choose from 'weak', 'medium', or 'strong.", 'yellow')
            continue

        print()
        password = generate_password(length, complexity)
        print_colored(f"Generated Password: {password}", 'cyan')
        print()

        copy_to_clipboard_option = input("Do you want to copy the password to the clipboard? (yes/no): ").lower()
        if copy_to_clipboard_option == 'yes':
            copy_to_clipboard(password)
            print_colored("Password copied to clipboard.", 'green')
        print()

        save_password_option = input("Do you want to save the password? (yes/no): ").lower()
        if save_password_option == 'yes':
            username = input("Enter the username for the password: ")
            save_to_csv(username, password)
            print_colored("Password saved to CSV file on the desktop.", 'green')
        print()

        generate_another = input("Do you want to generate another password? (yes/no): ").lower()
        if generate_another != 'yes':
            break
        print()

if __name__ == "__main__":
    main()
