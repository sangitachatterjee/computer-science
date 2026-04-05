# Task 1 — File Read & Write Basics (6 marks)
import json
from datetime import datetime

print("Task 1 — File Read & Write Basics (6 marks)")
NOTES_FILE = "python_notes.txt"

try:
    import requests
except ImportError:
    requests = None

initial_lines = [
    "Topic 1: Variables store data. Python is dynamically typed.",
    "Topic 2: Lists are ordered and mutable.",
    "Topic 3: Dictionaries store key-value pairs.",
    "Topic 4: Loops automate repetitive tasks.",
    "Topic 5: Exception handling prevents crashes.",
]

# Part A - Write
with open(NOTES_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(initial_lines) + "\n")
print("File written successfully.")

append_lines = [
    "Topic 6: Type hints document expected data shapes for readers and tools.",
    "Topic 7: Virtual environments isolate project dependencies cleanly.",
]

with open(NOTES_FILE, "a", encoding="utf-8") as f:
    f.write("\n".join(append_lines) + "\n")
print("Lines appended.")

# Part B — Read
with open(NOTES_FILE, "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines, start=1):
    print(f"{i}. {line.rstrip('\n')}")

print(f"\nTotal number of lines: {len(lines)}")

keyword = input("\nEnter a keyword to search for: ").strip()
if not keyword:
    print("No keyword entered; skipping search.")
else:
    kw_lower = keyword.lower()
    matches = [line.rstrip("\n") for line in lines if kw_lower in line.lower()]
    if matches:
        print(f"\nLines containing '{keyword}' (case-insensitive):")
        for line in matches:
            print(line)
    else:
        print(f"\nNo lines contain the keyword '{keyword}'. Try another word from the notes.")

# Task 2 — API Integration (8 marks)
print("\n\nTask 2 — API Integration (8 marks)")

BASE = "https://dummyjson.com/products"
API_TIMEOUT = 5  # Task 3 Part C — triggers Timeout if the server is too slow


def print_products_table(products):
    col_id = 4
    col_title = 30
    col_cat = 15
    col_price = 10
    col_rating = 8
    sep = (
        f"{'-' * col_id}|{'-' * col_title}|{'-' * col_cat}|"
        f"{'-' * col_price}|{'-' * col_rating}"
    )
    header = (
        f"{'ID':<{col_id}}| {f'Title':<{col_title - 1}}| "
        f"{f'Category':<{col_cat}}| {f'Price':<{col_price - 1}}| {f'Rating':<{col_rating}}"
    )
    print(header)
    print(sep)
    for p in products:
        pid = p.get("id", "")
        title = str(p.get("title", ""))[: col_title - 1]
        cat = str(p.get("category", ""))[: col_cat]
        price = p.get("price", 0)
        price_str = f"${float(price):.2f}"
        rating = p.get("rating", "")
        print(
            f"{str(pid):<{col_id}}| {title:<{col_title - 1}}| "
            f"{cat:<{col_cat}}| {price_str:<{col_price - 1}}| {str(rating):<{col_rating}}"
        )


if requests is None:
    print(
        "Skipping Tasks 2–3 API sections: install requests "
        "(python3 -m pip install requests, preferably in a venv)."
    )
    products_20 = []
    laptops = []
else:
    # Step 1 — Fetch and display 20 products
    try:
        r1 = requests.get(f"{BASE}?limit=20", timeout=API_TIMEOUT)
    except requests.exceptions.ConnectionError:
        print("Connection failed. Please check your internet.")
        r1 = None
    except requests.exceptions.Timeout:
        print("Request timed out. Try again later.")
        r1 = None
    except Exception as e:
        print(e)
        r1 = None

    products_20 = []
    if r1 is not None:
        try:
            r1.raise_for_status()
            data1 = r1.json()
            products_20 = data1.get("products", [])
        except Exception as e:
            print(e)

    if products_20:
        print("\nStep 1 — Products (limit=20)\n")
        print_products_table(products_20)

        # Step 2 — Filter rating >= 4.5, sort by price descending
        filtered = [p for p in products_20 if float(p.get("rating") or 0) >= 4.5]
        filtered.sort(key=lambda p: float(p.get("price") or 0), reverse=True)
        print("\nStep 2 — Rating ≥ 4.5, sorted by price (high → low)\n")
        if filtered:
            print_products_table(filtered)
        else:
            print("(No products matched the filter.)")

    # Step 3 — Laptops category
    try:
        r3 = requests.get(f"{BASE}/category/laptops", timeout=API_TIMEOUT)
    except requests.exceptions.ConnectionError:
        print("Connection failed. Please check your internet.")
        r3 = None
    except requests.exceptions.Timeout:
        print("Request timed out. Try again later.")
        r3 = None
    except Exception as e:
        print(e)
        r3 = None

    laptops = []
    if r3 is not None:
        try:
            r3.raise_for_status()
            data3 = r3.json()
            laptops = data3.get("products", [])
        except Exception as e:
            print(e)

    if laptops:
        print("\nStep 3 — Laptops (name and price)\n")
        for item in laptops:
            print(f"  {item.get('title', 'N/A')}: ${float(item.get('price', 0)):.2f}")

    # Step 4 — POST add product
    payload = {
        "title": "My Custom Product",
        "price": 999,
        "category": "electronics",
        "description": "A product I created via API",
    }
    try:
        r4 = requests.post(f"{BASE}/add", json=payload, timeout=API_TIMEOUT)
    except requests.exceptions.ConnectionError:
        print("Connection failed. Please check your internet.")
        r4 = None
    except requests.exceptions.Timeout:
        print("Request timed out. Try again later.")
        r4 = None
    except Exception as e:
        print(e)
        r4 = None

    if r4 is not None:
        print("\nStep 4 — POST /products/add (full response)\n")
        print(f"HTTP status: {r4.status_code}")
        print(f"Headers (content-type): {r4.headers.get('Content-Type', 'n/a')}")
        try:
            print(json.dumps(r4.json(), indent=2))
        except ValueError:
            print(r4.text)


# Task 3 — Exception Handling (7 marks)
print("\n\nTask 3 — Exception Handling (7 marks)")


# Part A — Guarded Calculator
def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "Error: Cannot divide by zero"
    except TypeError:
        return "Error: Invalid input types"


print("\nPart A — safe_divide tests:")
print(safe_divide(10, 2))
print(safe_divide(10, 0))
print(safe_divide("ten", 2))


# Part B — Guarded File Reader
def read_file_safe(filename):
    try:
        with open(filename, encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    finally:
        print("File operation attempt complete.")


print("\nPart B — read_file_safe tests:")
print("--- python_notes.txt ---")
content_ok = read_file_safe("python_notes.txt")
if content_ok is not None:
    print(content_ok.rstrip("\n"))
print("--- ghost_file.txt ---")
read_file_safe("ghost_file.txt")


# Part C — Robust API calls: applied in Task 2 (timeout=5, ConnectionError, Timeout, Exception)


# Part D — Input validation loop
print("\nPart D — Product lookup by ID (1–100, or 'quit'):")
if requests is None:
    print("Skipping: requests is not installed.")
else:
    while True:
        raw = input(
            "Enter a product ID to look up (1–100), or 'quit' to exit: "
        ).strip()
        if raw.lower() == "quit":
            break

        if not raw.isdigit():
            print("Warning: enter a whole number between 1 and 100, or 'quit'.")
            continue

        pid = int(raw)
        if pid < 1 or pid > 100:
            print("Warning: ID must be between 1 and 100.")
            continue

        url = f"https://dummyjson.com/products/{pid}"
        try:
            r = requests.get(url, timeout=API_TIMEOUT)
        except requests.exceptions.ConnectionError:
            print("Connection failed. Please check your internet.")
            continue
        except requests.exceptions.Timeout:
            print("Request timed out. Try again later.")
            continue
        except Exception as e:
            print(e)
            continue

        if r.status_code == 404:
            print("Product not found.")
        elif r.status_code == 200:
            try:
                prod = r.json()
                print(f"{prod.get('title', 'N/A')} — ${float(prod.get('price', 0)):.2f}")
            except Exception as e:
                print(e)
        else:
            print(f"Unexpected HTTP status: {r.status_code}")


# Task 4 — Logging to File (4 marks)
print("\n\nTask 4 — Logging to File (4 marks)")

ERROR_LOG = "error_log.txt"


def log_error(context, error_kind, detail):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] ERROR in {context}: {error_kind} — {detail}\n"
    with open(ERROR_LOG, "a", encoding="utf-8") as f:
        f.write(line)


if requests is None:
    print("Skipping Task 4 demos: requests is not installed.")
else:
    # Demo 1: unreachable host → ConnectionError (Python exception)
    try:
        requests.get(
            "https://this-host-does-not-exist-xyz.com/api",
            timeout=API_TIMEOUT,
        )
    except requests.exceptions.ConnectionError as e:
        msg = str(e).strip() or "No connection could be made"
        log_error("fetch_products", "ConnectionError", msg)

    # Demo 2: missing product → HTTP 404 (check status_code, not try/except)
    r999 = requests.get("https://dummyjson.com/products/999", timeout=API_TIMEOUT)
    if r999.status_code != 200:
        log_error(
            "lookup_product",
            "HTTPError",
            f"{r999.status_code} Not Found for product ID 999",
        )

print("\n--- Full contents of error_log.txt ---")
try:
    with open(ERROR_LOG, "r", encoding="utf-8") as f:
        print(f.read().rstrip("\n") or "(empty file)")
except FileNotFoundError:
    print("(error_log.txt does not exist yet.)")
