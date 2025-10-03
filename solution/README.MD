Data Engineering Solution: Event Log Processor
Summary of the Solution
This project provides an end-to-end solution for processing raw, time-ordered event logs from a set of JSON files. The script reconstructs the final state of three distinct database tables (accounts, cards, and saving_accounts), merges them into a single, comprehensive denormalized view, and performs a detailed analysis to identify all financial transactions based on changes to account balances and credit usage. The entire process is containerized using Docker to ensure consistent and reliable execution in any environment.

The Thinking Behind the Implemented Solution
The solution is designed in a modular, three-stage process using Python and the pandas library. This approach ensures clarity, maintainability, and correctness.

Stage 1: Table Reconstruction from Event Logs
The core of the solution is a function that reconstructs a table's final state from its event history. The logic is as follows:

Chronological Processing: All JSON files in a directory are read and sorted by filename. This is the most critical step, as the filenames are Unix timestamps, ensuring that events are processed in the exact order they occurred.

Stateful Reconstruction: A Python dictionary acts as an in-memory database. The script iterates through the sorted events:

A create event (op: 'c') adds a new record to the dictionary.

An update event (op: 'u') finds the existing record by its ID and overwrites its data with the new values.

Final DataFrame: After all events are processed, the dictionary holds the final, up-to-date state of every record. This is then converted into a clean pandas DataFrame.

Stage 2: Denormalization (Joining Tables)
Once the three tables are reconstructed, they are merged into a single master view using pandas.merge, which functions like a SQL JOIN.

Join Strategy: A left join is used, starting with the accounts table. This ensures that every account is included in the final output, even if it lacks a corresponding card or savings account.

Join Keys: The merges are performed on the shared keys identified in the data: card_id and savings_account_id.

Stage 3: Transaction Analysis
To identify transactions, the script goes back to the raw event logs. This is more accurate than using the final tables, as it captures every single change.

Transaction Definition: A transaction is defined as any create or update event that sets or changes a balance or credit_used field.

Data Extraction: The function scans the raw JSON files for these specific keys, extracting the timestamp, the value, and the associated ID for each transaction. The final list is then formatted, sorted, and displayed.

How to Run the Solution with Docker
This solution is containerized for easy, one-command execution.

Prerequisites
You must have Docker Desktop installed and running on your system.

Step-by-Step Instructions
Open your terminal (Git Bash is recommended on Windows) and navigate to the root directory of the project (DATA-ENGINEER-TEST).

Build the Docker image. This command reads the Dockerfile and builds the self-contained environment for the script.

docker build -t data-solution .

Run the Docker container. This command will start the container, execute the Solution.py script, and print all the output directly to your terminal.

docker run --rm data-solution

(Alternatively, you can use the provided automation script: ./run.sh)

Desired Result
After running the container, you will see the following output in your terminal:

The reconstructed tables for accounts, cards, and saving_accounts.

The final, denormalized (joined) table showing the complete view.

A summary of the total number of transactions found, followed by a detailed, chronological list of each transaction, including its timestamp, type, ID, and value.