# 🚀 SnapBase — AI-Powered SQL Assistant (CLI)

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![MySQL](https://img.shields.io/badge/MySQL-Compatible-orange)
![CLI](https://img.shields.io/badge/Interface-CLI-green)
![AI](https://img.shields.io/badge/AI-NVIDIA%20LLaMA--4%20%7C%20Ollama-purple)
![Status](https://img.shields.io/badge/Status-Production%20Ready-success)

<p align="center">
  <img src="images/output-1.png" alt="SnapBase SQL Logo" width="480"/>
</p>

> **SnapBase** is a terminal-based, AI-assisted SQL tool that lets you query MySQL databases using **natural language or raw SQL**, with strong **safety guardrails**, **schema awareness**, and **persistent configuration**.

---

## ✨ Key Features

✅ Run directly from terminal using `snapbase`  
✅ Natural language → SQL using **NVIDIA LLaMA-4 (Maverick)** or **Ollama (local)**  
✅ Direct SQL execution supported (`SHOW TABLES`, `SELECT`, etc.)  
✅ Schema-aware (prevents hallucinated tables/columns)  
✅ Blocks destructive queries (`DROP`, `DELETE`, `TRUNCATE`, …)  
✅ Stable MySQL execution (no connection crashes)  
✅ Persistent API key & DB profiles  
✅ Switch databases **without restarting**  
✅ Clean, readable table output  
✅ Beginner-friendly & modular codebase  

---

## 🧠 Why SnapBase?

Most AI SQL tools:
- Guess schemas ❌
- Break connections ❌
- Execute unsafe queries ❌
- Hide errors ❌

**SnapBase is built differently**:
- Safety-first
- Honest about limitations
- Designed like a real production CLI tool

## 🤖 LLM Provider Options

SnapBase now supports **dual LLM providers** for maximum flexibility:

**NVIDIA LLaMA-4 (Cloud)**
- Powered by NVIDIA's cloud-based LLaMA-4 Maverick model
- Requires NVIDIA API key
- Best for complex queries requiring cloud compute

**Ollama (Local)**
- Runs completely locally on your machine
- No API key required
- Better privacy and no network dependency
- Requires Ollama to be installed and running

Switch between providers using the new "Manage LLM Provider" option in the main menu.

---

## 📦 Project Structure

```text
snapbase/
│
├── snapbase/
│   ├── main.py            # Entry point
│   ├── app/               # CLI & banner
│   ├── db/                # DB connection & execution
│   ├── llm/               # NVIDIA & Ollama LLM integration
│   ├── safety/            # Guardrails & validation
│   └── utils/             # Helpers (formatting, intent)
│
├── pyproject.toml         # CLI packaging config
├── snapbase_config.json   # Saved API key & DB profiles
└── README.md
```

---

## ⚙️ Installation

### 1️⃣ Prerequisites

* Python **3.9+**
* MySQL server running
* NVIDIA API Key (NIM / LLaMA-4) OR Ollama installed and running locally

---

### 2️⃣ Clone the Repository

```bash
git clone https://github.com/Prateekkp/SnapBase.git
cd snapbase
```

---

### 3️⃣ Install as CLI Tool

```bash
pip install -e .
```

This creates the command:

```bash
snapbase
```

---

## ▶️ Usage

### Start SnapBase

```bash
snapbase
```

### Example Session

```text
SnapBase> show tables
SnapBase> list all customers from Delhi
SnapBase> describe orders
SnapBase> :switch_db
SnapBase> exit
```

---

## 🔐 Security & Safety

SnapBase **blocks all destructive queries**:

❌ `DROP TABLE`
❌ `DELETE FROM`
❌ `TRUNCATE`
❌ `ALTER`

Only **read-safe analytical queries** are allowed by default.

---

## 🧪 Supported Query Types

| Category        | Supported  |
| --------------- | ---------- |
| SHOW / DESCRIBE | ✅          |
| SELECT queries  | ✅          |
| Aggregations    | ✅          |
| Joins           | ✅          |
| Nested queries  | ⚠️ Limited |
| DDL / DML       | ❌ Blocked  |

---

## ⚠️ Known Limitations (Honest Disclosure)

* Very complex SQL problems (multi-level correlated subqueries)
	may produce **logically incorrect SQL**
* SnapBase prioritizes **stability & safety over cleverness**
* Designed for **analyst & mid-level data workflows**, not DB internals

> This is a **design choice**, not a bug.

---

## 🧩 Tech Stack

* **Python**
* **MySQL**
* **mysql-connector-python**
* **NVIDIA LLaMA-4 Maverick** (Cloud) / **Ollama** (Local)
* **Requests**
* **Tabulate**

---

## 🎓 Use Cases

* Data Analysts exploring databases
* Students learning SQL with AI assistance
* Fast schema discovery
* Safer alternative to raw SQL consoles
* Interview / portfolio project

---

## ⭐ Why This Project Stands Out

✔ Not a notebook
✔ Not a CRUD app
✔ Not a copy-paste AI demo

**SnapBase is a real CLI product with engineering discipline.**

---

## 📜 License

MIT License — free to use, modify, and learn from.

---

## 🙌 Author

Built with engineering discipline & curiosity.

> If you find this useful, ⭐ the repo — it helps a lot.

