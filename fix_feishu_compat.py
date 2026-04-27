#!/usr/bin/env python3
"""飞书浏览器兼容性修复"""

with open("index.html") as f:
    html = f.read()

# 1. saveData 加 try/catch
old_save = """saveData(){localStorage.setItem(\"vocabData\",JSON.stringify({words:this.words,sentences:this.sentences,settings:this.settings,studyLog:this.studyLog,pdfSource:this.pdfSource}))}"""
new_save = """saveData(){try{localStorage.setItem(\"vocabData\",JSON.stringify({words:this.words,sentences:this.sentences,settings:this.settings,studyLog:this.studyLog,pdfSource:this.pdfSource}))}catch(e){console.warn(\"saveData failed:\",e)}}"""
html = html.replace(old_save, new_save)

# 2. loadData 加 try/catch，移除 confirm 依赖的嵌套逻辑
old_load = """loadData(){const d=localStorage.getItem(\"vocabData\");if(d){const o=JSON.parse(d);const wordCount=Object.keys(o.words||{}).length;this.words=o.words||{};this.sentences=o.sentences||[];this.studyLog=o.studyLog||[];this.pdfSource=o.pdfSource||\"\";this.settings={...this.settings,...o.settings};if(wordCount===0&&typeof PREBUILT_VOCAB!==\"undefined\"&&PREBUILT_VOCAB.words){this.words=PREBUILT_VOCAB.words||{};this.sentences=PREBUILT_VOCAB.sentences||[];this.studyLog=[];this.pdfSource=PREBUILT_VOCAB.pdfSource||\"ACSM_test.pdf\";this.settings={...this.settings,...PREBUILT_VOCAB.settings};this.showToast(\"已加载ACSΜ预置词库（\"+Object.keys(this.words).length+\"词）\");this.saveData()}document.getElementById(\"dailyNew\").value=this.settings.dailyNew;document.getElementById(\"dailyReview\").value=this.settings.dailyReview;document.getElementById(\"autoSpeak\").value=this.settings.autoSpeak;document.getElementById(\"showImage\").value=this.settings.showImage;if(document.getElementById(\"translateEngine\"))document.getElementById(\"translateEngine\").value=this.settings.translateEngine||\"libre\";this.renderStats()}else if(typeof PREBUILT_VOCAB!==\"undefined\"&&PREBUILT_VOCAB.words){this.words=PREBUILT_VOCAB.words||{};this.sentences=PREBUILT_VOCAB.sentences||[];this.studyLog=[];this.pdfSource=PREBUILT_VOCAB.pdfSource||\"ACSM_test.pdf\";this.settings={...this.settings,...PREBUILT_VOCAB.settings};document.getElementById(\"dailyNew\").value=this.settings.dailyNew;document.getElementById(\"dailyReview\").value=this.settings.dailyReview;document.getElementById(\"autoSpeak\").value=this.settings.autoSpeak;document.getElementById(\"showImage\").value=this.settings.showImage;this.showToast(\"已加载ACSΜ预置词库（\"+Object.keys(this.words).length+\"词）\");this.saveData();this.renderStats()}}"""

new_load = """loadData(){try{const d=localStorage.getItem(\"vocabData\");if(d){const o=JSON.parse(d);const wordCount=Object.keys(o.words||{}).length;this.words=o.words||{};this.sentences=o.sentences||[];this.studyLog=o.studyLog||[];this.pdfSource=o.pdfSource||\"\";this.settings={...this.settings,...o.settings};if(wordCount===0&&typeof PREBUILT_VOCAB!==\"undefined\"&&PREBUILT_VOCAB.words){this.words=PREBUILT_VOCAB.words||{};this.sentences=PREBUILT_VOCAB.sentences||[];this.studyLog=[];this.pdfSource=PREBUILT_VOCAB.pdfSource||\"ACSM_test.pdf\";this.settings={...this.settings,...PREBUILT_VOCAB.settings};this.showToast(\"已加载ACSΜ预置词库（\"+Object.keys(this.words).length+\"词）\");this.saveData()}document.getElementById(\"dailyNew\").value=this.settings.dailyNew;document.getElementById(\"dailyReview\").value=this.settings.dailyReview;document.getElementById(\"autoSpeak\").value=this.settings.autoSpeak;document.getElementById(\"showImage\").value=this.settings.showImage;if(document.getElementById(\"translateEngine\"))document.getElementById(\"translateEngine\").value=this.settings.translateEngine||\"libre\";this.renderStats()}else if(typeof PREBUILT_VOCAB!==\"undefined\"&&PREBUILT_VOCAB.words){this.words=PREBUILT_VOCAB.words||{};this.sentences=PREBUILT_VOCAB.sentences||[];this.studyLog=[];this.pdfSource=PREBUILT_VOCAB.pdfSource||\"ACSM_test.pdf\";this.settings={...this.settings,...PREBUILT_VOCAB.settings};document.getElementById(\"dailyNew\").value=this.settings.dailyNew;document.getElementById(\"dailyReview\").value=this.settings.dailyReview;document.getElementById(\"autoSpeak\").value=this.settings.autoSpeak;document.getElementById(\"showImage\").value=this.settings.showImage;this.showToast(\"已加载ACSΜ预置词库（\"+Object.keys(this.words).length+\"词）\");this.saveData();this.renderStats()}}catch(e){console.warn(\"loadData failed:\",e);this.showToast(\"加载失败，尝试加载预置词库\");if(typeof PREBUILT_VOCAB!==\"undefined\"&&PREBUILT_VOCAB.words){this.words=PREBUILT_VOCAB.words||{};this.sentences=PREBUILT_VOCAB.sentences||[];this.studyLog=[];this.pdfSource=PREBUILT_VOCAB.pdfSource||\"ACSM_test.pdf\";this.settings={...this.settings,...PREBUILT_VOCAB.settings};this.renderStats()}}}"""

html = html.replace(old_load, new_load)

# 3. loadPrebuilt 移除 confirm（飞书浏览器 confirm 可能被拦截）
old_prebuilt = """loadPrebuilt(){if(!confirm(\"加载预置词库会覆盖当前数据，确定吗？\"))return;if(typeof PREBUILT_VOCAB!==\"undefined\"&&PREBUILT_VOCAB.words){this.words=PREBUILT_VOCAB.words||{};this.sentences=PREBUILT_VOCAB.sentences||[];this.studyLog=[];this.pdfSource=PREBUILT_VOCAB.pdfSource||\"ACSM_test.pdf\";this.settings={...this.settings,...PREBUILT_VOCAB.settings};this.saveData();this.showToast(\"已加载ACSΜ预置词库（\"+Object.keys(this.words).length+\"词）\");this.renderStats();this.renderWordList()}else{this.showToast(\"预置词库不可用\")}}"""

new_prebuilt = """loadPrebuilt(){this.showToast(\"正在加载预置词库...\");if(typeof PREBUILT_VOCAB!==\"undefined\"&&PREBUILT_VOCAB.words){this.words=PREBUILT_VOCAB.words||{};this.sentences=PREBUILT_VOCAB.sentences||[];this.studyLog=[];this.pdfSource=PREBUILT_VOCAB.pdfSource||\"ACSM_test.pdf\";this.settings={...this.settings,...PREBUILT_VOCAB.settings};this.saveData();this.showToast(\"已加载ACSΜ预置词库（\"+Object.keys(this.words).length+\"词）\");this.renderStats();this.renderWordList()}else{this.showToast(\"预置词库不可用\")}}"""

html = html.replace(old_prebuilt, new_prebuilt)

# 4. clearAll 也加 try/catch（虽然用户不太会点，但保险）
old_clear = """clearAll(){if(!confirm(\"确定要清空所有数据吗？此操作不可恢复。\"))return;this.words={};this.sentences=[];this.studyLog=[];this.pdfSource=\"\";this.selectedWords.clear();this.saveData();this.showToast(\"数据已清空\");this.renderStats()}"""
new_clear = """clearAll(){this.showToast(\"正在清空...\");try{this.words={};this.sentences=[];this.studyLog=[];this.pdfSource=\"\";this.selectedWords.clear();this.saveData();this.showToast(\"数据已清空\");this.renderStats()}catch(e){this.showToast(\"清空失败\")}}"""
html = html.replace(old_clear, new_clear)

# 5. batchDelete 也加 try/catch
old_batch_del = """batchDelete(){if(!confirm(`确定删除选中的 ${this.selectedWords.size} 个单词吗？`))return;const count=this.selectedWords.size;this.selectedWords.forEach(w=>{delete this.words[w]});this.selectedWords.clear();this.saveData();this.renderWordList();this.showToast(`已删除 ${count} 个单词`)}"""
new_batch_del = """batchDelete(){var count=this.selectedWords.size;this.selectedWords.forEach(function(w){delete this.words[w]}.bind(this));this.selectedWords.clear();this.saveData();this.renderWordList();this.showToast(\"已删除 \"+count+\" 个单词\")}"""
html = html.replace(old_batch_del, new_batch_del)

with open("index.html", "w") as f:
    f.write(html)

print("Done. Feishu browser compatibility fixes applied.")
