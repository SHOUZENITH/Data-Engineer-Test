# Data Engineering Solution: Event Log Processor

## Summary of the Solution
This project provides an **end-to-end solution** for processing raw, time-ordered event logs from a set of JSON files. The script:

1. Reconstructs the final state of three distinct database tables (**accounts, cards, saving_accounts**).  
2. Merges them into a single, comprehensive **denormalized view**.  
3. Performs a detailed **transaction analysis** by identifying all financial transactions based on changes to account balances and credit usage.  

The entire process is **containerized using Docker** to ensure consistent and reliable execution in any environment.

---

## The Thinking Behind the Implemented Solution

The solution is designed in a modular, **three-stage process** using Python and the `pandas` library. This ensures clarity, maintainability, and correctness.

### Stage 1: Table Reconstruction from Event Logs
- **Chronological Processing**:  
  All JSON files in a directory are read and sorted by filename. Since filenames are Unix timestamps, events are processed in exact chronological order.  

- **Stateful Reconstruction**:  
  A Python dictionary acts as an in-memory database:  
  - A **create event** (`op: 'c'`) adds a new record.  
  - An **update event** (`op: 'u'`) updates the existing record by ID.  

- **Final DataFrame**:  
  Once all events are processed, the dictionary holds the latest state of each record. This is then converted into a clean `pandas.DataFrame`.

---

### Stage 2: Denormalization (Joining Tables)
- **Merge Strategy**:  
  The three reconstructed tables are merged into a single master view using `pandas.merge`.  

- **Join Logic**:  
  - A **left join** is performed, starting with the `accounts` table.  
  - This guarantees all accounts appear in the final output, even if they lack a `card` or `saving_account`.  
  - Joins are performed using **shared keys** (`card_id`, `savings_account_id`).  

---

### Stage 3: Transaction Analysis
- **Direct Log Analysis**:  
  Transactions are identified directly from raw event logs (not the final tables) to capture **every change**.  

- **Transaction Definition**:  
  A transaction = any create/update event that changes a `balance` or `credit_used` field.  

- **Extraction Process**:  
  - The script scans JSON logs for relevant keys.  
  - Extracts: **timestamp, value, event type, ID**.  
  - Results are formatted, sorted chronologically, and displayed.  

---

## Running the Solution with Docker

### Prerequisites
- Install [Docker Desktop](https://www.docker.com/products/docker-desktop) and ensure it is running.

### Steps
1. Open your terminal and navigate to the project root (`DATA-ENGINEER-TEST`).  

2. **Build the Docker image**:  
   ```bash
   docker build -t data-solution .
