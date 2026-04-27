#!/usr/bin/env python3
"""从PDF提取生词，生成与前端兼容的词库JSON"""
import re
import json
import subprocess
import sys

# ====== 停用词（与前端一致）======
STOP_WORDS = set([
"the","a","an","and","or","but","in","on","at","to","for","of","with","by","from","as","is","was","are","were","be","been","being","have","has","had","do","does","did","will","would","could","should","may","might","must","shall","can","need","dare","ought","used","get","got","go","went","come","came","take","took","make","made","see","saw","know","knew","think","thought","say","said","tell","told","ask","give","gave","find","found","want","wanted","use","used","work","worked","feel","felt","try","tried","leave","left","call","called","good","new","first","last","long","great","little","own","other","old","right","big","high","different","small","large","next","early","young","important","few","public","bad","same","able","all","each","every","both","either","neither","one","two","three","four","five","six","seven","eight","nine","ten","this","that","these","those","i","you","he","she","it","we","they","me","him","her","us","them","my","your","his","its","our","their","mine","yours","hers","ours","theirs","myself","yourself","himself","herself","itself","ourselves","yourselves","themselves","what","which","who","whom","whose","whatever","whichever","whoever","whomever","that","whether","if","than","then","so","very","too","just","now","only","also","back","after","before","up","down","out","off","over","under","again","further","here","there","when","where","why","how","once","more","most","some","any","no","nor","not","only","own","same","than","too","very","just","don","didn","wasn","weren","haven","hasn","hadn","won","wouldn","couldn","shouldn","isn","aren","ain","let","s","t","ll","ve","re","d","m","o","c","e","g","p","r","u","v","w","x","y","z","fig","figure","table","et","al","eg","ie","etc","vs","vol","no","pp","page","pages","doi","http","https","www","com","org","edu","gov"
])

ABBREVS = set(["rt","rtx","ctrl","rm","rmx","rom","fitt","vp","amstar","cca","qoe","pubmed","ovid","ebscohost","1rm","wk","yr","nd","nc","by","ccby","acsm","mss","doi","vol","pp","fig","et","al","vs","med","lww","bj","de","ma","br","jc","ja","sm","ag","mr","dl","md","kw","phd","md","dr","jr","sr","prof","mr","mrs","ms","jw"])

AWL = set(["analysis","approach","area","assessment","assume","authority","available","benefit","concept","consistent","constitutional","context","contract","create","data","definition","derived","distribution","economic","environment","established","estimate","evidence","export","factors","financial","formula","function","identified","income","indicate","individual","interpretation","involved","issue","labour","legal","legislation","major","method","occur","percent","period","policy","principle","procedure","process","required","research","response","role","section","sector","significant","similar","source","specific","structure","theory","variable","adaptation","prescription","hypertrophy","isometric","isotonic","isokinetic","eccentric","concentric","periodization","sarcopenia","frailty","metabolite","biomarker","hemodynamic","neuromuscular","musculoskeletal","endocrine","homeostasis","inflammation","cytokine","hormone","insulin","glucose","lipid","cholesterol","adipose","catabolic","anabolic","proteolysis","phosphorylation","kinase","receptor","signaling","transcription","translation","expression","genotype","phenotype","polymorphism","heritability","variance","covariance","correlation","regression","coefficient","residual","heterogeneity","homogeneity","randomization","allocation","blinding","placebo","washout","crossover","longitudinal","prospective","retrospective","observational","cohort","prevalence","incidence","morbidity","mortality","hazard","interval","significance","parameter","precision","validity","reliability","reproducibility","generalizability","confounding","mediation","moderation","interaction","endpoint","diagnosis","prognosis","etiology","pathogenesis","pathophysiology","cascade","feedback","network","construct","dimension","domain","magnitude","intensity","dosage","exposure","duration","timing","sequence","review","systematic","resistance","exercise","supplemental","performance","physical","program","medicine"])

IRREGULAR = {"children":"child","people":"person","men":"man","women":"woman","teeth":"tooth","feet":"foot","mice":"mouse","geese":"goose","improves":"improve","enhanced":"enhance","increased":"increase","decreased":"decrease","provided":"provide","showed":"show","compared":"compare","reported":"report","completed":"complete","performed":"perform","prescribed":"prescribe","manipulated":"manipulate","examined":"examine","included":"include","excluded":"exclude","determined":"determine","required":"require","involved":"involve","changed":"change","measured":"measure","assessed":"assess","calculated":"calculate","yielded":"yield","impacted":"impact","affected":"affect","produced":"produce","reduced":"reduce","improved":"improve","based":"base","using":"use","training":"train","running":"run","walking":"walk","talking":"talk","working":"work","learning":"learn","studying":"study","trying":"try","applying":"apply","carrying":"carry","moving":"move","living":"live","giving":"give","driving":"drive","writing":"write","making":"make","taking":"take","coming":"come","going":"go","doing":"do","saying":"say","getting":"get","putting":"put","letting":"let","setting":"set","sitting":"sit","standing":"stand","lying":"lie","dying":"die","traine":"train","trained":"train","analysed":"analyse","analyzing":"analyse","analyzes":"analyse"}

def lemmatize(w):
    lw = w.lower()
    if lw in IRREGULAR:
        return IRREGULAR[lw]
    if lw == "versus":
        return "versus"
    if lw.endswith("ies") and len(lw) > 4:
        return lw[:-3] + "y"
    if lw.endswith("ves"):
        return lw[:-3] + "f"
    if lw.endswith("s") and not lw.endswith("ss") and len(lw) > 3 and not lw.endswith("sis"):
        return lw[:-1]
    if lw.endswith("ied"):
        return lw[:-3] + "y"
    if lw.endswith("ed") and len(lw) > 3:
        s = lw[:-2]
        if s.endswith("i"):
            return s[:-1] + "y"
        if s.endswith("c"):
            return s + "e"
        return s
    if lw.endswith("ing") and len(lw) > 5:
        s = lw[:-3]
        if s.endswith("y"):
            return s
        if len(s) > 2 and s[-1] != "e" and s[-2] in "aeiou" and s[-1] not in "aeiou" and len(s) <= 4:
            return s + "e"
        return s
    return lw

def get_difficulty(freq, word):
    w = word.lower()
    ln = len(w)
    is_academic = w in AWL or lemmatize(w) in AWL
    if ln >= 12:
        return "hard"
    if is_academic and ln >= 8:
        return "hard"
    if is_academic and ln >= 5:
        return "medium"
    if ln <= 4:
        return "easy"
    if freq >= 30 and ln <= 6:
        return "easy"
    if freq >= 8:
        return "medium"
    if ln >= 10:
        return "hard"
    return "medium"

INLINE_DICT = {
"abdominal":"腹部的","absolute":"绝对的","abstract":"抽象的","academic":"学术的","academy":"学院","accept":"接受","access":"访问","accident":"事故","accommodation":"住宿","accompany":"陪同","accomplish":"完成","accordance":"一致","according":"根据","account":"账户","accounting":"会计","accuracy":"精度","accurate":"准确的","accustomed":"习惯的","achieve":"实现","achievement":"成就","acid":"酸","acknowledge":"承认","acquire":"获取","acquisition":"获得","action":"行动","activate":"激活","active":"活跃的","activity":"活动","actual":"实际的","acuity":"敏锐","acute":"急性的","adapt":"适应","adaptation":"适应","addition":"添加","additional":"额外的","address":"地址","adequate":"足够的","adjust":"调整","adjustment":"调整","administer":"管理","administration":"管理","administrative":"行政的","admission":"许可","admit":"承认","adopt":"采用","adult":"成人","advance":"推进","advanced":"高级的","advantage":"优势","adverse":"不利的","advertise":"广告","advice":"建议","aerobic":"有氧的","aesthetic":"美学的","affect":"影响","affected":"受影响的","affiliate":"附属","affinity":"亲和力","afford":"负担得起","afterward":"后来","agency":"机构","agenda":"议程","agent":"代理人","aggregate":"总计","aggression":"侵略","aggressive":"侵略的","agility":"敏捷性","agreement":"协议","agriculture":"农业","aid":"援助","aim":"目标","airway":"气道","alert":"警觉","algebra":"代数","algorithm":"算法","align":"对齐","alignment":"对齐","alike":"相似的","alive":"活着的","alliance":"联盟","allocate":"分配","allow":"允许","allowance":"津贴","alongside":"在旁边","alter":"改变","alternate":"交替","alternative":"替代的","altogether":"总共","ambiguity":"歧义","ambiguous":"模糊的","ambition":"野心","amendment":"修正案","amino":"氨基酸","amongst":"在...之中","anabolic":"合成代谢的","anaerobic":"无氧的","analog":"模拟","analogous":"类似的","analogy":"类比","analyse":"分析","analysis":"分析","analytical":"分析的","analyze":"分析","anatomy":"解剖学","ancestor":"祖先","anchor":"锚","ancient":"古代的","anecdotal":"轶事的","anecdote":"轶事","angle":"角度","animate":"动画","ankle":"脚踝","annotate":"注释","announce":"宣布","annual":"年度的","anomaly":"异常","anonymous":"匿名的","antagonist":"拮抗剂","anterior":"前面的","antibiotic":"抗生素","anticipate":"预期","antioxidant":"抗氧化剂","anxiety":"焦虑","apparatus":"器械","apparent":"明显的","appeal":"呼吁","appearance":"外观","appendix":"附录","appetite":"食欲","application":"应用","apply":"应用","appoint":"任命","appreciate":"欣赏","approach":"方法","appropriate":"适当的","approval":"批准","approximate":"近似的","arbitrary":"任意的","architect":"建筑师","architecture":"建筑","archive":"档案","area":"区域","argue":"争论","arise":"出现","arithmetic":"算术","arrange":"安排","array":"数组","arrest":"逮捕","arrival":"到达","arrive":"到达","arterial":"动脉的","artery":"动脉","article":"文章","articulate":"发音","artificial":"人工的","ascending":"上升的","aspect":"方面","aspiration":"志向","assemble":"组装","assembly":"集会","assert":"断言","assess":"评估","assessment":"评估","asset":"资产","assign":"分配","assignment":"任务","assist":"协助","assistance":"援助","assistant":"助手","associate":"关联","association":"协会","assume":"假设","assumption":"假设","assurance":"保证","assure":"保证","asthma":"哮喘","asymptomatic":"无症状的","asymptotic":"渐近的","athlete":"运动员","athletic":"运动的","atmosphere":"大气","atomic":"原子的","attach":"附加","attachment":"附件","attain":"达到","attempt":"尝试","attend":"参加","attention":"注意","attitude":"态度","attribute":"属性","audience":"观众","audio":"音频","audit":"审计","author":"作者","authority":"权威","authorize":"授权","auto":"自动","automatic":"自动的","autonomy":"自治","auxiliary":"辅助的","availability":"可用性","available":"可用的","avenue":"大道","average":"平均","avoid":"避免","aware":"意识到的","awareness":"意识","axis":"轴","backup":"备份","bacteria":"细菌","balance":"平衡","bandwidth":"带宽","bankrupt":"破产","banner":"横幅","barrier":"障碍","base":"基础","baseline":"基线","basement":"地下室","basic":"基本的","basis":"基础","battery":"电池","bearing":"轴承","beginner":"初学者","behalf":"代表","behave":"表现","behavior":"行为","behaviour":"行为","belief":"信念","benchmark":"基准","beneficial":"有益的","benefit":"益处","bestow":"授予","beyond":"超越","bias":"偏见","bilateral":"双边的","binary":"二进制的","bind":"绑定","biochemical":"生物化学的","biochemistry":"生物化学","biomechanics":"生物力学","biopsy":"活检","bipolar":"双极的","birthday":"生日","blanket":"毯子","block":"块","bloodstream":"血流","bodily":"身体的","body":"身体","bond":"债券","bonus":"奖金","booklet":"小册子","boom":"繁荣","boost":"促进","border":"边界","boredom":"无聊","borrow":"借","bound":"界限","boundary":"边界","brainstorming":"头脑风暴","branch":"分支","breach":"违反","breadth":"广度","breakdown":"故障","breakthrough":"突破","breathing":"呼吸","brief":"简短的","briefing":"简报","brightness":"亮度","broadband":"宽带","brochure":"手册","bronchial":"支气管的","bronchus":"支气管","browse":"浏览","browser":"浏览器","brutal":"残酷的","buffer":"缓冲","build":"构建","builder":"建造者","building":"建筑","bulb":"灯泡","bulk":"批量","bulletin":"公告","burden":"负担","burnout":"倦怠","burst":"爆发","bypass":"旁路"
}

def get_inline_translation(word):
    w = word.lower()
    return INLINE_DICT.get(w)

def extract_words(text, source=""):
    words = re.findall(r'\b[a-zA-Z]{2,}\b', text)
    freq = {}
    for w in words:
        lw = w.lower()
        if lw in STOP_WORDS or lemmatize(lw) in STOP_WORDS:
            continue
        if lw in ABBREVS or lemmatize(lw) in ABBREVS:
            continue
        base = lemmatize(lw)
        freq[base] = freq.get(base, 0) + 1
    sorted_words = sorted(freq.items(), key=lambda x: -x[1])[:300]
    words_dict = {}
    for w, f in sorted_words:
        trans = get_inline_translation(w)
        translations = [trans] if trans else []
        words_dict[w] = {
            "word": w,
            "freq": f,
            "diff": get_difficulty(f, w),
            "status": "new",
            "created": 0,
            "translations": translations,
            "example": "",
            "interval": 0,
            "easeFactor": 2.5,
            "due": 0,
            "reviewCount": 0,
            "pdfSource": source
        }
    return words_dict

def extract_sentences(text):
    sentences = []
    parts = re.sub(r'([.!?])\s+', r'\1|', text).split("|")
    for s in parts:
        s = s.strip()
        if len(s) > 20 and len(s) < 400 and not re.search(r'https?://|www\.', s) and not re.search(r'[\u4e00-\u9fa5]', s):
            sentences.append({"en": s, "zh": ""})
    return sentences

def main():
    pdf_path = sys.argv[1] if len(sys.argv) > 1 else "ACSM_test.pdf"
    # 用pdftotext提取文本
    result = subprocess.run(["pdftotext", pdf_path, "-"], capture_output=True, text=True)
    text = result.stdout
    
    words = extract_words(text, pdf_path)
    sentences = extract_sentences(text)
    
    vocab_data = {
        "words": words,
        "sentences": sentences,
        "settings": {"dailyNew":10,"dailyReview":30,"autoSpeak":"off","showImage":"on","translateEngine":"libre"},
        "studyLog": [],
        "pdfSource": pdf_path
    }
    
    print(json.dumps(vocab_data, ensure_ascii=False, indent=2))
    print(f"\n# 提取了 {len(words)} 个单词, {len(sentences)} 个句子", file=sys.stderr)

if __name__ == "__main__":
    main()
