# Virtual Environment Setup

To create and activate a Python virtual environment for this project:

```bash
python3 -m venv .venv
source .venv/bin/activate   # On Linux/Mac
.venv\Scripts\activate    # On Windows
```

Once activated, install dependencies:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

To deactivate the environment:
```bash
deactivate
```
