# Console Library Management System with PostgreSQL

A simple, console-based application written in Python to manage a library's collection of books, utilizing a **PostgreSQL** database for persistent storage. This system allows users to perform standard library operations like adding, modifying, removing, and displaying book records directly through the command line.

---

## ✨ Features

* **Book Management:** Complete **CRUD** (Create, Read, Update, Delete) functionality for managing book records.
    * **Addition:** Add new books to the library database.
    * **Modification:** Update details (title, author, etc.) of existing books.
    * **Removal:** Delete book records from the database.
* **Database Integration:** Connects to and interacts with a PostgreSQL database using the `psycopg2` library.
* **User Interface:** A clean, menu-driven command-line interface for easy navigation and interaction.
* **Data Display:** Functionality to display the entire library catalog or specific book information.
