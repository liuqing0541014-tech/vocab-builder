#!/usr/bin/env python3
"""Rebuild index.html with clean JS"""

with open('/tmp/html_part.html') as f:
    html = f.read()

with open('/tmp/clean_js.js') as f:
    js = f.read()

# Assemble
final = html + '<script>\n' + js + '\n</script>\n</body>\n</html>'

with open('index.html', 'w') as f:
    f.write(final)

print(f"index.html rebuilt: {len(final)} bytes")

# Verify
with open('index.html') as f:
    content = f.read()
print(f"Braces balance: open={content.count('{')}, close={content.count('}')}")
print(f"Script tags: open={content.count('<script>')}, close={content.count('</script>')}")
print(f"Has VocabApp: {'class VocabApp' in content}")
print(f"Has const app: {'const app=new VocabApp()' in content}")
print(f"Ends with html: {content.strip().endswith('</html>')}")
