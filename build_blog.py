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
    """处理Python内容：注释转文字，代码留框"""
    lines = file_path.read_text(encoding='utf-8', errors='replace').splitlines()
    processed_parts = []
    current_code_block = []

    def flush_code():
        if current_code_block:
            processed_parts.append('<div style="white-space: pre-wrap; word-wrap: break-word;">\n')
            processed_parts.append(f"```python\n" + "\n".join(current_code_block) + "\n```")
            processed_parts.append('</div>\n')
            current_code_block.clear()

    for line in lines:
        stripped = line.strip()
        # 识别以 # 开头的注释行
        if stripped.startswith('#'):
            flush_code()  # 先把之前的代码块存起来
            # 去掉开头的 # 和随后的空格
            md_text = re.sub(r'^#\s*', '', line)
            processed_parts.append(f"{md_text}  ") # Markdown 换行需两个空格
        else:
            current_code_block.append(line)
            
    flush_code() # 处理最后剩余的代码
    return "\n".join(processed_parts)

def build():
    if not SRC.exists():
        SRC.mkdir(exist_ok=True)
        return

    py_files = sorted(SRC.glob('*.py'))
    
    common_footer = [
        "\n---", 
        f"更新时间: {NOW}  ",
        "made by **chanvel**"
    ]
    
    # --- 1. 生成 python/README.md ---
    markdown_segments = [
        f"# 🤔 Python 源码汇总\n",
        f"[⬅️ 返回首页](../README.md)\n",
    ]

    for py in py_files:
        try:
            markdown_segments.append(f"### 📄 {py.name}\n")
            # 调用新逻辑处理内容
            markdown_segments.append(process_py_content(py))
            markdown_segments.append("\n---\n")
        except Exception as e:
            print(f"❌ 读取 {py.name} 失败: {e}")
    
    markdown_segments.extend(common_footer)
    SRC_MD.write_text('\n'.join(markdown_segments), encoding='utf-8')

    # --- 2. 生成根目录 README.md ---
    root_content = [
        "### 🚀 代码库主页\n",
        f"- [📁 Python 源码详情](./python/README.md) ({len(py_files)} 个案例文件)\n",
    ] + common_footer
    
    ROOT_MD.write_text('\n'.join(root_content), encoding='utf-8')

if __name__ == "__main__":
    build()
    print(f"✅ 构建完成！注释已转为文档说明。")