#!/usr/bin/env python3
"""把预置词库嵌入index.html"""
import re

with open("prebuilt.js") as f:
    prebuilt_js = f.read().strip()

with open("index.html") as f:
    html = f.read()

# 1. 插入 PREBUILT_VOCAB 到 script 标签开头
html = html.replace("<script>", "<script>\n" + prebuilt_js + "\n")

# 2. 修改 loadData() — 添加预置词库加载
old_load = """loadData(){const d=localStorage.getItem("vocabData");if(d){const o=JSON.parse(d);this.words=o.words||{};this.sentences=o.sentences||[];this.studyLog=o.studyLog||[];this.pdfSource=o.pdfSource||"";this.settings={...this.settings,...o.settings};document.getElementById("dailyNew").value=this.settings.dailyNew;document.getElementById("dailyReview").value=this.settings.dailyReview;document.getElementById("autoSpeak").value=this.settings.autoSpeak;document.getElementById("showImage").value=this.settings.showImage;if(document.getElementById("translateEngine"))document.getElementById("translateEngine").value=this.settings.translateEngine||"libre";this.renderStats()}}"""

new_load = """loadData(){const d=localStorage.getItem("vocabData");if(d){const o=JSON.parse(d);this.words=o.words||{};this.sentences=o.sentences||[];this.studyLog=o.studyLog||[];this.pdfSource=o.pdfSource||"";this.settings={...this.settings,...o.settings};document.getElementById("dailyNew").value=this.settings.dailyNew;document.getElementById("dailyReview").value=this.settings.dailyReview;document.getElementById("autoSpeak").value=this.settings.autoSpeak;document.getElementById("showImage").value=this.settings.showImage;if(document.getElementById("translateEngine"))document.getElementById("translateEngine").value=this.settings.translateEngine||"libre";this.renderStats()}else if(typeof PREBUILT_VOCAB!=="undefined"&&PREBUILT_VOCAB.words){this.words=PREBUILT_VOCAB.words||{};this.sentences=PREBUILT_VOCAB.sentences||[];this.studyLog=[];this.pdfSource=PREBUILT_VOCAB.pdfSource||"ACSM_test.pdf";this.settings={...this.settings,...PREBUILT_VOCAB.settings};document.getElementById("dailyNew").value=this.settings.dailyNew;document.getElementById("dailyReview").value=this.settings.dailyReview;document.getElementById("autoSpeak").value=this.settings.autoSpeak;document.getElementById("showImage").value=this.settings.showImage;this.showToast("已加载ACSΜ预置词库（"+Object.keys(this.words).length+"词）");this.saveData();this.renderStats()}}"""

html = html.replace(old_load, new_load)

# 3. 在上传区域加 "加载预置词库" 按钮
old_upload = """<div class="upload-zone" id="uploadZone" onclick="document.getElementById('fileInput').click()">"""
new_upload = """<div style="text-align:center;margin-bottom:12px"><button class="btn primary" onclick="event.stopPropagation();app.loadPrebuilt()">📚 加载ACSΜ预置词库</button></div><div class="upload-zone" id="uploadZone" onclick="document.getElementById('fileInput').click()">"""
html = html.replace(old_upload, new_upload)

# 4. 添加 loadPrebuilt() 方法到 VocabApp
old_clear = "clearAll(){if(!confirm("
new_method = """loadPrebuilt(){if(!confirm("加载预置词库会覆盖当前数据，确定吗？"))return;if(typeof PREBUILT_VOCAB!=="undefined"&&PREBUILT_VOCAB.words){this.words=PREBUILT_VOCAB.words||{};this.sentences=PREBUILT_VOCAB.sentences||[];this.studyLog=[];this.pdfSource=PREBUILT_VOCAB.pdfSource||"ACSM_test.pdf";this.settings={...this.settings,...PREBUILT_VOCAB.settings};this.saveData();this.showToast("已加载ACSΜ预置词库（"+Object.keys(this.words).length+"词）");this.renderStats();this.renderWordList()}else{this.showToast("预置词库不可用")}}clearAll(){if(!confirm("""
html = html.replace(old_clear, new_method)

with open("index.html", "w") as f:
    f.write(html)

print("Done. index.html updated with prebuilt vocab.")
