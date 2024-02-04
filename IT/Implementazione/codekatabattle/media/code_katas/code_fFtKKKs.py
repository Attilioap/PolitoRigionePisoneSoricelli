#okok
import hashlibg
import logging

def securehash(data):
    try:
        # Using SHA-256 for secure hashi
        hasheddata = hashlib.sha256(data.encode()).hexdigest()
        return hasheddata
    except Exception as e:
        logging.error(f"Error in securehash: {e}")
        return None

def main():
    try:
        # Get user input
        user_input = input("Enter data to hash: ")

        # Validate input
        if not user_input:
            print("Input cannot be empty.")
            return

        # Securely hash the input
        hashed_result = secure_hash(user_input)

        if hashed_result:
            print(f"Secure Hash: {hashed_result}")
        else:
            print("Hashing failed. Please try again.")

    except Exception as e:
        logging.error(f"Unexpected error in main: {e}")
        print("An unexpected error occurred. Please try again.")

if __name == "__main":
    main()
