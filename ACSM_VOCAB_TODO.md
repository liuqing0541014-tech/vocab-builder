# ACSM运动科学词库 v8 — 已知问题与待修复清单

> 生成日期：2026-04-29  
> 版本：v8（无领域配额限制版）  
> 总词数：1853  
> 对应脚本：`extract_acsm_v8.py`  
> 对应输出：`prebuilt_acsm_v8.js`（702.6KB）

---

## 问题1：311个术语无原文例句（占比16.8%）

**现状**：1542/1853有例句，311个空缺。

**根因分析**：
1. **频率过低（~70%）**：出现1-3次的低频词，大概率落在：
   - 表格/图注（太短，被30字符句子过滤筛掉）
   - 参考文献列表（非完整句子）
   - 章节标题（无句号，句切分不到）
   - 列表项（单独一行）
   - 示例：`gestational diabetes` freq=1，`back scratch` freq=1
2. **缩写/全称错位（~20%）**：复合词是must-keep列表里的全称，但原文只写缩写
   - `balance error scoring system` → 原文写 `BESS`
   - `delayed onset muscle soreness` → 原文写 `DOMS`
   - `heart failure with preserved ejection fraction` → 原文写 `HFpEF`
3. **大小写/连字符变体（~10%）**：
   - `pvc` → 原文写 `PVC`（全大写）
   - `nonfreezing cold injury` → 可能写 `non-freezing`（带连字符）
   - `30-second chair stand` → 可能写 `30-second chair-stand`

**修复方案**：
- [ ] 放宽句子长度门槛（20-300字符 → 15-400字符）
- [ ] 缩写-全称双向匹配：搜全称例句时同时搜缩写形式
- [ ] 连字符变体匹配：`chair stand` 也要匹配 `chair-stand`
- [ ] 大小写不敏感已启用，但需验证全大写缩写（如 `PVC`）是否正确匹配
- [ ] 从标题/表格中提取简短例句（允许10-30字符）

---

## 问题2：领域分布严重偏斜

**现状**（由文本自然分布决定）：

| 领域 | 词数 | 占比 |
|------|------|------|
| physiology | 841 | 45.4% |
| cardiovascular | 316 | 17.1% |
| musculoskeletal | 201 | 10.8% |
| metabolism | 131 | 7.1% |
| fitness | 96 | 5.2% |
| assessment | 98 | 5.3% |
| prescription | 87 | 4.7% |
| rehabilitation | 83 | 4.5% |

**根因**：分类逻辑关键词偏向基础生理/心血管/肌肉骨骼，prescription/fitness/rehabilitation/assessment 的关键词在PDF文本中匹配度不足。大量术语被错误归类到physiology（默认兜底分类）。

**修复方案**：
- [ ] 重写分类逻辑：从"关键词包含"改为"精确领域关键词匹配 + 得分制"
- [ ] 增加prescription领域关键词：`preparticipation screening`、`risk stratification`、`contraindication`、`medical clearance`、`exercise prescription`、`fitt-vp` 等
- [ ] 增加fitness领域关键词：`health-related fitness`、`skill-related fitness`、`cardiorespiratory fitness`、`muscular endurance`、`muscular power` 等
- [ ] 增加rehabilitation领域关键词：`therapeutic exercise`、`return to play`、`cardiac rehabilitation`、`neuromuscular re-education` 等
- [ ] 增加assessment领域关键词：`fitness assessment`、`body composition assessment`、`vo2max test`、`1rm test`、`functional movement screen` 等
- [ ] 避免默认兜底到physiology：无明确领域匹配的术语应标记为`uncategorized`，而不是强制分到physiology

---

## 问题3：MUST_KEEP核心术语仍有336个未收录

**现状**：352/688已收录，336个未进入最终词库。

**根因**：
1. **词频过滤门槛过高**：很多核心术语在847页PDF中出现2-3次，被`freq >= 2`筛掉
2. **词形变体未合并**：
   - `1RM` vs `1-RM` vs `one-repetition maximum` vs `repetition maximum`
   - `BMI` vs `body mass index`
   - `VO2max` vs `VO2 max` vs `maximal oxygen uptake`
3. **复合词在文本中被空格拆分**：如 `blood flow restriction` 被拆成 `blood`、`flow`、`restriction` 三个独立单词

**修复方案**：
- [ ] 对MUST_KEEP列表中的词取消频率门槛（即使freq=1也收录）
- [ ] 词形归一化：建立变体映射表（`1RM` ↔ `1-RM` ↔ `one-repetition maximum`）
- [ ] 改进复合词提取：不仅要匹配完整短语，还要提取被拆分的N-gram组合
- [ ] 对MUST_KEEP中未收录的词做逐一排查，确认是遗漏还是确实不在文本中

---

## 问题4：缩写-全称对应质量不高

**现状**：56个映射，但部分匹配结果不干净。

**问题示例**：
- `PRISMA` → `ting items for systematic reviews and meta-analyses`（截断，缺少"Preferred repor"前缀）
- `HRR` → `of heart rate reserve`（缺少"percentage"前缀）
- `CDC` → `t` + `centers for disease control and prevention`（换行污染）
- `CAD` → `n pa and crf with risks for coronary artery disease`（上下文噪声）

**根因**：正则提取括号模式时，捕获了括号前的一个词（或半个词），而PDF换行符把单词切断了。

**修复方案**：
- [ ] 限制全称长度：捕获括号前的2-10个单词，而不是无限制长度
- [ ] 清理换行污染：对提取到的全称做换行符合并和空白规范化
- [ ] 验证映射：确保缩写对应的全称是合理的医学术语，不是随机片段
- [ ] 手动校对MUST_KEEP中的核心缩写映射（BMI、VO2max、ACSM等）

---

## 问题5：复合词/短语提取量可能不足

**现状**：205个复合词（182来自PDF2 + 23来自PDF1）。

**问题**：
- 短语列表PHRASE_PATTERNS是手动维护的MUST_KEEP子集，只包含带空格的复合词
- 未自动发现新的复合词：很多医学复合词不在MUST_KEEP列表中
- 3词及以上复合词完全未提取（如 `high-intensity interval training`、`functional electrical stimulation therapy`）

**修复方案**：
- [ ] 自动N-gram提取：从文本中自动发现高频2-gram、3-gram组合
- [ ] 医学复合词判定：使用POS模式（形容词+名词、名词+名词）识别潜在复合词
- [ ] 连字符复合词：`high-intensity`、`low-impact`、`non-functional` 等
- [ ] 括号复合词：`heart failure with reduced ejection fraction (HFrEF)`

---

## 问题6：中文翻译覆盖率不足

**现状**：TRANSLATIONS字典只覆盖约200个术语，大量术语仅有英文。

**影响**：用户在词库中看到纯英文术语，无中文释义。

**修复方案**：
- [ ] 批量机器翻译：调用翻译API对未覆盖术语自动翻译
- [ ] 人工校对：对运动科学核心术语的翻译准确性做领域专家审核
- [ ] 建立术语标准库：对齐ACSM官方中文译本、国内教材标准译名

---

## 问题7：翻译错误/领域误分类示例（需逐一修正）

| 术语 | 当前翻译/分类 | 问题 |
|------|--------------|------|
| `acc` | `[美国心脏病学会]` + 分类到physiology | 实际是缩写`ACC`，全称`American College of Cardiology`，不应作为独立单词收录；例句也不对 |
| `type` | `[类型]` + 分类到cardiovascular | `type`是通用词，不应收录 |
| `heat exhaustion` | `[heat exhaustion]`（英文重复） | 无中文翻译 |
| `exoskeleton` | `[exoskeleton]`（英文重复） | 无中文翻译 |
| `visual impairment` | `[视力障碍]` | 翻译正确，但例句来源是physiology章节，分类应为rehabilitation |
| `rct` | `[rct]` | 无中文翻译，应为`随机对照试验` |
| `rockport` | `[Rockport步行试验]` | 翻译正确，但分类需确认 |

**修复方案**：
- [ ] 清理通用词：`type`、`use`、`way` 等不应进入词库
- [ ] 清理纯英文重复翻译：无中文翻译的术语应标为`[待翻译]`而不是重复英文
- [ ] 修正误分类术语：逐条审核physiology领域的841个词，把明显不属于生理学的移出

---

## 优先级排序（建议修复顺序）

| 优先级 | 问题 | 影响 | 工作量 |
|--------|------|------|--------|
| 🔴 P0 | 通用词混入（`type`、`acc`等） | 词库质量硬伤 | 低（加黑名单） |
| 🔴 P0 | MUST_KEEP未收录336个 | 核心术语缺失 | 中（取消门槛+归一化） |
| 🟡 P1 | 无例句311个 | 用户体验 | 中（放宽匹配+缩写双向） |
| 🟡 P1 | 领域分布偏斜 | 分类准确性 | 中（重写分类逻辑） |
| 🟢 P2 | 缩写-全称质量 | 数据干净度 | 低（清理换行） |
| 🟢 P2 | 翻译覆盖率 | 中文用户体验 | 高（批量翻译+校对） |
| 🔵 P3 | 复合词自动发现 | 词汇丰富度 | 高（N-gram+POS） |

---

## 如何验证修复效果

每轮修复后检查以下指标：

```python
# 1. 总词数（当前1853）
# 2. MUST_KEEP覆盖率（当前352/688 = 51.2%，目标>90%）
# 3. 有例句比例（当前1542/1853 = 83.2%，目标>95%）
# 4. 无通用词（`type`、`use`、`way`、`acc` 等必须清零）
# 5. 各领域无默认兜底：physiology占比应<35%（当前45.4%）
# 6. 翻译覆盖率：有中文翻译的比例（当前~15%，目标>80%）
```

---

*本文件由阿木（秉木AI助手）于2026-04-29生成，用于追踪ACSM词库提取任务的技术债务。*
