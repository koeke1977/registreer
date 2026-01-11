
import os
import shutil
from pathlib import Path

# Bronmap (Dropbox)
SOURCE = r"C:\Users\Surface\Dropbox\FilipApresSki\Qr Codes"

# Doelmap in repo
IMAGES = Path("qr/images")
OUTPUT = Path("qr/index.html")

IMAGES.mkdir(parents=True, exist_ok=True)

# Kopieer nieuwe QR afbeeldingen
for file in os.listdir(SOURCE):
    if file.lower().endswith((".png", ".jpg", ".jpeg")):
        src = Path(SOURCE) / file
        dst = IMAGES / file
        if not dst.exists():
            shutil.copy2(src, dst)
            print("Gekopieerd:", file)

# Verzamel afbeeldingen
images = sorted([f.name for f in IMAGES.iterdir()
                 if f.suffix.lower() in (".png",".jpg",".jpeg")])

# HTML items
items = "\n".join([
    f'''
    <div class="item" data-name="{img.lower()}">
        <img src="images/{img}" loading="lazy">
        <div class="label">{img}</div>
    </div>
    '''
    for img in images
])

html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>QR Codes</title>
<style>
body {{
    font-family: Arial, sans-serif;
    background: #0e0e0e;
    color: white;
    margin: 0;
}}
header {{
    padding: 20px;
    text-align: center;
}}
input {{
    padding: 12px;
    width: 280px;
    font-size: 16px;
    border-radius: 6px;
    border: none;
}}
.grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(160px,1fr));
    gap: 14px;
    padding: 20px;
}}
.item {{
    background: #1c1c1c;
    padding: 10px;
    border-radius: 10px;
    text-align: center;
}}
.item img {{
    width: 100%;
    border-radius: 6px;
}}
.label {{
    font-size: 12px;
    opacity: 0.7;
    margin-top: 6px;
    word-break: break-all;
}}
</style>
</head>

<body>
<header>
    <h1>🔎 QR Codes</h1>
    <input id="search" placeholder="Zoek op naam..." oninput="filterItems()">
</header>

<div class="grid" id="grid">
{items}
</div>

<script>
function filterItems() {{
    const term = document.getElementById("search").value.toLowerCase();
    document.querySelectorAll(".item").forEach(item => {{
        const name = item.dataset.name;
        item.style.display = name.includes(term) ? "block" : "none";
    }});
}}
</script>

</body>
</html>
"""

OUTPUT.write_text(html, encoding="utf-8")
print("✅ QR Gallery bijgewerkt.")
