def build_outline_tree(outline_list):
    """将平铺的outline转换为树状结构"""
    if not outline_list:
        return []
    
    tree = []
    stack = []  # 用于跟踪父级节点的栈
    
    for item in outline_list:
        node = {
            "id": item["id"],
            "text": item["text"],
            "level": item["level"],
            "style": item["style"],
            "children": []
        }
        
        # 找到正确的父级位置
        while stack and stack[-1]["level"] >= node["level"]:
            stack.pop()
        
        if not stack:
            # 根级节点
            tree.append(node)
        else:
            # 添加到父节点的children中
            stack[-1]["children"].append(node)
        
        # 将当前节点加入栈
        stack.append(node)
    
    return tree
