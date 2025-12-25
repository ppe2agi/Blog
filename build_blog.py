import re
from pathlib import Path
from datetime import datetime

# --- 配置 ---
NOW = datetime.now().strftime('%Y-%m-%d %H:%M')
SRC, ROOT_MD, SRC_MD = Path('python'), Path('README.md'), Path('python/README.md')
CN_MAP = {c: i for i, c in enumerate('一二三四五六七八九十', 1)}

def get_sort_key(p):
    """提取开头数字或中文数字进行排序，其余按原名"""
    m = re.match(r'^(\d+|[一二三四五六七八九十])', p.stem)
    if not m: return (1, p.stem)
    val = m.group(1)
    return (0, int(val) if val.isdigit() else CN_MAP.get(val, 99))

def process_py(p):
    """提取注释为文本，代码存入块"""
    content, code_acc = [], []
    def flush():
        if code_acc:
            if any(l.strip() for l in code_acc):
                content.extend(["\n```python", *code_acc, "```\n"])
            code_acc.clear()

    for line in p.read_text(encoding='utf-8', errors='replace').splitlines():
        m = re.match(r'^\s*#\s?(.*)', line)
        if m:
            flush()
            content.append(m.group(1) or "\n")
        elif not line.strip():
            flush()
            content.append("")
        else:
            code_acc.append(line)
    flush()
    return "\n".join(content)

def build():
    SRC.mkdir(exist_ok=True)
    py_files = sorted(SRC.glob('*.py'), key=get_sort_key)
    footer = [f"\n---\n更新时间: {NOW}  ", "made by **chanvel**"]
    
    # 生成详情页
    sub_body = ["---", "layout: default", "---", "\n[⬅️ 返回主页](../README.md)\n"]
    for py in py_files:
        sub_body.extend([f"### 📄 {py.stem}", process_py(py), "\n---"])
    SRC_MD.write_text("\n".join(sub_body + footer), encoding='utf-8')

    # 生成主页
    root_links = [f"- [{p.stem}](./python/README.md#{p.stem.lower().replace(' ', '-').replace('、', '')})" for p in py_files]
    root_body = ["---", "layout: default", "---", "\n## 📚 脚本索引\n"] + root_links + [f"\n- [📂 源码目录](./python/README.md) ({len(py_files)})"]
    ROOT_MD.write_text("\n".join(root_body + footer), encoding='utf-8')

if __name__ == "__main__":
    build()
    print(f"✨ 已完成 {len(list(SRC.glob('*.py')))} 个文件的同步")