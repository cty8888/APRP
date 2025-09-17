from docx import Document
from app.utils.outline_utils import build_outline_tree

def parse_docx(file):
    """解析docx文件，提取文本内容和结构信息"""
    docx = Document(file)
    results = {
        "total_words_count": 0,
        "paragraph_count": 0,
        "paragraphs": [],
        "outline": []
    }
    
    for id, para in enumerate(docx.paragraphs):
        text = para.text.strip()  # 去掉段落两端的空白字符
        if not text:
            continue
        word_count = len(text.replace(" ", ""))  # 去掉空格后的字符数
        
        results["paragraphs"].append({
            "id": id,
            "text": text,
            "word_count": word_count
        })
        results["total_words_count"] += word_count
        results["paragraph_count"] += 1
        
        if para.style.name.startswith("Heading") or para.style.name == "Title":
            # 提取标题级别
            level = 0
            if para.style.name == "Title":
                level = 0
            elif para.style.name.startswith("Heading"):
                try:
                    level = int(para.style.name.split()[-1])
                except:
                    level = 1
            
            results["outline"].append({
                "id": id,
                "text": text,
                "level": level,
                "style": para.style.name
            })
    
    # 转换outline为树状结构
    results["outline_tree"] = build_outline_tree(results["outline"])
    return results
