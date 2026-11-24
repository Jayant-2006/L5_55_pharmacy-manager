# Lab 5: Reflection

**Name:** Jayant Mahishi | **SRN:** PES1UG24AM122

**1. Which issues were the easiest and hardest to fix?**
The easiest were style issues: removing unused imports, adding docstrings, renaming functions to snake_case and fixing blank lines. The hardest were the security fixes that had to keep the program working. Replacing `eval()` meant writing a small AST-based evaluator that accepts only numbers and basic arithmetic, and replacing `pickle` meant switching the save format to JSON and updating the load logic as well.

**2. Did the tools report any false positives, or issues you chose not to fix?**
Some Bandit findings were low severity and depend on context. For example, `random.randint` is harmless for a random label but wrong for prescription numbers that should be unguessable, and the `subprocess` module triggered warnings even when used without a shell. I did not silence them with `# nosec`. I removed the risky pattern so the code needs no exception. The tools also missed some bugs that I found by running the program. Stock accepted a negative quantity, a numeric medicine name was allowed, and dispensing "Insulin" failed silently. Static analysis cannot replace running and reading the output.

**3. How could static analysis be integrated into a real development workflow?**
It can run automatically as a pre-commit hook so style and security problems are caught before code is committed, and in a CI pipeline such as GitHub Actions so a pull request fails if Bandit finds a Medium or High issue or the Pylint score drops below a threshold. Running the tools early and often means problems are fixed while the code is fresh, instead of piling up before a release.

**4. What tangible improvements did you see in the code?**
The Pylint score rose from 4.83 to 10.00, Bandit findings fell from 8 to 0, and Flake8 warnings from 22 to 0. Beyond the numbers, the program is safer because it no longer allows code or command injection, no longer uses a broken hash, and no longer keeps a password in source. It is also more reliable and readable, with errors reported instead of swallowed, shared mutable state removed, documented functions and a consistent naming style.
