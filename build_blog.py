import os
from datetime import datetime

# 获取当前日期
current_date = datetime.now().strftime('%Y-%m-%d')
author_info = "made by chanvel"

# 1. 生成根目录的总 README.md
with open('README.md', 'w', encoding='utf-8') as f:
    # 使用 # 开启标题，紧接着用 <br> 换行，并用 <sub> 包裹副标题内容
    # 这样它们在视觉上属于同一个标题块，但在物理上是两行
    f.write(f"# 技术博客总入口<br><sub>{author_info} | 最近更新: {current_date}</sub>\n\n")
    
    f.write("## 学习分类\n")
    f.write("- [🐍 Python 语言学习](./python/README.md)\n")

# 2. 生成子目录的子 README.md
if not os.path.exists('python'):
    os.makedirs('python')

with open('python/README.md', 'w', encoding='utf-8') as f:
    # 子目录也保持统一的排版风格
    f.write(f"# 🐍 Python 学习笔记<br><sub>{author_info}</sub>\n\n")
    f.write("这里记录了从 .py 文件中自动提取的详细源码和案例。\n\n---\n\n")
    
    # 遍历文件
    files = [file for file in os.listdir('python') if file.endswith('.py')]
    
    if not files:
        f.write("目前该分类下暂无代码文件。\n")
    else:
        for file in files:
            file_path = os.path.join('python', file)
            f.write(f"### 📄 文件名: {file}\n\n")
            with open(file_path, 'r', encoding='utf-8') as py_file:
                f.write("```python\n" + py_file.read() + "\n```\n\n---\n\n")

print(f"✅ 样式已优化：副标题已移至标题下方（小字号），更新日期：{current_date}")