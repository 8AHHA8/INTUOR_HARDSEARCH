# 🔍 INTUOR HARDSEARCH

**INTUOR HARDSEARCH** is an ultra-fast, minimalist, and lightweight desktop application written in Python, designed to search for text across multiple document formats.

The application was developed with performance, low memory consumption, and simplicity in mind. Its purpose is to make searching through large collections of documents quick, convenient, and efficient.

## ✨ Key Features

- **Lightning-Fast Search** – Powered by SQLite FTS5 (Full-Text Search), enabling efficient searching across thousands of indexed documents.
- **Broad Format Support** – Extracts and indexes text from the following file formats:
  - PDF (`.pdf`)
  - Microsoft Word (`.docx`, `.doc`)
  - Microsoft Excel (`.xlsx`, `.xls`)
  - Microsoft PowerPoint (`.pptx`, `.ppt`)
  - OpenDocument Text (`.odt`)
  - Plain Text (`.txt`)
- **Targeted Scanning** – Scan an entire local or network drive, or select a specific folder to search.
- **Smart Context Filtering** – When scanning a specific folder, results are filtered by location. The application can also notify you when matching content exists outside the selected directory.
- **Instant Preview** – Search results display the file name, full path, and a text snippet containing the matching phrase.
- **Quick Access** – Double-click a result to open the corresponding file and locate it in Windows Explorer.
- **Lightweight Interface** – Built with Python's native Tkinter library, avoiding resource-heavy GUI frameworks.
- **Dark Mode** – A dark interface designed for comfortable reading, featuring large, easily readable fonts.

## 🚀 Getting Started

### Prerequisites

Before running the application, make sure you have:

- Python 3.8 or newer.
- Windows operating system.
- Git (optional, for cloning the repository).

> **Note:** The application is primarily designed for Windows and uses Windows-specific functionality for network drive detection and file handling.

### Installation

**1. Clone the repository:**

Replace `YOUR_GITHUB_USERNAME` with your actual GitHub username.

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/INTUOR_HARDSEARCH.git
cd INTUOR_HARDSEARCH
```

**2. Create a virtual environment:**

```bash
python -m venv venv
```

**3. Activate the virtual environment:**

```bash
venv\Scripts\activate
```

**4. Install the required dependencies:**

```bash
pip install pyxtxt pymupdf
```

**5. Run the application:**

```bash
python main.py
```

## 🛠️ Building the Executable (.exe)

The project includes a preconfigured `Intuor.spec` file for building a standalone Windows executable using PyInstaller.

The application uses **one-directory mode**, which helps maintain faster startup times.

### Build Instructions

**1. Install PyInstaller:**

```bash
pip install pyinstaller
```

**2. Build the application:**

```bash
pyinstaller Intuor.spec
```

**3. Locate the generated application:**

After the build process finishes, the executable and its required dependencies will be available in:

```text
dist/INTUOR_HARDSEARCH/
```

> **Important:** The application is compiled in one-directory mode. To transfer it to another computer, copy or ZIP the entire `INTUOR_HARDSEARCH` directory from `dist`. Do not distribute the `.exe` file separately, as it requires the accompanying files.

## 📂 Project Structure

```text
INTUOR_HARDSEARCH/
│
├── core/
│   ├── db_connection.py   # SQLite database initialization and settings
│   ├── extractor.py       # Text extraction from supported document formats
│   ├── indexer.py         # Multithreaded document indexing
│   ├── search_engine.py   # Search engine based on FTS5 and Regex
│   └── worker.py          # Background processing and asynchronous scanning
│
├── ui/
│   ├── styles.py          # Color palette and font configuration
│   ├── ui_builder.py      # Main window and interface construction
│   ├── ui_handlers.py     # User interactions and event handling
│   └── ui_results.py      # Search result cards and presentation
│
├── main.py                # Application entry point
├── README.md              # Project documentation
├── .gitignore             # Git exclusion rules
├── Intuor.spec            # PyInstaller build configuration
└── ikona.ico              # Application icon
```

## 🔒 Privacy

INTUOR HARDSEARCH is designed to perform document indexing and searching locally.

- No document content is intentionally uploaded to external servers.
- The search index is stored locally in an SQLite database (`intuor.db`).
- All document processing takes place on the user's computer.

## ⚠️ Disclaimer

This project is intended for educational and personal use.

The application is provided as-is, without any guarantees regarding compatibility with every document or file format.

---

**Built with Python. Designed for speed, simplicity, and efficiency.**