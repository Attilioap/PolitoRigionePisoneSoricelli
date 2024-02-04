# adjusted_code.py

import hashlib

class User:
    """
    A class representing a user with basic authentication features.
    """

    def __init__(self, username, password):
        """
        Initialize a User instance with a username and password.

        :param username: The username of the user.
        :param password: The password of the user.
        """
        self.username = username
        self.password = self._hash_password(password)

    def _hash_password(self, password):
        """
        Hash the given password using a SHA-256 algorithm.

        :param password: The password to be hashed.
        :return: The hashed password.
        """
        return hashlib.sha256(password.encode()).hexdigest()

    def change_password(self, new_password):
        """
        Change the user's password after checking its complexity.

        :param new_password: The new password to be set.
        :raises ValueError: If the new password is less than 8 characters long.
        """
        if len(new_password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        self.password = self._hash_password(new_password)

    def perform_critical_operation(self):
        """
        Simulate a critical operation.

        :return: The result of the critical operation.
        """
        result = self._complex_operation()
        return result

    def _complex_operation(self):
        """
        Simulate a complex operation.

        :return: The result of the complex operation.
        """
        return 42

def main():
    """
    Simulate the main execution of the program.
    """
    user = User("john_doe", "password123")

    # Simulate a security concern: Printing hashed password
    print(f"Hashed Password: {user.password}")

    try:
        # Simulate a reliability concern: Changing password with a weak one
        user.change_password("weakpass")
    except ValueError as e:
        print(f"Error: {e}")

    # Simulate a maintainability concern: Performing a critical operation
    result = user.perform_critical_operation()
    print(f"Result of Critical Operation: {result}")

if __name__ == "__main__":
    main()
