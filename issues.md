# Static Analysis Findings

Line numbers below refer to the original `electricity_bill.py` used for the
before reports.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Shell command injection risk | Bandit B605 — High | 63 | `os.system()` assembled a `curl` command from `meterIp`, allowing shell metacharacters in the input to alter the command. | Replaced shell execution with `http.client.HTTPConnection`, validated the input with `ipaddress.ip_address`, added a timeout, checked the HTTP status, and let connection errors reach the caller. |
| Unsafe XML parsing | Bandit B314 — Medium | 18 | `ElementTree.fromstring()` parsed XML without protections against malicious XML constructs. | Switched to `defusedxml.ElementTree.fromstring()` and documented the `defusedxml` runtime dependency in `requirements.txt` and the README. |
| Unsafe XML parser import | Bandit B405 — Low | 3 | The standard-library `xml.etree.ElementTree` parser import is flagged for parsing untrusted XML. | Replaced the parser import with `defusedxml.ElementTree`. |
| Hard-coded password-like string | Bandit B105 — Low | 13 | `CLERK_PASSWORD` contained a hard-coded password and was not used by the program. | Removed the unused credential; the application does not require clerk authentication. |
| Mutable default argument | Pylint W0102 | 42 | `extras={}` could share mutable state across bill-generation calls. | Changed the default to `None` and create a fresh dictionary within `generate_bill()`. |
| Unused currency argument | Pylint W0613 | 50 | `averageBill(currency)` did not use `currency`; its caller passed `"INR"` without effect. | Removed the parameter and updated the call to `average_bill()`; the existing rupee-denominated amounts remain unchanged. |
| Missing encoding | Pylint W1514 | 57 | `saveBills()` opened the output file without specifying a text encoding. | Opened `bills.json` with explicit UTF-8 encoding. |
| Naming and documentation | Pylint C0103, C0114, C0116 | 1, 17, 22, 29, 34, 42, 50, 56, 61, 67 | The module/functions/variables lacked documentation or used camelCase names. | Added a module docstring and useful function docstrings; renamed functions and local variables to snake_case, updating all callers. |
| Whitespace and line length | Flake8 E302, E203, E501, E225 | 22, 44, 72, 76 | The original source had insufficient function spacing, whitespace before a colon, a line over 79 characters, and a missing operator space. | Applied PEP 8 blank-line, spacing, wrapping, and operator formatting. |

The backwards-reading demonstration still reports zero units and prints its
warning; no tariff or billing rules were changed.
