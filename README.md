# MISMO 3.4 Validator

A Python-based validator for MISMO 3.4 XML files, designed to validate against the Fannie Mae DU and MISMO Reference Model schemas.

---

## 📦 Requirements

- Python 3.8 or higher
- `lxml` library

---

## ⚙️ Installation

Clone this repository:

```bash
git clone https://github.com/eeexde/MISMO3.4Validator.git
cd MISMO3.4Validator
```

Create a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate       # On macOS/Linux
venv\Scripts\activate          # On Windows
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Usage

Validate the sample loan file (`your_project/loan_file.xml`):

```bash
python your_project/main.py
```

Validate one or more files, optionally against a different schema:

```bash
python your_project/main.py path/to/loan1.xml path/to/loan2.xml
python your_project/main.py path/to/loan.xml --xsd schemas/DU_Wrapper_3.4.0_B324.xsd
```

The script can be run from any directory. Exit codes, for use in CI or other scripts:

| Code | Meaning |
|------|---------|
| 0 | All files are valid |
| 1 | At least one file failed schema validation |
| 2 | A file or the schema could not be read/parsed |

Check that the schema set itself compiles:

```bash
python tools/validate_schema.py
```

Run the tests:

```bash
python -m unittest discover -s tests
```
