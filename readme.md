# CLIUniApp – Team Collaboration Guide

> **Project:** University Application (CLI + GUI)  
> **Language:** Python  
> **Submission:** Single `.zip` file per group

---

## Who Does What

| Member | Parts | Area |
|--------|-------|------|
| **Jasmine** | A + B | University menu, Student register/login |
| **Christina** | C | Subject Enrolment System |
| **Lex** | D | Admin System |
| **Raghav** | E + Integration | GUIUniApp + merging everything |

---

## Folder Structure

Everyone must follow this exactly. Do not rename anything.

```
CLIUniApp/
│
├── models/
│   ├── __init__.py
│   ├── student.py
│   ├── subject.py
│   └── database.py
│
├── controllers/
│   ├── __init__.py
│   ├── student_controller.py
│   ├── subject_controller.py
│   └── admin_controller.py
│
├── gui/
│   ├── __init__.py
│   ├── login_window.py
│   ├── enrolment_window.py
│   ├── subject_window.py
│   └── exception_window.py
│
├── students.data
├── main.py
├── gui_main.py
└── README.md
```

---

## Naming Conventions

### Class Names
- `Student` — in `models/student.py`
- `Subject` — in `models/subject.py`
- `Database` — in `models/database.py`
- `StudentController` — in `controllers/student_controller.py`
- `SubjectController` — in `controllers/subject_controller.py`
- `AdminController` — in `controllers/admin_controller.py`

### Variable Names — Student fields
- `student_id` — 6-digit zero-padded string, e.g. `"042731"`
- `name`
- `email`
- `password`
- `subjects` — list of Subject objects

### Variable Names — Subject fields
- `subject_id` — 3-digit zero-padded string, e.g. `"541"`
- `mark` — integer between 25 and 100
- `grade` — string, one of: `"HD"`, `"D"`, `"C"`, `"P"`, `"Z"`

### Grade Boundaries — everyone use these exact same values
- 85–100 → `HD`
- 75–84 → `D`
- 65–74 → `C`
- 50–64 → `P`
- 25–49 → `Z`

### Regex Patterns — define once in `student_controller.py`, import wherever needed
- **Email:** must match `firstname.lastname@university.com`
- **Password:** starts with one uppercase letter, at least 5 letters total, ends with 3 or more digits

---

## Section Responsibilities

### Jasmine — Parts A + B

**Files to own:**
- `models/student.py` — Student class and all its fields
- `models/subject.py` — Subject class and all its fields
- `models/database.py` — read, write, and clear operations on `students.data`
- `controllers/student_controller.py` — university menu, student menu, register, login, regex validation

**Methods to implement in `StudentController`:**
- `university_menu()` — top-level A/S/X menu
- `student_menu()` — L/R/X menu
- `register_student()` — validate format, check for duplicate, save to file
- `login_student()` — validate format, check student exists, return the Student object
- `validate_credentials(email, password)` — returns True/False using regex

**How to test your part alone:**
- Create a temporary `test_jasmine.py` at the project root
- Import `StudentController` and call `university_menu()` directly
- You do not need Christina's or Lex's files to be written yet

---

### Christina — Part C

**File to own:**
- `controllers/subject_controller.py` — full subject enrolment menu

**Depends on:** `Student`, `Subject`, `Database` from Jasmine — ask her for these files early

**Methods to implement in `SubjectController`:**
- `__init__(self, student)` — receives the logged-in Student object
- `enrolment_menu()` — C/E/R/S/X loop
- `enrol_subject()` — create a Subject, add to student.subjects (max 4), save to file
- `remove_subject()` — prompt for subject_id, remove from list, save to file
- `show_subjects()` — print all enrolled subjects with mark and grade
- `change_password()` — prompt new password + confirm, validate with regex, save to file

**How to test your part alone:**
- Create a temporary `test_christina.py` at the project root
- Manually create a `Student` object with fake data, write them to `students.data` using `Database`, then pass that student into `SubjectController` and call `enrolment_menu()`
- You do not need Jasmine's login flow to be finished

---

### Lex — Part D

**File to own:**
- `controllers/admin_controller.py` — full admin menu

**Depends on:** `Student`, `Database` from Jasmine — ask her for these files early

**Methods to implement in `AdminController`:**
- `admin_menu()` — C/G/P/R/S/X loop
- `show_students()` — list all students from file; print `< Nothing to Display >` if empty
- `group_students()` — group students by their grade, print each group
- `partition_students()` — split into PASS (avg mark >= 50) and FAIL (avg mark < 50)
- `remove_student()` — prompt for ID, remove from file, handle not-found case
- `clear_database()` — ask Y/N confirmation first, then clear the file

**How to test your part alone:**
- Create a temporary `test_lex.py` at the project root
- Manually create a few `Student` objects, attach some `Subject` objects to them, write them to `students.data` using `Database`, then call `AdminController().admin_menu()`
- You do not need Jasmine's menus or Christina's enrolment to be finished

---

### Raghav — Part E + Integration

**Files to own:**
- `gui/login_window.py` — email + password fields, login button, reads registered students from `students.data`
- `gui/enrolment_window.py` — enrol button, shows enrolment list, enforces max 4 subjects
- `gui/subject_window.py` — lists enrolled subjects with mark and grade
- `gui/exception_window.py` — handles empty fields, bad format, and attempts to enrol in more than 4 subjects
- `main.py` — CLI entry point, calls `StudentController().university_menu()`
- `gui_main.py` — GUI entry point, launches `LoginWindow`

**Integration responsibilities:**
- Wire `main.py` so a successful student login passes the Student object to `SubjectController`
- Wire `main.py` so the university menu calls both `StudentController` and `AdminController` correctly
- Test the full CLI flow end-to-end before the showcase
- Confirm that `students.data` written by the CLI is readable by the GUI and vice versa

---

## Git Workflow in VSCode

### First time — Jasmine does this, then shares the repo link with everyone
1. Open VSCode and open the project folder
2. Press `Ctrl+Shift+P` → type `Git: Initialize Repository` → select the folder
3. Go to GitHub, create a new **private** repository called `CLIUniApp`
4. Open the VSCode terminal (`Ctrl+`` `) and run these three commands:
   ```
   git remote add origin <your-github-repo-url>
   git branch -M main
   git push -u origin main
   ```
5. On GitHub → Settings → Collaborators → invite Christina, Lex, and Raghav

### Cloning — Christina, Lex, and Raghav do this once
1. Open VSCode
2. Press `Ctrl+Shift+P` → `Git: Clone`
3. Paste the repo URL Jasmine shared → pick a local folder to save it

### Before you start working each day — always do this first
1. Click the **Source Control** icon in the left sidebar (looks like a fork/branch)
2. Click the `...` menu → `Pull`
3. Only start coding after you have pulled

### Everyone works on their own branch — never on main
- Jasmine → `jasmine/parts-ab`
- Christina → `christina/part-c`
- Lex → `lex/part-d`
- Raghav → `raghav/part-e`

To create your branch in VSCode:
1. Click the branch name in the bottom-left corner (it says `main`)
2. Click `+ Create new branch`
3. Type your branch name from the list above and press Enter

### Saving and uploading your work
1. Save your file with `Ctrl+S`
2. Open the Source Control sidebar
3. Hover over your changed files → click the `+` icon to stage them
4. Type a short message describing what you did, e.g. `add register flow`
5. Click the `✓ Commit` button
6. Click `Sync Changes` to push to GitHub

### When your part is done — tell Raghav to merge it
1. Go to GitHub in your browser
2. Click `Pull Requests` → `New Pull Request`
3. Set base to `main`, compare to your branch
4. Click `Create Pull Request` and message Raghav
5. Raghav reviews it and merges

### Rules — everyone follow these
- Never push directly to `main`
- Always pull before you start working
- Commit little and often — do not do one giant commit the night before
- Do not edit files that belong to someone else — message them if you need a change

---

## Shared Agreements — Do Not Change These Without Telling Everyone

- `students.data` is stored as JSON using Python's built-in `json` module
- `Database.read_all()` always returns a list of `Student` objects (empty list if the file is empty, never crashes)
- `Database.write_all(students)` always takes a full list and overwrites the entire file
- `Student.subjects` is always a list of `Subject` objects — never a list of IDs or strings
- `student_id` and `subject_id` are always zero-padded strings, not integers
- Grade boundaries are fixed as listed above — do not change them without a group decision

---

## Submission Checklist

- [ ] CLI runs completely from start to finish without errors
- [ ] `students.data` is created automatically if it does not exist
- [ ] GUI reads from the same `students.data` as the CLI
- [ ] All menus match the sample I/O wording and indentation from the assignment spec
- [ ] Every folder has an `__init__.py` file
- [ ] `README.md` explains how to run both the CLI and GUI
- [ ] Contribution breakdown is written in the README
- [ ] Zipped and named correctly: `group<number>-Cmp1<lab>.zip`
