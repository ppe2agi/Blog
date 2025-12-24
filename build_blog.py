import os
from pathlib import Path
from datetime import datetime

# === 配置 ===
current_date = datetime.now().strftime('%Y-%m-%d %H:%M')
author_info = "made by chanvel"
source_dir = Path('python')

def build():
    # 1. 确保目录存在
    source_dir.mkdir(exist_ok=True)

    # 2. 获取所有 .py 文件
    py_files = sorted(list(source_dir.glob('*.py')))
    
    # 3. 核心：生成 python/README.md (整合所有源码)
    with open(source_dir / 'README.md', 'w', encoding='utf-8') as f:
        f.write(f"# 🐍 Python 源码整合详情\n\n")
        f.write(f"在本页你可以直接查阅 `python/` 目录下的所有案例代码。\n\n")
        f.write(f"[⬅️ 返回首页](../README.md)\n\n---\n\n")
        
        if not py_files:
            f.write("> 📂 暂无代码文件。\n")
        else:
            # 遍历并整合每个文件内容
            for py_file in py_files:
                # 排除 README.md 本身（虽然 glob('*.py') 已经排除了）
                content = py_file.read_text(encoding='utf-8')
                
                f.write(f"## 📄 案例：{py_file.name}\n\n")
                f.write(f"```python\n{content}\n```\n\n")
                f.write(f"---\n\n") # 分割线

    # 4. 生成根目录 README.md (作为导航)
    root_content = [
        f"<sub>{author_info} | 更新时间: {current_date}</sub>\n",
        "# 🚀 自动化代码库",
        f"- [👉 点击进入 Python 源码详情页](./python/README.md) —— 已整合 {len(py_files)} 个案例"
    ]
    Path('README.md').write_text('\n'.join(root_content), encoding='utf-8')

if __name__ == "__main__":
    build()
    print(f"✅ 整合完成！已将 {len(list(source_dir.glob('*.py')))} 个文件写入 python/README.md")
