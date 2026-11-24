# Lab 5: Issues Table - pharmacy_manager.py

**Name:** Jayant Mahishi | **SRN:** PES1UG24AM122 | **GitHub:** Jayant-2006

## Summary of results

| Tool | Before | After |
|------|--------|-------|
| Pylint | 4.83 / 10 | 10.00 / 10 |
| Bandit | 8 issues (2 High, 2 Medium, 4 Low) | 0 issues |
| Flake8 | 22 warnings | 0 warnings |

## Issues found and fixed

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Command injection via `os.system` (Bandit B605, High) | Security | 68 | `os.system("echo ..." + name)` builds a shell command from the medicine name, so a crafted name can run arbitrary commands | Removed the shell call; the label is printed with `print()` |
| Weak MD5 hash for patient ID (Bandit B324, High) | Security | 51 | MD5 is broken and unsuitable for identifying or protecting patient data | Replaced with `hashlib.sha256` |
| Use of `eval()` on doctor's note (Bandit B307, Pylint W0123, Medium) | Security | 48 | `eval(formula)` executes any Python expression, giving arbitrary code execution | Replaced with an AST-based evaluator allowing only numbers and `+ - * /` |
| Unsafe `pickle.load` (Bandit B301/B403, Medium) | Security | 3, 64 | Unpickling a tampered `pharmacy.dat` can run arbitrary code | Stock is saved and loaded as JSON (`pharmacy.json`) |
| Hardcoded password (Bandit B105, Low) | Security | 11 | `DB_PASSWORD = "pharma@123"` is stored in source code and version control | Read from the `PHARMACIST_PASSWORD` environment variable; compared with `secrets.compare_digest` |
| Insecure random for Rx numbers (Bandit B311, Low) | Security | 54 | `random.randint` is predictable, so prescription numbers can be guessed | Replaced with `secrets.randbelow` |
| Mutable default argument `audit=[]` (Pylint W0102) | Bug | 13 | The same list is shared across all calls, so audit logs from different calls mix together | Default changed to `None`; a new list is created inside the function |
| Bare `except: pass` (Bandit B110, Pylint W0702, Low) | Bug | 27 | Silently hides all errors, so dispensing an unknown medicine such as "Insulin" fails without any message | Replaced with an explicit `if name not in medicines` check that prints a clear message |
| No input validation | Bug | 13-20 | Negative quantities (`-10`) and a numeric medicine name (`404`) are accepted, producing corrupt stock | Names must be non-empty strings; negative quantities raise `ValueError` |
| Resource leak: files opened without `with` (Pylint R1732) | Quality | 57, 62 | Files are not closed if an error occurs between `open` and `close` | Used `with open(...)` context managers |
| `global` statement (Pylint W0603) | Quality | 63 | Reassigning a module-level global is error-prone | Updated the dict in place using `clear()` and `update()` |
| Unused imports `sys`, `logging` (Pylint W0611, Flake8 F401) | Style | 2, 6 | Dead code that clutters the file | Removed |
| Non-snake_case function names (Pylint C0103) | Style | 13-84 | `addMedicine`, `isExpired`, etc. violate PEP 8 | Renamed to `add_medicine`, `is_expired`, etc. |
| Missing docstrings (Pylint C0114/C0116) | Style | module and all functions | No documentation | Added a module docstring and one for every function |
| Redundant `if/else` returning True/False (Pylint R1703, R1705) | Style | 35, 79 | Verbose branching around a boolean | Return the comparison directly |
| Formatting problems (Flake8 E302, E501, W291 etc.) | Style | throughout | Wrong blank lines, long lines, spacing | Reformatted to PEP 8 (79-character lines, two blank lines between functions) |
| Missing `if __name__ == "__main__"` guard | Quality | 107 | `main()` runs on import, so the module can't be reused or tested | Added the guard |
