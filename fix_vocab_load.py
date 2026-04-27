#!/usr/bin/env python3
"""修复预置词库加载问题"""

with open("index.html") as f:
    html = f.read()

# 1. 确保 PREBUILT_VOCAB 在 window 上可用（兼容所有浏览器）
# 在 PREBUILT_VOCAB 定义后加一行
html = html.replace(
    "const PREBUILT_VOCAB={",
    "const PREBUILT_VOCAB={"
)
# 在第一个 </script> 前（或 PREBUILT_VOCAB 之后）添加 window 赋值
# 找到 PREBUILT_VOCAB 结束位置
pv_end = html.find("const PREBUILT_VOCAB=")
if pv_end > 0:
    # 找到对应的 };
    semicolon_pos = html.find("};", pv_end)
    if semicolon_pos > 0:
        insert_pos = semicolon_pos + 2
        html = html[:insert_pos] + "\nwindow.PREBUILT_VOCAB=PREBUILT_VOCAB;" + html[insert_pos:]

# 2. 修改 loadData()：如果 localStorage 里的 words 为空或太少，加载预置词库
# 当前 loadData 的 if(d) 分支需要扩展
old_if_d = """loadData(){const d=localStorage.getItem("vocabData");if(d){const o=JSON.parse(d);this.words=o.words||{};this.sentences=o.sentences||[];this.studyLog=o.studyLog||[];this.pdfSource=o.pdfSource||"";this.settings={...this.settings,...o.settings};document.getElementById("dailyNew").value=this.settings.dailyNew;document.getElementById("dailyReview").value=this.settings.dailyReview;document.getElementById("autoSpeak").value=this.settings.autoSpeak;document.getElementById("showImage").value=this.settings.showImage;if(document.getElementById("translateEngine"))document.getElementById("translateEngine").value=this.settings.translateEngine||"libre";this.renderStats()}"""

# 新版：if(d) 内加判断，如果 words 为空，仍然加载预置词库
new_load = """loadData(){const d=localStorage.getItem("vocabData");if(d){const o=JSON.parse(d);const wordCount=Object.keys(o.words||{}).length;this.words=o.words||{};this.sentences=o.sentences||[];this.studyLog=o.studyLog||[];this.pdfSource=o.pdfSource||"";this.settings={...this.settings,...o.settings};if(wordCount===0&&typeof PREBUILT_VOCAB!=="undefined"&&PREBUILT_VOCAB.words){this.words=PREBUILT_VOCAB.words||{};this.sentences=PREBUILT_VOCAB.sentences||[];this.studyLog=[];this.pdfSource=PREBUILT_VOCAB.pdfSource||"ACSM_test.pdf";this.settings={...this.settings,...PREBUILT_VOCAB.settings};this.showToast("已加载ACSΜ预置词库（"+Object.keys(this.words).length+"词）");this.saveData()}document.getElementById("dailyNew").value=this.settings.dailyNew;document.getElementById("dailyReview").value=this.settings.dailyReview;document.getElementById("autoSpeak").value=this.settings.autoSpeak;document.getElementById("showImage").value=this.settings.showImage;if(document.getElementById("translateEngine"))document.getElementById("translateEngine").value=this.settings.translateEngine||"libre";this.renderStats()}"""

if old_if_d in html:
    html = html.replace(old_if_d, new_load)
    print("Replaced loadData() if(d) branch")
else:
    print("ERROR: Could not find loadData() to replace")

# 3. 简化按钮的 onclick，避免 event.stopPropagation 在某些浏览器失效
old_btn = 'onclick="event.stopPropagation();app.loadPrebuilt()"'
new_btn = 'onclick="app.loadPrebuilt()"'
html = html.replace(old_btn, new_btn)

with open("index.html", "w") as f:
    f.write(html)

print("Done.")
