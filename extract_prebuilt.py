#!/usr/bin/env python3
"""将PREBUILT_VOCAB从index.html中移出到单独的prebuilt.js文件"""

with open("index.html") as f:
    html = f.read()

# Find PREBUILT_VOCAB block
pv_start = html.find("const PREBUILT_VOCAB=")
pv_end_marker = html.find("window.PREBUILT_VOCAB=PREBUILT_VOCAB;", pv_start)

if pv_start > 0 and pv_end_marker > 0:
    # Include the newline after window.PREBUILT_VOCAB=PREBUILT_VOCAB;
    pv_end = pv_end_marker + len("window.PREBUILT_VOCAB=PREBUILT_VOCAB;")
    # Also consume trailing newline if present
    if html[pv_end:pv_end+1] == "\n":
        pv_end += 1
    
    # Remove the inline PREBUILT_VOCAB block
    html = html[:pv_start] + html[pv_end:]
    print("Removed inline PREBUILT_VOCAB block")
    
    # Add prebuilt.js script tag before the main <script> tag
    # Find the main inline <script> tag (not the pdf.js one)
    main_script = html.find("<script>\nconst STOP_WORDS")
    if main_script > 0:
        html = html[:main_script] + '<script src="prebuilt.js"></script>\n' + html[main_script:]
        print("Added prebuilt.js script reference")
    else:
        print("WARNING: Could not find main script tag")
else:
    print("ERROR: Could not find PREBUILT_VOCAB block")

with open("index.html", "w") as f:
    f.write(html)

# Verify
with open("index.html") as f:
    content = f.read()

print("\nVerification:")
print("- PREBUILT_VOCAB inline:", "const PREBUILT_VOCAB=" in content)
print("- prebuilt.js reference:", 'src="prebuilt.js"' in content)
print("- File size:", len(content))
