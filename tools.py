from database import get_connection

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "lookup_employee",
            "description": (
                "Look up an employee's HR record by employee ID. Returns "
                "department, job title, employment type, start date, PTO "
                "balance, and status."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "employee_id": {
                        "type": "string",
                        "description": "The employee ID, e.g. 'E-2003'.",
                    }
                },
                "required": ["employee_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "submit_pto_request",
            "description": (
                "Submit a PTO request for an employee and deduct the days "
                "from their PTO balance."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "employee_id": {"type": "string", "description": "e.g. 'E-2003'"},
                    "start_date": {"type": "string", "description": "YYYY-MM-DD"},
                    "end_date": {"type": "string", "description": "YYYY-MM-DD"},
                    "days_requested": {
                        "type": "number",
                        "description": "Number of PTO days being requested.",
                    },
                    "reason": {
                        "type": "string",
                        "description": "Optional short reason, e.g. 'vacation'.",
                    },
                },
                "required": ["employee_id", "start_date", "end_date", "days_requested"],
            },
        },
    },
]

def lookup_employee(employee_id: str) -> dict:
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM employees WHERE employee_id = ?", (employee_id,)
    ).fetchone()
    if row is None:
        return {"found": False, "error": f"No employee found with ID '{employee_id}'."}
    return {"found": True, **dict(row)}

def submit_pto_request(
    employee_id: str,
    start_date: str,
    end_date: str,
    days_requested: float,
    reason: str = "",
) -> dict:
    # TODO: ask the user to confirm before submitting, this changes their PTO balance
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM employees WHERE employee_id = ?", (employee_id,)
    ).fetchone()

    if row is None:
        return {"success": False, "error": f"No employee found with ID '{employee_id}'."}

    if days_requested > row["pto_balance_days"]:
        return {
            "success": False,
            "error": f"Insufficient PTO balance: employee {employee_id} has "
                     f"{row['pto_balance_days']} day(s) available.",
        }

    new_balance = round(row["pto_balance_days"] - days_requested, 2)
    conn.execute(
        "UPDATE employees SET pto_balance_days = ? WHERE employee_id = ?",
        (new_balance, employee_id),
    )
    conn.commit()

    return {
        "success": True,
        "employee_id": employee_id,
        "new_pto_balance_days": new_balance,
        "message": f"PTO request submitted for {employee_id}: {days_requested} day(s) "
                   f"from {start_date} to {end_date}.",
    }

TOOL_FUNCTIONS = {
    "lookup_employee": lookup_employee,
    "submit_pto_request": submit_pto_request,
}
