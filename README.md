# 📚 Library Manager

## Table of Contents
- [📄 Project Description](#-project-description)
- [🎯 Motivation](#-motivation)
- [🚀 Features](#-features)
- [📅 Project Management](#-project-management)
- [📖 Documentation](#-documentation)
- [🛠 Technologies Used](#-technologies-used)
- [📦 Installation and Configuration](#-installation-and-configuration)
- [🧪 Testing](#-testing)
- [🤝 Contributions](#-contributions)
- [📧 Contact](#-contact)



## 📄 Project Description

**Library Manager** is a library management system that allows you to manage book inventories, handle loans, and manage users. This project was developed as part of an educational exercise to reinforce concepts of Python, PostgreSQL, and testing techniques, using agile methodologies.
**Please note:** This project is still under development, and some features and improvements are yet to be implemented. Contributions and suggestions are welcome as we continue to enhance the system.


## 🎯 Motivation

This project was developed as part of a bootcamp to practice backend development with Python and PostgreSQL. The goal is to provide a hands-on experience in building a comprehensive tool for managing library operations, including book inventories, user registration, and loan processes. By working on this project, participants gain practical skills in Python, database management, and testing, while applying best practices in software development.


## 🚀 Features

### Inventory Management (CRUD Operations)
- **Create**: Register new books in the system.
- **Read**: Search and consult books by different criteria (title, author, category, etc.).
- **Update**: Update information on existing books.
- **Delete**: Remove books from the inventory.
- **Validation**: Ensure no duplicates in the inventory using appropriate validations.

### Category Management (CRUD Operations)
- **Create**: Add new categories and tags for classifying books.
- **Read**: View existing categories and their associated tags.
- **Update**: Modify existing categories and their details.
- **Delete**: Remove categories and tags from the system.

### Book Loans (CRUD Operations)
- **Create**: Register loans of books to users.
- **Read**: View and track loan statuses and return dates.
- **Update**: Update loan information upon return of books.
- **Delete**: Manage loan records as needed.
- **Notifications**: Notify users about return dates and delays.

### User Management (CRUD Operations)
- **Create**: Register new users in the library system.
- **Read**: Search and consult users by different criteria (name, membership number, etc.).
- **Update**: Update user information.
- **Delete**: Remove users from the system.
- **Validation**: Ensure no duplicate users using appropriate validations.


## 📅 Project Management
This project was developed by a team of 6 developers using SCRUM. Tools like Jira were used for backlog management and sprint planning.


## 📖 Documentation
- **[Algorithm Flowchart](https://miro.com/app/board/uXjVKwLsYHQ=)**: A flowchart illustrating the main algorithms implemented in the project, available on Miro.
- **[Data Model](https://drawsql.app/teams/equipo3-f5/diagrams/biblioteca-equipo-3)**: A diagram showing the key entities of the system and their relationships, available on DrawSQL.
- **Project Management (Jira)**: 
    - **[Jira Board](https://librarymanager.atlassian.net/jira/software/projects/LM/boards/1)**: Access to the Jira board where user stories and tasks are managed. **Note**: This link is private and only accessible to authorized project members. Contact the administrator [Jessica](#jessica).

## 🛠 Technologies Used

- **Language**: Python (v3.12.4)
- **Database**: PostgreSQL (v16.2)
- **Testing**: Pytest (v8.3.2), Unittest (integrated with Python)
- **Version Control**: Git (v2.45.2) with GitFlow
- **Agile Methodologies**: SCRUM


## 📦 Installation and Configuration

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/evymari/library_manager.git]
   cd library_manager
   ```
2. **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate o venv\Scripts\activate
    ```
3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4. **Configure the database:**

    Create a database in PostgreSQL.

    Configure the .env file with the database credentials.


## 🧪 Testing

- **Run unit and integration tests:**

    ```bash
    pytest
    ```

### Types of Tests Performed
- **Unit Tests**: Verify the functionality of individual components, ensuring that each function and method works as intended.
- **Integration Tests**: Ensure that different modules and components work together seamlessly.

### Code Coverage
- The test suite has achieved a **code coverage of over 80%**, meeting the project requirements.
- This level of coverage ensures that the majority of the codebase is well-tested, reducing the risk of bugs and ensuring the reliability of core functionalities.
- To check the code coverage yourself, follow these steps:
  - Install the coverage package if you haven't already:
    ```bash
    pip install coverage
    ```
  - Run the tests with coverage:
    ```bash
    coverage run -m pytest
    ```
  - Generate a coverage report:
    ```bash
    coverage report
    ```
- The coverage report will provide detailed insights into which parts of the codebase are covered by tests and which parts might need additional testing.


## 🤝 Contributions

Contributions are welcome. Please open an issue or submit a pull request for any improvements.


## 📧 Contact

For any inquiries, you can reach out to us through our GitHub and LinkedIn profiles:

-  [![GitHub Octocat](https://img.icons8.com/ios-glyphs/30/000000/github.png)](https://github.com/ItalianCookieMonster)  [![LinkedIn](https://img.icons8.com/ios-glyphs/30/0077b5/linkedin.png)](https://www.linkedin.com/in/valentinatoni/) Valentina 
- [![GitHub Octocat](https://img.icons8.com/ios-glyphs/30/000000/github.png)](https://github.com/limonadaweb)  [![LinkedIn](https://img.icons8.com/ios-glyphs/30/0077b5/linkedin.png)](https://www.linkedin.com/in/adriana) Adriana  
- [![GitHub Octocat](https://img.icons8.com/ios-glyphs/30/000000/github.png)](https://github.com/Dpoetess)  [![LinkedIn](https://img.icons8.com/ios-glyphs/30/0077b5/linkedin.png)](https://https://www.linkedin.com/in/lynn-poh/)  Lynn 
- [![GitHub Octocat](https://img.icons8.com/ios-glyphs/30/000000/github.png)](https://github.com/tursdlc)  [![LinkedIn](https://img.icons8.com/ios-glyphs/30/0077b5/linkedin.png)](https://www.linkedin.com/in/ana) Ana  
- [![GitHub Octocat](https://img.icons8.com/ios-glyphs/30/000000/github.png)](https://github.com/evymari)  [![LinkedIn](https://img.icons8.com/ios-glyphs/30/0077b5/linkedin.png)](https://www.linkedin.com/in/evelyn)  Evelyn (Product Owner)  
- <a id="jessica"></a>[![GitHub Octocat](https://img.icons8.com/ios-glyphs/30/000000/github.png)](https://github.com/jess-ar)  [![LinkedIn](https://img.icons8.com/ios-glyphs/30/0077b5/linkedin.png)](https://www.linkedin.com/in/jessica-arroyo-lebron/) Jessica (Scrum Master)


## 😊 If you've made it this far, feel free to follow us on GitHub or LinkedIn. We'd love to be in touch!



