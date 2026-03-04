# AGENT EXECUTION PROTOCOL

You are not allowed to:

- Create new folders not specified
- Move files
- Rename architecture
- Duplicate financial logic
- Hardcode currency symbols

You MUST:

- Work phase-by-phase
- Stop after each phase
- Run self audit
- Show before/after diffs
- Use EUR only

All financial calculations must exist only in:

services/financial_engine.py

All KPI calculations must exist only in:

services/kpi_engine.py

No business logic allowed inside UI blocks.