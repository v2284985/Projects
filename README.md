# Git Repository Exposure Scanner

A Python tool to scan websites for exposed `.git` directories and files. This tool helps identify potential security risks by checking for publicly accessible `.git` files, which can leak sensitive information such as source code, configuration, and branch details.

---

## Features
- **Concurrent Scanning**: Uses multi-threading to speed up the scanning process.
- **Regex Matching**: Extracts useful information like branch names and Git configurations.
- **Randomized User-Agent**: Avoids detection by rotating `User-Agent` headers.
- **Progress Bar**: Displays real-time progress during the scan.
- **Output Options**: Saves results to a JSON file for further analysis.
- **Configurable**: Allows customization of delay, workers, and output file via command-line arguments.

---
## Author Information
- **Author**: Ved Kumar
- **Email**: devkumarmahto204@outlook.com
- **GitHub**: [devkumar-swipe](https://github.com/devkumar-swipe)
- **Tool Version**: 1.0.0

---

## Uses of This Tool
This tool is designed for:
CSecurity Researchers**: To identify misconfigured web servers that expose `.git` repositories.
- **Developers**: To check if their websites accidentally expose `.git` directories.
- **Penetration Testers**: To include in their reconnaissance phase for identifying potential information leaks.
- **Bug Bounty Hunters**: To find vulnerabilities related to exposed `.git` repositories.

---

## Installation

### Prerequisites
- Python 3.x installed on your system.
- `pip` for installing dependencies.

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/devkumar-swipe/gitfinder.git
   cd gitfinder

2. Install the dependencies:
   ```bash
   pip install -r requirements.txt

3. Activate your virtual environment 
   ```bash
   source ./<your_env_name>/bin/activate

3. Run the tool
   ```bash
   python gitfinder.py -h
   ```
4. Enter the target URL when prompted:
     ```bash
   Enter the target URL (e.g., http://example.com): http://example.com
   



### Usage
Basic Command
```bash
python gitfinder.py http://example.com
```

## Advanced Options
Save results to a file:
```bash
python gitfinder.py http://example.com -o results.json
```

## Set delay between requests (in seconds):
```bash
python gitfinder.py http://example.com -d 2

```
## Set number of concurrent workers:
```bash
python gitfinder.py http://example.com -w 20
```

## Combine options:
```bash
python gitfinder.py http://example.com -o results.json -d 1 -w 15
```

### Command-Line Arguments
- **Argument	Description**
<br>url	Target URL to scan (e.g., http://example.com).
<br>-o, --output	Save results to a file (e.g., results.json).
<br>-d, --delay	Delay between requests in seconds (default: 1).
<br>-w, --workers	Number of concurrent workers (default: 10).




---

### **How to Use**
1. Clone the repository.
2. Install dependencies using `pip install -r requirements.txt`.
3. Run the script as described in the `README.md` file.

This setup ensures your project is well-documented, easy to install, and ready for collaboration!
