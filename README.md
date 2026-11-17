# HR Support Agent

A simple AI agent I made for a class assignment. It answers questions about
employee PTO balances and can submit a PTO request. It uses the DeepSeek API
and a SQLite database that gets loaded from `data/employees.csv`. All the data
is fake.

## Setup

1. Make a virtual environment and install the requirements:

   ```
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

2. Put your API key in a `.env` file in the project folder:

   ```
   DEEPSEEK_API_KEY=sk-your-key-here
   ```

3. Run it:

   ```
   python agent.py
   ```

## Example questions

- What is E-2003's PTO balance?
- Submit 5 days of PTO for E-2003 from 2026-09-01 to 2026-09-05

Type `exit` to quit.
