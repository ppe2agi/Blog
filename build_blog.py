import os
from datetime import datetime

# === 配置信息 ===
current_date = datetime.now().strftime('%Y-%m-%d')
author_info = "made by chanvel"
# 你设定的新标题
project_title = "知行合一" 
# 你的自定义域名
domain_name = "blog.ppe2agi.qzz.io"

# 0. 在根目录生成 CNAME 文件 (确保自定义域名生效)
with open('CNAME', 'w', encoding='utf-8') as f:
    f.write(domain_name)

# 1. 生成根目录的总 README.md
with open('README.md', 'w', encoding='utf-8') as f:
    # 写入一级标题，这将作为网页的主标题
    f.write(f"# {project_title}\n\n")
    # 副标题使用浅灰色
    f.write(f"<sub><font color='#888'>{author_info} | 最近更新: {current_date}</font></sub>\n\n")
    f.write("---\n\n")
    f.write("- [🤔 Python 语言](./python/README.md)\n")

# 2. 生成子目录的内容
if not os.path.exists('python'):
    os.makedirs('python')

with open('python/README.md', 'w', encoding='utf-8') as f:
    f.write(f"# 🤔 Python 语言\n")
    f.write(f"<sub><font color='#888'>{author_info}</font></sub>\n\n")
    f.write("这里记录了从 .py 文件中自动提取的源码和案例。\n\n---\n\n")
    
    # 过滤出 python 文件夹下的所有 .py 文件
    files = [file for file in os.listdir('python') if file.endswith('.py')]
    
    if not files:
        f.write("目前该分类下暂无代码文件。\n")
    else:
        for file in files:
            file_path = os.path.join('python', file)
            f.write(f"### 📄 文件名: {file}\n\n")
            with open(file_path, 'r', encoding='utf-8') as py_content:
                f.write("```python\n" + py_content.read() + "\n```\n\n---\n\n")

print(f"✅ 执行完成：")
print(f"   - 已确保 CNAME 存在 ({domain_name})")
print(f"   - 已更新主页标题为：{project_title}")
print(f"   - 更新日期：{current_date}")