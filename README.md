# CheckFlow

#### Video Demo: <https://youtube.com/shorts/Qsuw4z6TFhE?is=WxFn9l1rqKNlzjhV>

### Description:
CheckFlow is a command-line checklist manager written in Python, built as my final project for **CS50’s Introduction to Programming with Python**. It allows users to create, orginize, and track multiple checklists directly from the terminal, with all data persisted in a SQLite database.

The project was developed with the goal of tracking everyday activities, for both individuals and businesses.

The project consists of two main files: `project.py`, which handles all the logic and operations, and `test_project.py`, which contains twelve tests designed to check if the main functions work as expected.

### Features
* Create checklists with a name and optional description
* Add multiple items to a checklist
* View checklists by status:
  * New
  * In progress
  * Done
* Open and interact with checklists
* Mark items as done or not done
* Edit unfinished items
* Add new items to existing checklists
* Duplicate checklists
* Delete checklists with confirmation
* View completed checklists through the History menu
* Reuse completed checklists by creating a fresh copy

## **How it works**

When the program starts, the user is presented with a main menu offering five options:

```text
1. Create checklist
2. Access checklists
3. Edit checklist
4. View history
5. Exit
Choice:
```
The program validates menu input and asks the user to try again when an invalid option is entered.

### 1. Create checklist
The user provides a checklist name and an optional description, then adds as many items as needed.

The checklist is only saved after the user confirms the operation. A name is required, while the description and items are optional.

New checklists are saved with the `new` status.


### 2. Access checklists
Checklists can be filtered by status

CheckFlow uses three checklist statuses:

| Status          | Description                                                              |
| --------------- | ------------------------------------------------------------------------ |
| **New**         | The checklist has been created but no item has been completed yet.       |
| **In progress** | At least one item has been completed, but the checklist is not finished. |
| **Done**        | All items have been completed and the checklist has been finalized.      |

When the first item in a new checklist is marked as done, CheckFlow automatically changes its status to **In progress**.

A checklist can only be completed when all of its items are marked as done. Once this condition is met, the user is asked to confirm the completion. If confirmed, the current date is stored in the database.

New and in-progress checklists can be opened and their items can be marked or unmarked. Completed checklists are accessed through the History menu.

### 3. Edit Checklist

The editing menu allows the user to:
* Edit an item
* Add an item
* Duplicate a checklist
* Delete a checklist

Only unfinished items can be edited. Attempting to edit an item that is already marked as done is rejected by the program.

Destructive operations such as deleting a checklist require confirmation before the data is removed.

### 4. History
Completed checklists are available through the History menu.

The history displays the checklist's completion date and provides an option to create a copy of a completed checklist.

When a checklist is duplicated, its name receives the `(copy)` suffix and its items are recreated as unfinished items in a new checklist. This allows completed checklists to be reused as templates.

### 5. Exit
Closes the program.

## Technologies
* **Python**
* **SQLite**
* **datetime** — used to record checklist completion dates
* **pytest** — used for automated testing

The application does not require external libraries for its core functionality; SQLite is accessed through Python's built-in `sqlite3` module.

## Database

CheckFlow uses two SQLite tables.

### `checklists`

```text
id
name
description
status
conclusion_date
```

### `items`

```text
id
content
status
checklist_id
```

The `checklist_id` field establishes the relationship between an item and its checklist.

## Testing and real-world debugging

Beyond the required automated tests, I asked a family member to use the program without any instructions, simply to see how someone unfamiliar with the code would interact with it  (Thanks sis and love! 😉). This uncovered several real usage bugs that my own testing had missed, for example, selecting a checklist ID that didn't exist used to crash part of the program, and it was possible to exit a fully completed checklist without ever confirming it as done, leaving it permanently stuck as `in_progress`. Fixing these issues based on real interaction, rather than only my own assumptions about how the program would be used, was one of the most valuable parts of building this project.


## Scope

The current version of CheckFlow is intentionally focused on a simple personal checklist management experience.

It does **not** currently include:

* User accounts
* Login or authentication
* Multiple users
* Graphical interface
* Mobile application
* Notifications
* Automatic scheduling
* User permissions
* Audit logs
* Assigned responsibilities

These features may be considered for future versions.

## Future Development

The project could eventually evolve into a more general process-management system.

Possible future features include:

* Categories
* Multiple users
* Assigned responsibilities
* Permissions
* Audit history
* Scheduled checklists
* Notifications
* Business workflows
* Recurring checklists
* Process monitoring
* Automation

The long-term idea is to use the checklist system as a foundation for managing any process composed of sequential or verifiable steps.

## Author

**Viviane**

Developed as the final project for **CS50P — Introduction to Programming with Python**.
