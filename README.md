# SQL Query Chat App

This is a Streamlit-based application that allows users to input natural language questions or SQL queries and get results from a MySQL database. The app leverages a Hugging Face model to translate natural language questions into SQL queries.

## Features

- Input natural language questions or direct SQL queries.
- Translates natural language questions into SQL queries.
- Connects to a MySQL database hosted on Amazon RDS to execute queries.
- Displays the results of the queries.

## Description

This application uses Amazon RDS (Relational Database Service) to host the MySQL database. By using Amazon RDS, the application benefits from a managed database service, which takes care of routine database tasks such as backups, patch management, and scaling, allowing you to focus on the application development.

## Setup and Installation

### Prerequisites

- Python 3.7 or higher
- An active MySQL database on Amazon RDS
- ngrok account for tunneling (optional but recommended for local development)

### Installation

1. **Clone the repository**

    ```bash
    git clone https://github.com/yourusername/sql-query-chat-app.git
    cd sql-query-chat-app
    ```

2. **Create a virtual environment**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables**

    Create a `.env` file in the root directory and add your MySQL and ngrok credentials. Use the `.env.example` file as a template:

    ```env
    MYSQL_HOST=your_mysql_host
    MYSQL_USER=your_mysql_user
    MYSQL_PASSWORD=your_mysql_password
    MYSQL_DATABASE=your_mysql_database
    MYSQL_PORT=3306
    NGROK_AUTH_TOKEN=your_ngrok_auth_token
    ```

    For example, if you are using Amazon RDS, your `.env` file might look like this:

    ```env
    MYSQL_HOST=mysqldatabase.c36siqiasd1q.ap-south-1.rds.amazonaws.com
    MYSQL_USER=admin
    MYSQL_PASSWORD=your_password
    MYSQL_DATABASE=mysqldatabase
    MYSQL_PORT=3306
    NGROK_AUTH_TOKEN=your_ngrok_auth_token
    ```

5. **Run the deployment script**

    ```bash
    python deploy.py
    ```

## File Structure

```plaintext
project-directory/
│
├── .env                # Environment variables (not included in the repository)
├── .env.example        # Template for the .env file
├── .gitignore          # Specifies files to ignore in the repository
├── app.py              # Main Streamlit application
├── deploy.py           # Deployment script
└── requirements.txt    # List of Python dependencies




