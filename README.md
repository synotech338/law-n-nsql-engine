# 🟪 Law-N N-SQL Engine

Minimal execution engine for **N-SQL (Network SQL)** in the **Law-N** stack.

This is **Repo #8** in the Law-N Part 3 rollout.

Where `law-n-nsql-spec` defines the language,  
`law-n-nsql-engine` actually **runs** the queries.

---

## What this repo does (now)

✅ Parses a small, practical subset of N-SQL:

- `SELECT ... FROM network.routes ...`
- `SELECT ... FROM network.devices ...`
- `OPTIMIZE ROUTE "A" TO "B" ...`
- `INSPECT FREQUENCY 3.42GHz`
- `INSPECT DEVICE "0xA4C1"`

✅ Builds a simple AST (abstract syntax tree)  
✅ Routes queries to dedicated executors  
✅ Executes against an **in-memory mock network** adapter:

- devices
- towers
- routes
- frequencies

This is a **reference engine** for:

- tower simulators  
- CLSI prototypes  
- network-native OS experiments  
- Law-N demos & visualizations  

---

## High-Level Architecture

```text
N-SQL text
   ↓
 parser.py      → tokenizes and parses into AST
   ↓
 ast.py         → typed AST nodes (SelectQuery, OptimizeRoute, InspectQuery)
   ↓
 engine.py      → dispatches to executors
   ↓
 executors/     → select / optimize / inspect
   ↓
 adapters/      → in-memory mock network (later: CLSI, towers, devices)

