#!/usr/bin/env python3
# 合并 generate_vocab2.py 的 supplement 到 generate_vocab.py

with open("/root/.openclaw/workspace/vocabulary-builder/generate_vocab.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# 找到 all_words 定义行
idx = None
for i, line in enumerate(lines):
    if line.strip().startswith("all_words = physiology + anatomy + cardio + prescription + fitness + nutrition + rehab + biomech"):
        idx = i
        break

if idx is None:
    print("未找到 all_words 定义行")
    exit(1)

# 读取 supplement 定义（去掉最后一行 all_words 定义）
with open("/root/.openclaw/workspace/vocabulary-builder/generate_vocab2.py", "r", encoding="utf-8") as f:
    v2_lines = f.readlines()

# 找到 supplement 定义起始行
start_idx = None
for i, line in enumerate(v2_lines):
    if "supplement = [" in line:
        start_idx = i
        break

# 找到 supplement 定义结束行（] 行）
end_idx = None
for i in range(len(v2_lines)-1, -1, -1):
    if v2_lines[i].strip() == "]":
        end_idx = i
        break

if start_idx is None or end_idx is None:
    print("未找到 supplement 定义")
    exit(1)

supplement_block = v2_lines[start_idx:end_idx+1]

# 在 all_words 行前插入 supplement 定义
new_lines = lines[:idx] + supplement_block + ["\n"] + [lines[idx].replace("biomech", "biomech + supplement")]
new_lines += lines[idx+1:]

with open("/root/.openclaw/workspace/vocabulary-builder/generate_vocab.py", "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print(f"修改完成，在 {idx} 行前插入 supplement ({len(supplement_block)} 行)")
print(f"all_words 已更新为: {new_lines[idx + len(supplement_block) + 1].strip()}")
