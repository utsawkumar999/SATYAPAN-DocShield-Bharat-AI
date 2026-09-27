import os

# Read frontend HTML
html_path = r"E:\SIH\code\frontend\index.html"
with open(html_path, "r", encoding="utf-8") as f:
    raw_html = f.read()

# Copy index.html into backend app
with open(r"E:\SIH\code\backend\app\index.html", "w", encoding="utf-8") as f:
    f.write(raw_html)

# Clean and rebuild main.py safely
main_path = r"E:\SIH\code\backend\app\main.py"
with open(main_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

clean_lines = []
for line in lines:
    if "from fastapi.responses import HTMLResponse" in line or "import os" in line:
        continue
    if "serve_ui" in line or "serve_ui_direct" in line:
        continue
    clean_lines.append(line)

content = "".join(clean_lines)

# Prepend clean imports
content = "from fastapi.responses import HTMLResponse, FileResponse\nimport os\n" + content

# Replace root function safely with fallback
old_pattern = 'return {"status": "DocShield AI Omega Engine Online"}'
safe_root = """# Serve complete UI safely
    candidates = [
        os.path.join(os.path.dirname(__file__), "index.html"),
        os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "index.html"),
        "code/backend/app/index.html",
        "code/frontend/index.html",
        "frontend/index.html",
        "index.html"
    ]
    for c in candidates:
        if os.path.exists(c):
            try:
                with open(c, "r", encoding="utf-8") as f:
                    return HTMLResponse(content=f.read())
            except Exception:
                pass
    return HTMLResponse(content='''<!DOCTYPE html><html><head><meta http-equiv="refresh" content="0; url=/docs" /></head><body><h2>Loading SATYAPAN Console...</h2></body></html>''')"""

if old_pattern in content:
    content = content.replace(old_pattern, safe_root)
else:
    import re
    content = re.sub(r'return HTMLResponse\(open\(os\.path\.join\(.*?\)\.read\(\)\)', safe_root, content)

with open(main_path, "w", encoding="utf-8") as f:
    f.write(content)

print("✅ FIX_APPLIED_SUCCESSFULLY")
