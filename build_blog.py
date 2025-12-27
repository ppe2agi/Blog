import re
from pathlib import Path
from datetime import datetime

# --- 配置 ---
# 获取当前时间
NOW = datetime.now().strftime('%Y-%m-%d %H:%M')
SRC, ROOT_MD, SRC_MD = Path('python'), Path('README.md'), Path('python/README.md')
CN_MAP = {c: i for i, c in enumerate('一二三四五六七八九十', 1)}

def get_sort_key(p):
    name = p.stem
    m = re.match(r'^(\d+|[一二三四五六七八九十])', name)
    
    # 元组第一位决定大类：
    # -1: 包含“序”的文件 (最高)
    #  0: 带数字/中文序号的文件 (中等)
    #  1: 普通文件 (最低)    
    if "序" in name: return (-1, name)
    if not m: return (1, name)
    
    val = m.group(1)
    return (0, int(val) if val.isdigit() else CN_MAP.get(val, 99))

def process_py(p):
    """提取注释与代码块"""
    content, code_acc = [], []
    def flush():
        if code_acc and any(l.strip() for l in code_acc):
            # 修正：在代码块前后强制添加空行
            content.append("") 
            content.append("```python")
            content.extend(code_acc)
            content.append("```")
            content.append("")
        code_acc.clear()

    for line in p.read_text(encoding='utf-8', errors='replace').splitlines():
        m = re.match(r'^\s*#\s?(.*)', line)
        if m:
            flush()
            # 修正：确保注释行也是独立的段落
            content.append(m.group(1).strip())
            content.append("") 
        elif not line.strip():
            flush()
            content.append("")
        else:
            code_acc.append(line)
    flush()
    return "\n".join(content)

def build():
    SRC.mkdir(exist_ok=True)
    # 保持原有的 glob 和排序
    py_files = sorted(SRC.glob('*.py'), key=get_sort_key)
    
    # 修改页脚样式
    footer = [f"\n---\nmade by chanvel   |   {NOW}"]
    
    # 1. 详情页 (python/README.md)
    sub_body = [f"[源代码汇总](../README.md)\n"]
    
    for py in py_files:
        # --- 核心修正点：确保标题前后有足够的换行符 ---
        # 原代码 sub_body.extend([f"### {py.stem}", process_py(py)]) 
        # 容易导致标题和内容粘在一起，Markdown 无法识别
        sub_body.append(f"\n---\n") # 添加分割线更清晰
        sub_body.append(f"### {py.stem}\n") # 标题后加换行
        sub_body.append(process_py(py))
        # ------------------------------------------

    SRC_MD.write_text("\n".join(sub_body + footer), encoding='utf-8')

    # 2. 主页 (README.md)
    root_body = [f"[Python源代码](./python/README.md)"]
    ROOT_MD.write_text("\n".join(root_body + footer), encoding='utf-8')

if __name__ == "__main__":
    build()
    print(f"✨ 构建成功！已调整换行逻辑，防止内容合并。")