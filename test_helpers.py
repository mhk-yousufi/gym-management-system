from db_helpers import add_member, get_all_members

# Add a new member using our function
new_id = add_member("Sara Malik", "0321-9876543", "2026-07-20", 1)
print(f"Added new member with id: {new_id}")

# Read all members back
members = get_all_members()
print("\nAll members:")
for m in members:
    print(f"ID: {m['id']}, Name: {m['name']}, Phone: {m['phone']}")