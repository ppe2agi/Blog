import os
from pathlib import Path
from datetime import datetime
import re

# --- 配置 ---
NOW = datetime.now().strftime('%Y-%m-%d %H:%M')
SRC = Path('python')
ROOT_MD = Path('README.md')
SRC_MD = SRC / 'README.md'

def process_py_content(file_path):
    """提取 Python 文件内容并转换为 Markdown"""
    lines = file_path.read_text(encoding='utf-8', errors='replace').splitlines()
    processed_parts = []
    current_code_block = []

    def flush_code():
        if current_code_block:
            if any(line.strip() for line in current_code_block):
                processed_parts.append("\n```python")
                processed_parts.extend(current_code_block)
                processed_parts.append("```\n")
            current_code_block.clear()

    for line in lines:
        comment_match = re.match(r'^\s*#\s?(.*)', line)
        if comment_match:
            flush_code()
            content = comment_match.group(1)
            processed_parts.append(content if content.strip() else "\n")
        elif not line.strip():
            flush_code()
            processed_parts.append("") 
        else:
            current_code_block.append(line)
            
    flush_code()
    return "\n".join(processed_parts)

def build():
    if not SRC.exists():
        SRC.mkdir(exist_ok=True)
        return

    py_files = sorted(SRC.glob('*.py'))
    
    # 定义通用的页脚
    common_footer = [
        "\n<br>\n",
        "---",
        f"**更新时间:** {NOW}  ",
        "made by **chanvel**"
    ]
    
    # --- 1. 生成 python/README.md ---
    # 第一个一级标题会被 Cayman 抓取到顶部背景中
    sub_md = [
        "# Python 源代码详情\n", 
        f"[⬅️ 返回首页](../README.md)\n",
    ]

    for py in py_files:
        try:
            # 文件名使用二级标题 (##)，它会留在白色正文区
            sub_md.append(f"## 📄 {py.name}\n")
            sub_md.append(process_py_content(py))
            print(f"✅ 已同步: {py.name}")
        except Exception as e:
            print(f"❌ 错误: {e}")
    
    sub_md.extend(common_footer)
    SRC_MD.write_text('\n'.join(sub_md), encoding='utf-8')

    # --- 2. 生成根目录 README.md ---
    # 第一个一级标题会被 Cayman 抓取到顶部背景中
    root_md = [
        "# 源代码主页\n",
        "### 📂 项目目录",
        f"- [📁 点击进入 Python 源代码仓库](./python/README.md) ({len(py_files)} 个案例文件)",
    ] + common_footer
    
    ROOT_MD.write_text('\n'.join(root_md), encoding='utf-8')

if __name__ == "__main__":
    build()
    print("\n✨ 构建完成！请推送到 GitHub 并在 Settings 中确保主题为 Cayman。")