def run_sql(sql: str) -> dict | str:
    """Escape hatch for anything the 8 tools can't answer.

    Input: one read-only SELECT written by the model.
    Everything below is CODE, not prompt — it must hold even if
    the model ignores its instructions:

    1. Validate   → single statement, starts with SELECT;
                    reject ;, INSERT/UPDATE/DELETE/DROP/ALTER/...
    2. Scope      → (hook now, activate if multi-user later):
                    force WHERE user_id = current_user
    3. Enforce    → append LIMIT 50 if missing; 5s statement timeout
    4. Execute    → READ-ONLY Postgres role (no write grants at all)
    5. Shape      → {"columns": [...], "rows": [...], "row_count": n}
    6. On error   → return the DB error STRING back to the model
                    so it can fix and retry (self-correction loop)
    """
