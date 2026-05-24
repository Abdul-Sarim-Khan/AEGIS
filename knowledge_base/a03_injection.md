# A03: Injection

## Summary
Injection occurs when untrusted input is sent to an interpreter (SQL, OS shell, LDAP, NoSQL, template engines) as part of a command or query, allowing an attacker to alter the intended logic.

## Why it matters
Successful injection can read or destroy entire databases, execute operating-system commands, bypass authentication, and lead to full system compromise. SQL injection remains one of the most damaging and common flaws.

## Common vulnerable patterns
- String-concatenated SQL: `cursor.execute("SELECT * FROM users WHERE name = '" + name + "'")`.
- f-string or `%` formatting inside queries: `cursor.execute(f"... WHERE id = {user_id}")`.
- OS command execution with user input: `os.system("ping " + host)`, `subprocess.call(cmd, shell=True)`.
- Dynamic code evaluation: `eval(user_input)`, `exec(user_input)`.
- Server-side template injection passing raw input into a template render.
- NoSQL injection where request data is placed directly into a query document.

## Code indicators to flag
- `execute(` with `+`, `%`, `.format(`, or f-strings containing variables.
- `os.system(`, `subprocess` with `shell=True`.
- `eval(`, `exec(`, `pickle.loads(` on external data.
- `cursor.executescript(` with concatenated input.

## Mitigations
- Use parameterized queries / prepared statements (`cursor.execute("... WHERE id = ?", (user_id,))`).
- Use an ORM correctly and avoid raw query interpolation.
- Never pass user input to a shell; use `subprocess` with an argument list and `shell=False`.
- Never `eval`/`exec` untrusted input; use safe parsers (`ast.literal_eval`, `json.loads`).
- Validate and allowlist input; escape output for the correct context.
