# static-site-generator
This is a guided project on creating a static site generator, which takes raw content, or markdown files, and turns them into a static website

## ⚙ Setup Instructions

1. Install Python and Git:

```bash
sudo apt update
sudo apt install -y git python3 python3-pip
```

2. Clone the repository:
```bash
git clone https://github.com/fotis-sofoulis/static-site-generator.git
```

3. Create a virtual environment:
```bash
python3 -m venv .venv && source .venv/bin/activate
```

4. Install the requirements:
```bash
pip install -r requirements.txt
```

5. After the installation you should be able to generate a static website, with(you may change the files in the `content/` and the `static/` folder to customize your static website):
```bash
python3 main.py
```

## 📋 ToDo
1. Create implementation for `word/docx` files.
2. Update to `uv` package manager.
