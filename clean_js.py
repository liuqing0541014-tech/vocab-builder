import re

# Read inline JS
with open('/tmp/inline_js.js') as f:
    js = f.read()

# 1. Fix loadData - restore clean version
old_load = """loadData(){try{const d=localStorage.getItem(\"vocabData\");if(d){const o=JSON.parse(d);const wordCount=Object.keys(o.words||{}).length;this.words=o.words||{};this.sentences=o.sentences||[];this.studyLog=o.studyLog||[];this.pdfSource=o.pdfSource||\"\";this.settings={...this.settings,...o.settings};if(wordCount===0\u0026\u0026typeof PREBUILT_VOCAB!==\"undefined\"\u0026\u0026PREBUILT_VOCAB.words){this.words=PREBUILT_VOCAB.words||{};this.sentences=PREBUILT_VOCAB.sentences||[];this.studyLog=[];this.pdfSource=PREBUILT_VOCAB.pdfSource||\"ACSM_test.pdf\";this.settings={...this.settings,...PREBUILT_VOCAB.settings};this.showToast(\"已加载ACSΜ预置词库（\"+Object.keys(this.words).length+\"词）\");this.saveData()}document.getElementById(\"dailyNew\").value=this.settings.dailyNew;document.getElementById(\"dailyReview\").value=this.settings.dailyReview;document.getElementById(\"autoSpeak\").value=this.settings.autoSpeak;document.getElementById(\"showImage\").value=this.settings.showImage;if(document.getElementById(\"translateEngine\"))document.getElementById(\"translateEngine\").value=this.settings.translateEngine||\"libre\";this.renderStats()}else if(typeof PREBUILT_VOCAB!==\"undefined\"\u0026\u0026PREBUILT_VOCAB.words){this.words=PREBUILT_VOCAB.words||{};this.sentences=PREBUILT_VOCAB.sentences||[];this.studyLog=[];this.pdfSource=PREBUILT_VOCAB.pdfSource||\"ACSM_test.pdf\";this.settings={...this.settings,...PREBUILT_VOCAB.settings};document.getElementById(\"dailyNew\").value=this.settings.dailyNew;document.getElementById(\"dailyReview\").value=this.settings.dailyReview;document.getElementById(\"autoSpeak\").value=this.settings.autoSpeak;document.getElementById(\"showImage\").value=this.settings.showImage;this.showToast(\"已加载ACSΜ预置词库（\"+Object.keys(this.words).length+\"词）\");this.saveData();this.renderStats()}}catch(e){console.warn(\"loadData failed:\",e);this.showToast(\"加载失败，尝试加载预置词库\");if(typeof PREBUILT_VOCAB!==\"undefined\"\u0026\u0026PREBUILT_VOCAB.words){this.words=PREBUILT_VOCAB.words||{};this.sentences=PREBUILT_VOCAB.sentences||[];this.studyLog=[];this.pdfSource=PREBUILT_VOCAB.pdfSource||\"ACSM_test.pdf\";this.settings={...this.settings,...PREBUILT_VOCAB.settings};this.renderStats()}}}"""

new_load = """loadData(){const d=localStorage.getItem(\"vocabData\");if(d){const o=JSON.parse(d);this.words=o.words||{};this.sentences=o.sentences||[];this.studyLog=o.studyLog||[];this.pdfSource=o.pdfSource||\"\";this.settings={...this.settings,...o.settings};document.getElementById(\"dailyNew\").value=this.settings.dailyNew;document.getElementById(\"dailyReview\").value=this.settings.dailyReview;document.getElementById(\"autoSpeak\").value=this.settings.autoSpeak;document.getElementById(\"showImage\").value=this.settings.showImage;if(document.getElementById(\"translateEngine\"))document.getElementById(\"translateEngine\").value=this.settings.translateEngine||\"libre\";this.renderStats()}else if(typeof PREBUILT_VOCAB!==\"undefined\"\u0026\u0026PREBUILT_VOCAB.words){this.words=PREBUILT_VOCAB.words||{};this.sentences=PREBUILT_VOCAB.sentences||[];this.studyLog=[];this.pdfSource=PREBUILT_VOCAB.pdfSource||\"ACSM_test.pdf\";this.settings={...this.settings,...PREBUILT_VOCAB.settings};document.getElementById(\"dailyNew\").value=this.settings.dailyNew;document.getElementById(\"dailyReview\").value=this.settings.dailyReview;document.getElementById(\"autoSpeak\").value=this.settings.autoSpeak;document.getElementById(\"showImage\").value=this.settings.showImage;this.saveData();this.showToast(\"已加载ACSΜ预置词库（\"+Object.keys(this.words).length+\"词）\");this.renderStats()}}"""

if old_load in js:
    js = js.replace(old_load, new_load)
    print("1. loadData replaced")
else:
    print("1. ERROR: loadData not found")

# 2. Fix saveData
old_save = """saveData(){try{localStorage.setItem(\"vocabData\",JSON.stringify({words:this.words,sentences:this.sentences,settings:this.settings,studyLog:this.studyLog,pdfSource:this.pdfSource}))}catch(e){console.warn(\"saveData failed:\",e)}}"""
new_save = """saveData(){localStorage.setItem(\"vocabData\",JSON.stringify({words:this.words,sentences:this.sentences,settings:this.settings,studyLog:this.studyLog,pdfSource:this.pdfSource}))}"""

if old_save in js:
    js = js.replace(old_save, new_save)
    print("2. saveData replaced")
else:
    print("2. ERROR: saveData not found")

# 3. Fix deleteWord - restore confirm
old_delete = """deleteWord(word){if(!confirm(`确定删除单词 \"${word}\" 吗？`))return;delete this.words[word];this.selectedWords.delete(word);this.saveData();document.getElementById(\"wordDetailModal\").classList.remove(\"show\");this.renderWordList();this.showToast(\"已删除\")}"""
# It's already correct! Let me check if it's wrong
print("3. deleteWord:", "deleteWord(word){if(!confirm" in js)

# 4. Fix clearAll - restore confirm
old_clear = """clearAll(){this.showToast(\"正在清空...\");try{this.words={};this.sentences=[];this.studyLog=[];this.pdfSource=\"\";this.selectedWords.clear();this.saveData();this.showToast(\"数据已清空\");this.renderStats()}catch(e){this.showToast(\"清空失败\")}}"""
new_clear = """clearAll(){if(!confirm(\"确定要清空所有数据吗？此操作不可恢复。\"))return;this.words={};this.sentences=[];this.studyLog=[];this.pdfSource=\"\";this.selectedWords.clear();this.saveData();this.showToast(\"数据已清空\");this.renderStats()}"""

if old_clear in js:
    js = js.replace(old_clear, new_clear)
    print("4. clearAll replaced")
else:
    print("4. ERROR: clearAll not found")

# 5. Fix batchDelete - restore confirm and const
old_batch = """batchDelete(){var count=this.selectedWords.size;this.selectedWords.forEach(function(w){delete this.words[w]}.bind(this));this.selectedWords.clear();this.saveData();this.renderWordList();this.showToast(\"已删除 \"+count+\" 个单词\")}"""
new_batch = """batchDelete(){if(!confirm(`确定删除选中的 ${this.selectedWords.size} 个单词吗？`))return;const count=this.selectedWords.size;this.selectedWords.forEach(w=>{delete this.words[w]});this.selectedWords.clear();this.saveData();this.renderWordList();this.showToast(`已删除 ${count} 个单词`)}"""

if old_batch in js:
    js = js.replace(old_batch, new_batch)
    print("5. batchDelete replaced")
else:
    print("5. ERROR: batchDelete not found")

# 6. Fix loadPrebuilt - restore confirm
old_prebuilt = """loadPrebuilt(){this.showToast(\"正在加载预置词库...\");if(typeof PREBUILT_VOCAB!==\"undefined\"\u0026\u0026PREBUILT_VOCAB.words){this.words=PREBUILT_VOCAB.words||{};this.sentences=PREBUILT_VOCAB.sentences||[];this.studyLog=[];this.pdfSource=PREBUILT_VOCAB.pdfSource||\"ACSM_test.pdf\";this.settings={...this.settings,...PREBUILT_VOCAB.settings};this.saveData();this.showToast(\"已加载ACSΜ预置词库（\"+Object.keys(this.words).length+\"词）\");this.renderStats();this.renderWordList()}else{this.showToast(\"预置词库不可用\")}}"""
new_prebuilt = """loadPrebuilt(){if(!confirm(\"加载预置词库会覆盖当前数据，确定吗？\"))return;if(typeof PREBUILT_VOCAB!==\"undefined\"\u0026\u0026PREBUILT_VOCAB.words){this.words=PREBUILT_VOCAB.words||{};this.sentences=PREBUILT_VOCAB.sentences||[];this.studyLog=[];this.pdfSource=PREBUILT_VOCAB.pdfSource||\"ACSM_test.pdf\";this.settings={...this.settings,...PREBUILT_VOCAB.settings};this.saveData();this.showToast(\"已加载ACSΜ预置词库（\"+Object.keys(this.words).length+\"词）\");this.renderStats();this.renderWordList()}else{this.showToast(\"预置词库不可用\")}}"""

if old_prebuilt in js:
    js = js.replace(old_prebuilt, new_prebuilt)
    print("6. loadPrebuilt replaced")
else:
    print("6. ERROR: loadPrebuilt not found")

with open('/tmp/clean_js.js', 'w') as f:
    f.write(js)

print(f"\nClean JS length: {len(js)}")
print("Saved to /tmp/clean_js.js")
