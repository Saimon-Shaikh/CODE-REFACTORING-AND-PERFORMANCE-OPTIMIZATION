"""
Final Refactored and Optimized User Management System for Task 4.

Key Optimization: Implements an O(1) hash map lookup (self.srno_index) 
for all unique serial number searches, drastically improving performance 
for update and delete operations on large datasets.
"""
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Any

# -----------------------------
# Data Model
# -----------------------------
@dataclass
class User:
    srno: int
    name: str
    age: int
    gender: str
    occupation: str


# -----------------------------
# Database Layer (Optimized)
# -----------------------------
class UserDatabase:
    def __init__(self):
        # Primary storage: list for iteration/display (O(n) display)
        self.entries: List[User] = []
        
        # Performance Optimization: Dictionary for O(1) lookup by srno
        self.srno_index: Dict[int, User] = {} 

    def _get_next_srno(self) -> int:
        return len(self.entries) + 1

    def add_user(self, name: str, age: Any, gender: str, occupation: str) -> None:
        try:
            # Robustness: Ensure age is an integer
            age_int = int(age)
        except ValueError:
            print("Error: Age must be a valid number. Entry aborted.")
            return

        user = User(
            srno=self._get_next_srno(), 
            name=name, 
            age=age_int, 
            gender=gender, 
            occupation=occupation
        )
        
        # Add to both data structures
        self.entries.append(user)
        self.srno_index[user.srno] = user
        

    def find_user(self, key: str, value: str) -> Optional[User]:
        # O(1) Performance Optimization for unique ID search
        if key == 'srno':
            try:
                srno_val = int(value)
                return self.srno_index.get(srno_val)
            except ValueError:
                return None # Invalid srno format

        # Fallback to O(n) linear search for non-indexed fields
        for entry in self.entries:
            # Robustness: Use getattr and case-insensitive comparison
            entry_value = str(getattr(entry, key, '')).lower()
            if entry_value == str(value).lower():
                return entry
        return None

    def update_user(self, key: str, value: str, new_data: dict) -> bool:
        # Find user using optimized method
        user = self.find_user(key, value)
        
        if user:
            for field, val in new_data.items():
                if field == 'age':
                    try:
                        val = int(val)
                    except ValueError:
                        print("Error: Update failed. Age must be a valid number.")
                        return False
                
                # Update the attribute on the User object
                setattr(user, field, val)
                
            # Note: srno and srno_index do not need modification 
            # because the User object reference is preserved.
            return True
        return False

    def delete_user(self, key: str, value: str) -> bool:
        # Find user using optimized method
        user = self.find_user(key, value)
        
        if user:
            # Remove from both structures for consistency (O(1) removal from index)
            self.entries.remove(user) # O(n) removal from list, but less frequent than search
            del self.srno_index[user.srno] # O(1) removal from dictionary
            return True
        return False

    def display_all(self):
        """Displays all users, using the simple list for iteration."""
        if not self.entries:
            print("No users found in database.")
            return
            
        print(f"\n===== Displaying All {len(self.entries)} Users =====")
        for user in self.entries:
            self.display_user(user)
        print("=" * 43)

    @staticmethod
    def display_user(user: User):
        """Displays a single user's details."""
        print("-" * 30)
        # asdict is used for clean, automatic display
        for key, val in asdict(user).items():
            print(f"{key.capitalize()}: {val}")
        print("-" * 30)


# -----------------------------
# User Interface Layer
# -----------------------------
def get_user_input() -> Dict[str, str]:
    """Collects user input as a dictionary of strings."""
    return {
        "name": input("Enter name: ").strip(),
        "age": input("Enter age: ").strip(), # Stays as string for later validation
        "gender": input("Enter gender: ").strip(),
        "occupation": input("Enter occupation: ").strip(),
    }


def get_search_criteria() -> Optional[tuple[str, str]]:
    """Handles user input to select a search field and value."""
    options = ["srno", "name", "age", "gender", "occupation"]
    print("\nSelect a field to search by:")
    for i, opt in enumerate(options, start=1):
        print(f"{i}. {opt.capitalize()}")
    
    try:
        choice = int(input("Enter your choice: "))
        if 1 <= choice <= len(options):
            key = options[choice - 1]
            value = input(f"Enter {key} to search: ").strip()
            return key, value
    except ValueError:
        print("Invalid input.")
    return None


# -----------------------------
# Main Application
# -----------------------------
def main():
    db = UserDatabase()
    print("===== Welcome To User Management System (Optimized) =====")

    while True:
        print("\nWhat would you like to do:")
        print("1. Add an entry")
        print("2. Update an entry")
        print("3. Delete an entry")
        print("4. Search an entry")
        print("5. Display all entries")
        print("6. Exit")

        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("⚠️ Invalid input! Please enter a number.")
            continue
        
        try:
            if choice == 1:
                user_data = get_user_input()
                db.add_user(**user_data)
                print("✅ Entry successfully added.")
                
            elif choice == 2:
                search_tuple = get_search_criteria()
                if search_tuple:
                    key, value = search_tuple
                    print('Enter the updated details:-')
                    new_data = get_user_input()
                    if db.update_user(key, value, new_data):
                        print("✅ Entry successfully updated.")
                    else:
                        print("⚠️ Update failed. Entry not found or invalid data provided.")
                        
            elif choice == 3:
                search_tuple = get_search_criteria()
                if search_tuple:
                    key, value = search_tuple
                    if db.delete_user(key, value):
                        print("✅ Entry successfully deleted.")
                    else:
                        print("⚠️ Deletion failed. Entry not found.")
                        
            elif choice == 4:
                search_tuple = get_search_criteria()
                if search_tuple:
                    key, value = search_tuple
                    user = db.find_user(key, value)
                    if user:
                        db.display_user(user)
                    else:
                        print("⚠️ No entry found matching the criteria.")
                        
            elif choice == 5:
                db.display_all()
                
            elif choice == 6:
                print("👋 Exiting User Management System. Goodbye!")
                break
                
            else:
                print("Invalid option. Please enter a number between 1 and 6.")
                
        except Exception as e:
            # Catching generic errors for robustness in the main loop
            print(f"An unexpected application error occurred: {e}")


if __name__ == "__main__":
    main()
