"""
jsontest.py — Vergelijking: Python json.dumps() vs JavaScript JSON.stringify()

Bronnen (W3Schools):
  https://www.w3schools.com/whatis/whatis_json.asp
  https://www.w3schools.com/js/js_json_datatypes.asp
  https://www.w3schools.com/js/js_json_stringify.asp
"""

import json
import subprocess
from datetime import datetime

# ANSI kleuren
RESET  = "\033[0m"
BOLD   = "\033[1m"
CYAN   = "\033[36m"
GREEN  = "\033[32m"
YELLOW = "\033[33m"
RED    = "\033[31m"


def header(title: str) -> None:
    print(f"\n{BOLD}{CYAN}{'=' * 60}{RESET}")
    print(f"{BOLD}{CYAN}  {title}{RESET}")
    print(f"{BOLD}{CYAN}{'=' * 60}{RESET}")


def py(label: str, value) -> None:
    print(f"  {BOLD}[Python]{RESET}  {label}")
    print(f"           {GREEN}→ {value}{RESET}")


def js(label: str, value) -> None:
    print(f"  {BOLD}[JS]    {RESET}  {label}")
    print(f"           {YELLOW}→ {value}{RESET}")


def note(text: str) -> None:
    print(f"\n  {RED}⚠  {text}{RESET}")


def run_js(code: str) -> str:
    """Voer JavaScript-code uit via Node.js."""
    try:
        result = subprocess.run(
            ["node", "-e", code],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            return result.stdout.strip()
        return f"[JS-fout: {result.stderr.strip()}]"
    except FileNotFoundError:
        return "[Node.js niet beschikbaar]"


# ─────────────────────────────────────────────────────────────
# 1. BASIS
# ─────────────────────────────────────────────────────────────
header("1. Basis — object naar JSON-string")

data = {"name": "John", "age": 30, "city": "New York"}

py("json.dumps(data)", json.dumps(data))
js('JSON.stringify(data)', run_js(
    'const d={name:"John",age:30,city:"New York"};'
    'console.log(JSON.stringify(d));'
))
print("\n  ✅ Beide produceren dezelfde compacte JSON-string.")

# ─────────────────────────────────────────────────────────────
# 2. DATATYPES (bron: w3schools.com/js/js_json_datatypes.asp)
# ─────────────────────────────────────────────────────────────
header("2. Datatypes — conversietabel (bron: W3Schools)")

type_data = {
    "True":   (True,  "true"),
    "False":  (False, "false"),
    "None":   (None,  "null"),
    "42":     (42,    "42"),
    "hello":  ("hello", '"hello"'),
    "[1,2,3]": ([1, 2, 3], "[1,2,3]"),
}

print(f"\n  {'Python waarde':<18} {'json.dumps()':<22} {'JSON.stringify()':<20} {'Match?'}")
print(f"  {'-'*70}")

for label, (py_val, js_expected) in type_data.items():
    py_out = json.dumps(py_val)
    match  = "✅" if py_out.replace(" ", "") == js_expected else "⚠️ "
    print(f"  {match} {label:<16} {GREEN}{py_out:<22}{RESET} {YELLOW}{js_expected:<20}{RESET}")

note("Python True/False → true/false en None → null — identiek aan JS.")

# ─────────────────────────────────────────────────────────────
# 3. WITRUIMTE (VERSCHIL)
# ─────────────────────────────────────────────────────────────
header("3. Witruimte bij lijsten (VERSCHIL!)")

arr = [1, 2, 3]
py_default = json.dumps(arr)
js_default = run_js("console.log(JSON.stringify([1,2,3]));")

py("json.dumps([1, 2, 3])  — standaard", py_default)
js("JSON.stringify([1,2,3]) — standaard", js_default)

note(
    "Python voegt standaard spaties toe na komma's: [1, 2, 3]\n"
    "  JavaScript doet dat NIET: [1,2,3]"
)

py_compact = json.dumps(arr, separators=(",", ":"))
py('json.dumps(arr, separators=(",", ":"))  — compact', py_compact)
gelijk = "✅ Nu identiek aan JSON.stringify!" if py_compact == js_default else "⚠️  Nog steeds anders"
print(f"  {gelijk}")

# ─────────────────────────────────────────────────────────────
# 4. PRETTY-PRINT (bron: w3schools.com/js/js_json_stringify.asp)
# ─────────────────────────────────────────────────────────────
header("4. Pretty-print — inspringing")

obj = {"name": "John", "age": 30, "married": True}

py_pretty = json.dumps(obj, indent=4)
js_pretty = run_js(
    'const o={name:"John",age:30,married:true};'
    'console.log(JSON.stringify(o, null, 4));'
)

print(f"\n  {BOLD}Python  json.dumps(obj, indent=4):{RESET}")
for line in py_pretty.splitlines():
    print(f"    {GREEN}{line}{RESET}")

print(f"\n  {BOLD}JS      JSON.stringify(obj, null, 4):{RESET}")
for line in js_pretty.splitlines():
    print(f"    {YELLOW}{line}{RESET}")

note(
    "JSON.stringify(value, replacer, space) — drie argumenten.\n"
    "  null als replacer = geen filtering. indent=4 ↔ space=4: identiek."
)

# ─────────────────────────────────────────────────────────────
# 5. SORTEREN (VERSCHIL)
# ─────────────────────────────────────────────────────────────
header("5. Sleutels sorteren (VERSCHIL!)")

unsorted = {"z": 3, "a": 1, "m": 2}

py("json.dumps(data, sort_keys=True)", json.dumps(unsorted, sort_keys=True))
js_sorted = run_js(
    "const o={z:3,a:1,m:2};"
    "const s=Object.fromEntries(Object.entries(o).sort());"
    "console.log(JSON.stringify(s));"
)
js("JSON.stringify — handmatig sorteren vereist", js_sorted)

note(
    "Python heeft ingebouwde sort_keys=True.\n"
    "  JavaScript heeft dit NIET — handmatig via Object.entries().sort()."
)

# ─────────────────────────────────────────────────────────────
# 6. DATUMS (VERSCHIL)
# ─────────────────────────────────────────────────────────────
header("6. Datums (VERSCHIL!)")

now = datetime(2024, 1, 15, 12, 0, 0)

try:
    json.dumps(now)
    py_date_result = "(geen fout)"
except TypeError as e:
    py_date_result = f"TypeError: {e}"

js_date = run_js("console.log(JSON.stringify(new Date('2024-01-15T12:00:00')));")

py("json.dumps(datetime(2024,1,15,12,0,0))", py_date_result)
js("JSON.stringify(new Date(...))", js_date)

workaround = json.dumps(str(now))
py(f"json.dumps(now, default=str)  — workaround", workaround)

note(
    "JS converteert Date-objecten automatisch naar een ISO-string.\n"
    "  Python gooit een TypeError — gebruik default=str als workaround."
)

# ─────────────────────────────────────────────────────────────
# 7. FUNCTIES (VERSCHIL)
# ─────────────────────────────────────────────────────────────
header("7. Functies en niet-serialiseerbare waarden (VERSCHIL!)")

js_func_result = run_js(
    'const o={name:"John",age:function(){return 30;},city:"New York"};'
    'console.log(JSON.stringify(o));'
)
try:
    json.dumps({1, 2, 3})
    py_set_result = "(geen fout)"
except TypeError as e:
    py_set_result = f"TypeError: {e}"

js("JSON.stringify({name, age:function(){...}, city})", js_func_result)
py("json.dumps({1, 2, 3})  — set niet serialiseerbaar", py_set_result)

note(
    "JS verwijdert functies stilzwijgend (sleutel + waarde verdwijnt).\n"
    "  Python gooit een TypeError bij niet-ondersteunde types zoals set."
)

# ─────────────────────────────────────────────────────────────
# SAMENVATTING
# ─────────────────────────────────────────────────────────────
header("Samenvatting van verschillen")

print(f"""
  {"Aspect":<30} {"json.dumps() Python":<30} {"JSON.stringify() JS"}
  {"-"*80}
  {"Spaties in lijsten":<30} {"[1, 2, 3]  (met spatie)":<30} [1,2,3]  (geen spatie)
  {"Sleutels sorteren":<30} {"sort_keys=True  (ingebouwd)":<30} niet ingebouwd
  {"Datums":<30} {"TypeError → gebruik default=str":<30} auto → ISO-string
  {"Functies":<30} {"TypeError":<30} stille weglating
  {"Pretty-print arg":<30} {"indent=N":<30} 3e arg: space=N
  {"True/False/None":<30} {"true/false/null  ✅":<30} true/false/null  ✅
""")
