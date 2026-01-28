# SecureBug 🛡️
A Security-Focused Bug Tracking System

## Overview

SecureBug is a backend-oriented bug tracking system built using **Flask** and **SQLite**, designed with a strong focus on **security, authorization, and auditability**.

Rather than emphasizing UI complexity, SecureBug prioritizes **server-side enforcement of rules**, a **controlled bug workflow**, and **comprehensive audit logging** for all critical actions.

This project was developed as a **CS50x Final Project** and reflects a security-first approach to backend system design.

---

## Core Features

### Role-Based Access Control (RBAC)

SecureBug defines three user roles:

- **Reporter** – can create bug reports
- **Developer** – can be assigned bugs and update their progress
- **Admin** – full control, including assigning and closing bugs

All permission checks are enforced strictly on the **backend**.

---

### Bug Lifecycle Enforcement

Each bug follows a controlled workflow:

open → in_progress → fixed → closed

Invalid status transitions are explicitly blocked to preserve workflow integrity.

---

### Bug Assignment Logic

- Bugs can only be assigned to developers
- Closed bugs cannot be reassigned
- Reassignment is allowed before closure
- Self-assignment is permitted to reflect real-world workflows

Assignment and status are treated as **separate concerns**.

---

### Audit Logging

All state-changing actions are recorded in an `audit_logs` table, including:

- Bug creation
- Bug assignment and reassignment
- Bug status changes

Audit logs capture **old → new values**, ensuring full traceability and accountability.

---

### Security-Oriented Design Decisions

- No trust in frontend-provided role or identity data
- All authorization logic enforced server-side
- Explicit separation of responsibility (assignment) and progress (status)
- Correct handling of SQL `NULL` values as Python `None`
- Read-before-write logic to preserve accurate audit history

---

## Technology Stack

- **Backend:** Python, Flask
- **Database:** SQLite
- **Frontend:** HTML, CSS (minimal, interaction-only)

The project intentionally avoids frontend frameworks to maintain focus on backend logic and security.
