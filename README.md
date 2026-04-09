# ec2-safe-ops

A safety-first EC2 lifecycle management tool with human-in-the-loop verification and Excel-based workflow.

---

## 🔥 Overview

`ec2-safe-ops` is a CLI tool designed to safely manage EC2 instances (START / STOP / DELETE) by combining:

- **Human verification** (Excel)
- **Structured data** (CSV)
- **Controlled execution** (Python CLI)

This tool is built with a strong focus on **preventing operational mistakes** in real-world environments.

---

## 🎯 Problem Statement

Manual EC2 operations are prone to human error:

- Accidental deletion of production instances
- Wrong instance selection
- Bulk operations without verification

This tool introduces **multi-layer safeguards** to minimize such risks.

---

## 🧠 Design Philosophy

- Human-in-the-loop decision making
- Defense in depth (multiple safety layers)
- Separation of concerns (Excel / CSV / CLI)
- Fail-safe defaults (dry-run by default)

---

## 🔁 Resource Lifecycle Management (Concept)

This tool represents a part of a broader **resource lifecycle management strategy**.

Cloud resources typically go through multiple stages:

- Provisioning
- Active use
- Idle / unused
- Termination

This tool focuses on the **safe transition between states**, especially:

- Running → Stopped
- Stopped → Started
- Stopped → Terminated

Rather than fully automating decisions, this design intentionally incorporates:

- Human verification (HumanCheck)
- Explicit intent confirmation
- Controlled execution boundaries

This reflects a hybrid approach:

> **Automation + Human Judgment**

Future extensions may include:

- Automated lifecycle detection (idle resources)
- Policy-based lifecycle control
- Integration with monitoring and auto-healing systems


## ⚙️ Architecture

EC2 (AWS)  
↓  
**ec2_report.py** ↓  
**Excel** (HumanCheck)  
↓  
**CSV** (execution data)  
↓  
**CLI** (start / stop / delete)  
↓  
**AWS Execution** ↓  
**Archive** (old/)

---

## 🧩 Features

### ✅ Human Verification
- Excel-based review before execution
- Explicit approval via `HumanCheck` column

### 🛡️ Safety Mechanisms
- `dry-run` by default
- Production environment protection (Keyword-based)
- Action confirmation for DELETE
- Maximum execution limits
- Action consistency check (HumanCheck validation)
- Post-execution file archival

### 📊 Excel Workflow
- Visual cues (STOP / DELETE / SKIP)
- Dropdown-based input (HumanCheck)
- Filtering and controlled export via VBA Macro

### 🔁 Execution Control
- START / STOP / DELETE support
- Action-based filtering
- Verified-only execution

---

## 📁 Project Structure

```text
ec2-safe-ops/
├ src/
│  ├ ec2_app/  # CLI logic
│  └ common/   # Shared handlers
├ excel/
│  ├ ec2_safe_ops.xlsm
│  └ vba/       # Source code
├ infra/        # Terraform sandbox
├ tests/        # Future test cases
└ pyproject.toml
```

## 🧪 Testing Strategy
- rified functionality using Terraform-based sandbox environment.
- sted START / STOP / DELETE operations on real AWS resources.
- sured safety via dry-run and confirmation mechanisms.

## 🚀 Usage
### 1. Generate EC2 inventory
```
python src/ec2_app/ec2_report.py
```
### 2. Review in Excel
- Open excel/ec2_safe_ops.xlsm.
- Set HumanCheck column for desired actions.

### 3. Export CSV
- Use the Excel macro to generate the execution CSV.

### 4. Execute
```bash
# Dry-run
python src/ec2_app/ec2_stop.py

# Execute
python src/ec2_app/ec2_stop.py --execute
```
## ⚠️ Safety Notes
- DELETE requires explicit confirmation.
- Production environments are automatically excluded.
- Only verified records (HumanCheck) are executed.

## 👤 Author
Akira Takahashi

## 🛠 Future Improvements
- Unit tests (pytest)
- CLI enhancement with Typer
- AWS tagging integration
- Web UI alternative to Excel