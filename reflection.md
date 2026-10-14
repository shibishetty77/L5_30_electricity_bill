# Draft Reflection — Verify Against the Lab Handout

**The supplied workspace did not contain the lab handout or its four exact
reflection questions. These draft responses are based on the lab objectives;
verify the actual questions with your instructor and revise the answers to
match them before submission.**

1. Static analysis helped identify problems before relying on manual execution:
   Pylint highlighted maintainability issues, Flake8 identified formatting
   problems, and Bandit found security risks such as shell command execution
   and unsafe XML parsing.

2. The tools overlap only partly. Pylint checks a broad set of code-quality and
   naming rules, Flake8 reports Python style and simple source errors, and
   Bandit focuses on potentially dangerous security patterns. Running all
   three exposed different classes of findings in the same small program.

3. The highest-risk finding was constructing a shell command from a meter
   address. I replaced it with an HTTP client, validated the input as an IP
   address, applied a timeout, and made request failures explicit. I also
   replaced the standard XML parser with `defusedxml` and removed the unused
   hard-coded password-like value.

4. I preserved the demonstration readings, tariff slabs, fixed charge, tax,
   extra fee, and existing behavior for a backwards meter reading. After the
   changes, the program still generated four bills and reported the same
   highest bill, average, and total. The reports provide repeatable evidence
   that the code-quality, security, and style findings were addressed.
