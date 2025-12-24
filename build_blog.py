import os
from datetime import datetime

# === 1. 配置信息 ===
current_date = datetime.now().strftime('%Y-%m-%d')
author_info = "made by chanvel"
domain_name = "blog.ppe2agi.qzz.io"

# 确保 docs 目录存在
if not os.path.exists('docs'):
    os.makedirs('docs')
if not os.path.exists('docs/python'):
    os.makedirs('docs/python')

# === 2. 在 docs 目录生成 CNAME (MkDocs 会将其构建到站点根目录) ===
with open('docs/CNAME', 'w', encoding='utf-8') as f:
    f.write(domain_name)

# === 3. 生成主页 (index.md 对应你原来的 README) ===
with open('docs/index.md', 'w', encoding='utf-8') as f:
    f.write(f"<sub><font color='#888'>{author_info} | 最近更新: {current_date}</font></sub>\n\n")
    f.write("- [🤔 Python 语言](./python/index.md)\n")

# === 4. 生成子目录的内容 ===
# 注意：MkDocs 中子目录的默认页应命名为 index.md
with open('docs/python/index.md', 'w', encoding='utf-8') as f:
    f.write(f"# 🤔 Python 语言\n")
    f.write(f"<sub><font color='#888'>{author_info}</font></sub>\n\n")
    f.write("这里记录了从 .py 文件中自动提取的源码和案例。\n\n---\n\n")
    
    # 注意：源码文件依然在项目根目录的 python/ 文件夹下
    source_dir = 'python' 
    if os.path.exists(source_dir):
        files = [file for file in os.listdir(source_dir) if file.endswith('.py')]
        if not files:
            f.write("目前该分类下暂无代码文件。\n")
        else:
            for file in files:
                file_path = os.path.join(source_dir, file)
                f.write(f"### 📄 文件名: {file}\n\n")
                with open(file_path, 'r', encoding='utf-8') as py_content:
                    f.write("```python\n" + py_content.read() + "\n```\n\n---\n\n")

print(f"✅ 执行完成：MkDocs 结构已生成。")
