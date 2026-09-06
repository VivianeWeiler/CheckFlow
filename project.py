import sqlite3
from datetime import date


# ======= MENU / INTERFACE ======= #


def main():

    init_db()

    while True:

        try:
            print_divider()
            print("Welcome to CheckFlow\n")

            choice = int(input("1. Create checklist\n"
                               "2. Access checklists\n"
                               "3. Edit checklist\n"
                               "4. View history\n"
                               "5. Exit\n"
                               "\nChoice: "))
            print_divider()

        except ValueError:
            print("Invalid choice.")
            print_divider()
            continue

        if choice not in [1, 2, 3, 4, 5]:
            print("Invalid choice.")
            print_divider()
            continue

        if choice == 1:
            checklist_form()
        elif choice == 2:
            access_checklist()
        elif choice == 3:
            edit_route()
        elif choice == 4:
            access_history()
        elif choice == 5:
            break


def add_item(wanted_id):
    # Store new items temporarily until the user confirms the changes.
    items = []

    while True:
        item = input("Item (press Enter to finish): ").strip()

        print_divider()

        if item == "":
            while True:
                confirmation = input("Save new items? [y/n]: ")

                if confirmation not in ["y", "n"]:
                    print("Invalid choice.")
                    print_divider()
                    continue

                if confirmation == "y":
                    # Pass the function to update
                    add_database(wanted_id, items)
                    print("Items successfully added.")
                    print_divider()

                    return

                elif confirmation == "n":
                    # back to add more items
                    print("Returning to item addition")
                    print_divider()

                    break

            continue

        # Add the item to the items list
        items.append(item)


# Acesses the menu to see the Checklists
def access_checklist():
    while True:
        try:
            wanted_status = int(input("1. New \n"
                                      "2. In progress \n"
                                      "3. Done \n"
                                      "0. Back to menu\n"
                                      "\nChoice: "))

            print_divider()

        except ValueError:
            print("Invalid choice.")
            print_divider()
            continue

        if wanted_status not in [1, 2, 3, 0]:
            print("Invalid choice.")
            print_divider()
            continue

        # If the choice is new
        if wanted_status == 1:
            status = "new"

        # If the choice is in_progress
        elif wanted_status == 2:
            status = "in_progress"

        # If the choice is done
        elif wanted_status == 3:
            # Completed checklists are handled by the history menu.
            access_history()
            continue

        # return to menu
        elif wanted_status == 0:
            return

        while True:
            checklist_list(status)
            wanted_id = choose_checklist_id()

            if wanted_id is None:
                break

            checklist = get_checklist_by_id(wanted_id)
            if checklist is None:
                print("Checklist not found.")
                continue

            while True:
                selected_item = open_checklist(wanted_id)

                if selected_item is None:
                    break

                run_checklist(selected_item, wanted_id)


def access_history():
    status = "done"

    while True:
        checklist_list(status)
        wanted_id = choose_checklist_id()

        if wanted_id is None:
            break
        else:
            checklist = get_checklist_by_id(wanted_id)
            if checklist is None:
                print("Checklist not found.")
                continue
            else:
                formated_checklist = display_checklist(wanted_id)
                print(formated_checklist)

                try:
                    action_history = int(input("1. Create a copy\n"
                                               "0. Back to the list\n"
                                               "\nChoice: "))
                    print_divider()

                except ValueError:
                    print("Invalid choice.")
                    print_divider()
                    continue

                if action_history not in [1, 0]:
                    print("Invalid choice.")
                    print_divider()
                    continue

                elif action_history == 0:
                    continue

                else:
                    new_id = duplicate_checklist(wanted_id)
                    duplicate_path(new_id)
                    continue


# Create the form to create a new checklist
def checklist_form():
    # Keep items in memory until the user confirms that the checklist should be saved.
    items = []
    message = "Name: "

    while True:
        name = input(message).strip()
        if name != "":
            break
        else:
            message = "Name is required. Try again: "

    description = input("Description: ").strip()
    while True:
        item = input("Item (press Enter to finish): ").strip()


        print_divider()

        if item == "":
            while True:
                # Ask for the confirmation to save
                confirmation_save = input(
                    "Save this checklist?\n\n"
                    "[y] Save\n"
                    "[n] Continue editing\n"
                    "[0] Cancel\n"
                    "\nChoice: ").strip().lower()
                print_divider()

                if confirmation_save not in ["y", "n", "0"]:
                    print("Invalid choice.")
                    print_divider()
                    continue

                if confirmation_save == "y":
                    # Save the checklist and all collected items.
                    save_checklist(name, description, items)
                    print("Checklist created successfully.")


                    print_divider()
                    return

                elif confirmation_save == "n":
                    # back to add more items
                    print("Returning to item addition")

                    print_divider()
                    break

                elif confirmation_save == "0":
                    print("Checklist not saved. Returning to menu.")


                    print_divider()
                    return

            continue
        # Add the item to the items list
        items.append(item)


def checklist_list(status):
    checklists = get_checklists_by_status(status)
    print(f"Checklists {status.capitalize()}\n")

    if checklists == []:
        print("No checklists with this status")
        return
    else:
        for id, name, description, status, conclusion_date in checklists:
            print(f"{id} - {name}, {description} (status: {status.capitalize()})")


def choose_checklist_id():
    while True:
        try:
            wanted_id = int(
                input("\nChecklist ID (0 to go back): "))

            print_divider()

        except ValueError:
            print("Invalid choice.")
            print_divider()
            continue

        if wanted_id == 0:
            return

        return wanted_id


def deletion_procedure(wanted_id):
    while True:
        confirmation = input("Are you sure you want to delete this checklist?\n"
                             "This action cannot be undone. [y/n]: "
                             ).strip().lower()
        print_divider()

        if confirmation not in ["y", "n"]:
            print("Invalid choice.")
            print_divider()
            continue

        if confirmation == "y":
            delete_checklist_data(wanted_id)
            print("Checklist deleted.")
            print_divider()
            return True

        else:
            print("Checklist not deleted.")
            return False


def duplicate_checklist(wanted_id):
    checklist = get_checklist_by_id(wanted_id)
    items = get_items_by_id(wanted_id)

    new_items = []

    id, name, description, status, conclusion_date = checklist
    new_name = f"{name} (copy)"

    for id, content, status, checklist_id in items:
        new_items.append(content)

    new_id = save_checklist(new_name, description, new_items)
    print("Checklist created successfully.")


    print_divider()
    return new_id


def duplicate_path(new_id):
    while True:
        try:
            new_path = int(input("1. Open copied checklist\n"
                                 "0. Back to the list\n"
                                 "\nChoice: "))
            print_divider()

        except ValueError:
            print("Invalid choice.")
            print_divider()
            continue

        if new_path not in [1, 0]:
            print("Invalid choice.")
            print_divider()
            continue

        break

    if new_path == 1:
        while True:
            selected_item = open_checklist(new_id)

            if selected_item is None:
                break

            run_checklist(selected_item, new_id)


def edit_item(selected_item, wanted_id):
    item = get_items_by_id(wanted_id)
    for id, content, status, checklist_id in item:
        if id == selected_item:
            if status == "done":
                print("Cannot edit a 'Done' item.")
                print_divider()
                return

            while True:
                new_content = input(f"Editing item: {content.capitalize()}\n\n"
                                    "New content: ")

                if new_content == "":
                    print("Edit canceled.")
                    print_divider()
                    return

                confirmation = input(
                    "Save this change? [y/n]: ").strip().lower()
                print_divider()

                if confirmation not in ["y", "n"]:
                    print("Invalid choice.")
                    print_divider()
                    continue

                if confirmation == "y":
                    update_item_content(selected_item, new_content)
                    return

                else:
                    print("Change canceled. Returning to edit.")
                    print_divider()
                    continue


def edit_route():
    while True:
        checklist_list("new")
        print()
        checklist_list("in_progress")

        wanted_id = choose_checklist_id()

        if wanted_id is None:
            return

        id, name, description, status, conclusion_date = get_checklist_by_id(wanted_id)
        print(f"{id} - {name}, {description} (status: {status.capitalize()})\n")

        try:
            choice = int(input("1. Edit item\n"
                               "2. Add item\n"
                               "3. Duplicate checklist\n"
                               "4. Delete checklist\n"
                               "0. Back to the list\n"
                               "\nChoice: "))
            print_divider()

        except ValueError:
            print("Invalid choice.")
            print_divider()
            continue

        if choice not in [1, 2, 3, 4, 0]:
            print("Invalid choice.")
            print_divider()
            continue

        if choice == 0:
            continue

        elif choice == 1:
            while True:
                selected_item = open_checklist(wanted_id)

                if selected_item is None:
                    break

                edit_item(selected_item, wanted_id)

        elif choice == 2:
            add_item(wanted_id)
            print_divider()
            continue

        elif choice == 3:
            duplication = input(
                "Are you sure you want to duplicate this checklist? [y/n]: ").strip().lower()
            print_divider()
            if duplication == "y":
                new_id = duplicate_checklist(wanted_id)
                duplicate_path(new_id)
                continue
            else:
                print("Action canceled.")
                print_divider()
                continue

        elif choice == 4:
            deleted = deletion_procedure(wanted_id)
            if deleted:
                continue


def modify_checklist_status(wanted_id):
    if all_items_done(wanted_id):

        while True:
            confirmation = input("Mark this checklist as completed?\n"
                                 "[y] Yes\n"
                                 "[n] No, review and edit\n"
                                 "\nChoice: ").strip().lower()
            print_divider()

            if confirmation in ["y", "n"]:
                break
            print("Invalid choice.")
            print_divider()

        if confirmation == "y":
            conclusion_date = str(date.today())
            update_checklist_status(wanted_id, "done", conclusion_date)
        elif confirmation == "n":
            print("Please, review your checklist")
            return


def open_checklist(wanted_id):
    while True:
        print(display_checklist(wanted_id))

        choice = input("Item number to edit (0 to go back): ").strip()
        print_divider()

        if choice == "0":
            checklist = get_checklist_by_id(wanted_id)
            id, name, description, status, conclusion_date = checklist

            if all_items_done(wanted_id) and status != "done":
                modify_checklist_status(wanted_id)

            return

        elif choice.isdigit():
            selected_item = int(choice)
            real_id = translate_menu(wanted_id, selected_item)

            if real_id is None:
                print("Invalid choice.")
                print_divider()
                continue

            return real_id

        else:
            print("Invalid choice.")
            print_divider()
            continue


# marcar/desmarcar
def run_checklist(selected_item, wanted_id):
    item = get_items_by_id(wanted_id)
    for id, content, status, checklist_id in item:
        if id == selected_item:
            if status == "done":  # Desmarcar
                # Allow the user to undo a completed item.
                while True:
                    confirmation = input("Mark item as not done? [y/n]: ").strip().lower()

                    if confirmation in ["y", "n"]:
                        break
                    print("Invalid choice.")
                    print_divider()

                if confirmation == "y":
                    update_item_status(selected_item, "not_done")
                    print_divider()
                    continue
                elif confirmation == "n":
                    print_divider()
                    return

            elif status == "not_done":  # Marcar
                # Mark the item as completed after user confirmation.
                while True:
                    confirmation = input("Mark item as done? [y/n]: ").strip().lower()

                    if confirmation in ["y", "n"]:
                        break
                    print("Invalid choice.")
                    print_divider()

                if confirmation == "y":
                    update_item_status(selected_item, "done")

                    id, name, description, status, conclusion_date = get_checklist_by_id(wanted_id)
                    if status == "new":
                        update_checklist_status(wanted_id, "in_progress")

                    modify_checklist_status(wanted_id)

                    print_divider()
                    continue
                elif confirmation == "n":
                    print_divider()
                    return


# ======= DATABASE (WRITE) ======= #


# Create the table
def init_db():
    # Create the database connection.
    con = sqlite3.connect("checklist.db")
    cur = con.cursor()

    # Create the tables if they do not already exist.
    cur.executescript('''
        CREATE TABLE IF NOT EXISTS checklists(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        status TEXT NOT NULL,
        conclusion_date TEXT
        );
        CREATE TABLE IF NOT EXISTS items(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL,
        status TEXT,
        checklist_id INTEGER,
        FOREIGN KEY (checklist_id) REFERENCES checklists(id)
        );
    ''')

    # Save changes and close the database connection.
    con.commit()
    con.close()


# Save the basics information in the table
def save_checklist(name, description, items):
    con = sqlite3.connect("checklist.db")
    cur = con.cursor()

    data_checklist = (name, description, "new")

    cur.execute(
        "INSERT INTO checklists(name, description, status) VALUES(?, ?, ?)", data_checklist)

    # Get the ID generated for the new checklist.
    get_id = cur.lastrowid

    for item in items:
        data_items = (item, "not_done", get_id)
        cur.execute(
            "INSERT INTO items(content, status, checklist_id) VALUES(?, ?, ?)", data_items)

    con.commit()
    con.close()

    return get_id


def add_database(wanted_id, items):
    con = sqlite3.connect("checklist.db")
    cur = con.cursor()

    for item in items:
        data_items = (item, "not_done", wanted_id)
        cur.execute(
            "INSERT INTO items(content, status, checklist_id) VALUES(?, ?, ?)", data_items)

    con.commit()
    con.close()


# ======== DATABASE (UPDATE) ======== #


def update_item_content(selected_item, new_content):
    con = sqlite3.connect("checklist.db")
    cur = con.cursor()

    data = (new_content, selected_item)

    cur.execute("UPDATE items SET content = ? WHERE id = ?", data)

    con.commit()
    con.close()


def update_item_status(selected_item, new_status):
    con = sqlite3.connect("checklist.db")
    cur = con.cursor()

    data = (new_status, selected_item)

    cur.execute("UPDATE items SET status = ? WHERE id = ?", data)

    con.commit()
    con.close()


def update_checklist_status(wanted_id, new_status, conclusion_date=None):
    con = sqlite3.connect("checklist.db")
    cur = con.cursor()

    data = (new_status, conclusion_date, wanted_id)

    cur.execute("UPDATE checklists SET status = ?, conclusion_date = ? WHERE id = ?", data)

    con.commit()
    con.close()


# ======== DATABASE (READ) ======== #


def all_items_done(wanted_id):
    items = get_items_by_id(wanted_id)

    for id, content, status, checklist_id in items:
        if status == "not_done":
            return False

    return True


def get_checklists_by_status(status):
    con = sqlite3.connect("checklist.db")
    cur = con.cursor()

    cur.execute("SELECT * FROM checklists WHERE status=?", (status,))

    result = cur.fetchall()
    con.close()

    return result


def get_checklist_by_id(wanted_id):
    con = sqlite3.connect("checklist.db")
    cur = con.cursor()

    cur.execute("SELECT * FROM checklists WHERE id=?", (wanted_id,))
    result = cur.fetchone()
    con.close()

    return result


def get_items_by_id(wanted_id):
    con = sqlite3.connect("checklist.db")
    cur = con.cursor()

    cur.execute("SELECT * FROM items WHERE checklist_id=?", (wanted_id,))
    result = cur.fetchall()
    con.close()

    return result


# ======== DATABASE (DELETE) ======== #


def delete_checklist_data(wanted_id):
    con = sqlite3.connect("checklist.db")
    cur = con.cursor()

    # Delete the checklist's items before deleting the checklist itself.
    cur.execute("DELETE FROM items WHERE checklist_id = ?", (wanted_id,))
    cur.execute("DELETE FROM checklists WHERE id = ?", (wanted_id,))

    con.commit()
    con.close()


# ===== FORMATTING / DISPLAY ===== #


def display_checklist(wanted_id):
    text = ""

    checklist = get_checklist_by_id(wanted_id)
    items = get_items_by_id(wanted_id)

    if checklist is None:
        return ("No checklist with this id")
    else:
        id, name, description, status, conclusion_date = checklist
        text += f"{id} - {name}, {description} (status: {status.capitalize()}) \n"
        if conclusion_date is not None:
            text += f"Completed in {conclusion_date}\n"
        text += "\n"

    for number, (id, content, status, checklist_id) in enumerate(items, start=1):
        if status == "done":
            text += f"{number}. [X] {content}\n"
        elif status == "not_done":
            text += f"{number}. [ ] {content}\n"

    return text


def translate_menu(wanted_id, selected_item):
    items = get_items_by_id(wanted_id)
    for number, (id, content, status, checklist_id) in enumerate(items, start=1):
        if number == selected_item:
            return id

    return


# Print the divider (------------------------------)
def print_divider():
    print("-" * 30)


if __name__ == "__main__":
    main()
