import re
from pathlib import Path
from datetime import datetime

# --- 配置 ---
NOW = datetime.now().strftime('%Y-%m-%d %H:%M')
SRC, ROOT_MD, SRC_MD = Path('python'), Path('README.md'), Path('python/README.md')
CN_MAP = {c: i for i, c in enumerate('一二三四五六七八九十', 1)}

def get_sort_key(p):
    name = p.stem
    if "序" in name: return (-1, name)
    m = re.match(r'^(\d+|[一二三四五六七八九十])', name)
    if not m: return (1, name)
    val = m.group(1)
    return (0, int(val) if val.isdigit() else CN_MAP.get(val, 99))

def process_py(p):
    content, code_acc = [], []
    def flush():
        if code_acc and any(l.strip() for l in code_acc):
            content.append(f"\n```python\n" + "\n".join(code_acc).strip() + "\n```\n")
        code_acc.clear()

    for line in p.read_text(encoding='utf-8').splitlines():
        m = re.match(r'^\s*#\s?(.*)', line)
        if m:
            flush()
            # 1. 彻底清除行首空格，解决【汉诺塔】等块的幽灵缩进
            text = m.group(1).lstrip()
            
            # 2. 核心修复：处理多级序号（如 4.3.2）
            # 将所有点号替换为 HTML 实体 &#46; 彻底切断 GitHub 的自动列表逻辑
            # 这样既不会出现 3\、 乱码，也能保证文字绝对顶格
            if re.match(r'^\d', text):
                text = text.replace('.', '&#46;')
            
            content.append(f"{text}<br>")
        elif not line.strip():
            flush(); content.append("<br>")
        else:
            code_acc.append(line)
            
    flush()
    return "\n".join(content)

def build():
    SRC.mkdir(exist_ok=True)
    py_files = sorted(SRC.glob('*.py'), key=get_sort_key)
    footer = [f"\n---\nmade by chanvel   |   {NOW}"]
    
    sub_body = ["[源代码汇总](../README.md)\n"]
    for py in py_files:
        sub_body.extend([f"### {py.stem}", process_py(py)])
    
    # 写入文件，确保编码统一
    SRC_MD.write_text("\n".join(sub_body + footer), encoding='utf-8')
    ROOT_MD.write_text("\n".join([f"[Python源代码](./python/README.md)"] + footer), encoding='utf-8')

if __name__ == "__main__":
    build()
    print(f"✨ 构建完成：已修复多级序号缩进，确保 Page 渲染与源码一致。")