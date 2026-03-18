import requests
import re
from urllib.parse import urljoin
import concurrent.futures
import argparse
import json
import time
import random
from tqdm import tqdm

# Define the paths and patterns from the YAML file
PATHS = [
    "/.git/",
    "/.git/HEAD",
    "/.git/config",
    "/.git/index",
    "/.git/logs/HEAD",
    "/.git/refs/heads/master",
    "/.git/refs/heads/main",
    "/.git/description",
    "/.git/hooks/",
    "/.git/info/exclude",
]

# Regex patterns to match in the response
REGEX_PATTERNS = {
    "HEAD": r"ref: refs/heads/([\w-]+)",  # Extract branch name
    "config": r"\[core\]",  # Match [core] in .git/config
    "description": r"Unnamed repository",  # Match default description
}

# List of User-Agents to randomize requests
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Mobile Safari/537.36",
]

# Headers with a random User-Agent
def get_random_headers():
    return {"User-Agent": random.choice(USER_AGENTS)}

def check_git_exposure(url, path):
    """
    Check if a specific .git path is exposed on the target URL.
    """
    full_url = urljoin(url, path)
    try:
        response = requests.get(full_url, headers=get_random_headers(), timeout=10)
        if response.status_code == 200:
            result = {"status": "exposed", "content": response.text}

            # Check for regex matches
            if path.endswith("HEAD"):
                branch_match = re.search(REGEX_PATTERNS["HEAD"], response.text)
                if branch_match:
                    result["branch"] = branch_match.group(1)
            elif path.endswith("config"):
                config_match = re.search(REGEX_PATTERNS["config"], response.text)
                if config_match:
                    result["config"] = "Git config exposed"
            elif path.endswith("description"):
                description_match = re.search(REGEX_PATTERNS["description"], response.text)
                if description_match:
                    result["description"] = "Default Git description exposed"
            return path, result
        else:
            return path, {"status": "not exposed", "status_code": response.status_code}
    except requests.RequestException as e:
        return path, {"status": "error", "error": str(e)}

def scan_target(url, max_workers=10, delay=1):
    """
    Scan the target URL for exposed .git paths using concurrent requests.
    """
    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(check_git_exposure, url, path): path for path in PATHS}
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(PATHS), desc="Scanning"):
            path, result = future.result()
            results[path] = result
            time.sleep(delay)  # Add delay between requests
    return results

def print_results(results):
    """
    Print the results in a readable format.
    """
    for path, data in results.items():
        print(f"Path: {path}")
        print(f"Status: {data['status']}")
        if "branch" in data:
            print(f"Branch: {data['branch']}")
        if "config" in data:
            print(f"Config: {data['config']}")
        if "description" in data:
            print(f"Description: {data['description']}")
        if "error" in data:
            print(f"Error: {data['error']}")
        print("-" * 40)

def save_results(results, output_file):
    """
    Save the results to a file in JSON format.
    """
    with open(output_file, "w") as f:
        json.dump(results, f, indent=4)
    print(f"Results saved to {output_file}")

def main():
    """
    Main function to run the tool.
    """
    parser = argparse.ArgumentParser(description="Git Repository Exposure Scanner")
    parser.add_argument("url", help="Target URL to scan (e.g., http://example.com)")
    parser.add_argument("-o", "--output", help="Output file to save results (e.g., results.json)")
    parser.add_argument("-d", "--delay", type=int, default=1, help="Delay between requests in seconds")
    parser.add_argument("-w", "--workers", type=int, default=10, help="Number of concurrent workers")
    args = parser.parse_args()

    if not args.url.startswith(("http://", "https://")):
        print("Invalid URL. Please include http:// or https://")
        return

    print(f"Scanning {args.url}...")
    results = scan_target(args.url, max_workers=args.workers, delay=args.delay)
    print_results(results)

    if args.output:
        save_results(results, args.output)

if __name__ == "__main__":
    main()
