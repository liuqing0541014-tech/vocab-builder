#!/usr/bin/env python3
"""为移动端添加语音fallback方案"""

with open("index.html") as f:
    html = f.read()

# 1. 添加 playAudio fallback 方法到 VocabApp
# 在 speakWord 方法之前插入
insert_before = "speakWord(word){if(!window.speechSynthesis){this.showToast(\"浏览器不支持语音\");return}"

new_methods = """playAudio(word){return new Promise((resolve,reject)=>{const audio=new Audio(`https://dict.youdao.com/dictvoice?audio=${encodeURIComponent(word)}&type=2`);audio.oncanplaythrough=()=>resolve(audio);audio.onerror=(e)=>reject(e);audio.play().catch(e=>reject(e));})}
speakWord(word){if(window.speechSynthesis){window.speechSynthesis.cancel();const u=new SpeechSynthesisUtterance(word);u.lang="en-US";u.rate=.9;try{const voices=window.speechSynthesis.getVoices();const enVoice=voices.find(v=>v.lang.startsWith("en"));if(enVoice)u.voice=enVoice}catch(e){}window.speechSynthesis.speak(u)}else{this.playAudio(word).catch(()=>this.showToast("语音播放失败，请检查网络"))}}"""

html = html.replace(insert_before, new_methods + "\n")

# 2. 修改 speak() 方法
old_speak = """async speak(){const w=this.studyQueue[this.currentStudy];if(!w)return;if(!window.speechSynthesis){this.showToast("浏览器不支持语音");return}window.speechSynthesis.cancel();await new Promise(r=>setTimeout(r,50));const u=new SpeechSynthesisUtterance(w.word);u.lang="en-US";u.rate=.9;try{const voices=window.speechSynthesis.getVoices();const enVoice=voices.find(v=>v.lang.startsWith("en"));if(enVoice)u.voice=enVoice}catch(e){}window.speechSynthesis.speak(u)}"""

new_speak = """async speak(){const w=this.studyQueue[this.currentStudy];if(!w)return;if(window.speechSynthesis){window.speechSynthesis.cancel();await new Promise(r=>setTimeout(r,50));const u=new SpeechSynthesisUtterance(w.word);u.lang="en-US";u.rate=.9;try{const voices=window.speechSynthesis.getVoices();const enVoice=voices.find(v=>v.lang.startsWith("en"));if(enVoice)u.voice=enVoice}catch(e){}window.speechSynthesis.speak(u)}else{try{await this.playAudio(w.word)}catch(e){this.showToast("语音播放失败，请检查网络")}}}"""

html = html.replace(old_speak, new_speak)

# 3. 修改 speakReview 方法
old_review = """speakReview(){const w=this.reviewQueue[this.currentReview];if(!w||!window.speechSynthesis)return;window.speechSynthesis.cancel();const u=new SpeechSynthesisUtterance(w.word);u.lang="en-US";u.rate=.9;try{const voices=window.speechSynthesis.getVoices();const enVoice=voices.find(v=>v.lang.startsWith("en"));if(enVoice)u.voice=enVoice}catch(e){}window.speechSynthesis.speak(u)}"""

new_review = """speakReview(){const w=this.reviewQueue[this.currentReview];if(!w)return;if(window.speechSynthesis){window.speechSynthesis.cancel();const u=new SpeechSynthesisUtterance(w.word);u.lang="en-US";u.rate=.9;try{const voices=window.speechSynthesis.getVoices();const enVoice=voices.find(v=>v.lang.startsWith("en"));if(enVoice)u.voice=enVoice}catch(e){}window.speechSynthesis.speak(u)}else{this.playAudio(w.word).catch(()=>this.showToast("语音播放失败"))}}"""

html = html.replace(old_review, new_review)

with open("index.html", "w") as f:
    f.write(html)

print("Done. Mobile TTS fallback added.")
