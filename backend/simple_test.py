#!/usr/bin/env python3
"""
简化的API测试脚本
"""

import requests
import time

def test_connection():
    """测试服务器连接"""
    print("🔍 测试服务器连接...")
    
    try:
        # 测试根路径
        response = requests.get("http://127.0.0.1:8000/", timeout=5)
        print(f"✅ 根路径响应: {response.status_code}")
        print(f"   内容: {response.text[:100]}")
        
        # 测试API文档
        response = requests.get("http://127.0.0.1:8000/docs", timeout=5)
        print(f"✅ 文档页面响应: {response.status_code}")
        
        # 测试API端点
        response = requests.get("http://127.0.0.1:8000/api/v1/", timeout=5)
        print(f"✅ API根路径响应: {response.status_code}")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器")
        return False
    except Exception as e:
        print(f"❌ 连接测试失败: {e}")
        return False

def test_auth_endpoints():
    """测试认证端点"""
    print("\n🔐 测试认证端点...")
    
    try:
        # 测试注册端点
        test_user = {
            "username": "testuser",
            "password": "password123",
            "name": "测试用户",
            "role": "student"
        }
        
        response = requests.post("http://127.0.0.1:8000/api/v1/auth/register", json=test_user, timeout=10)
        print(f"✅ 注册端点响应: {response.status_code}")
        if response.status_code == 200:
            print(f"   注册成功: {response.json()}")
        else:
            print(f"   注册失败: {response.text}")
        
        # 测试登录端点
        login_data = {
            "username": "testuser",
            "password": "password123"
        }
        
        response = requests.post("http://127.0.0.1:8000/api/v1/auth/login", data=login_data, timeout=10)
        print(f"✅ 登录端点响应: {response.status_code}")
        if response.status_code == 200:
            token = response.json()["access_token"]
            print(f"   登录成功，Token: {token[:20]}...")
            return token
        else:
            print(f"   登录失败: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ 认证测试失败: {e}")
        return None

def test_submission_endpoints(token):
    """测试提交端点"""
    if not token:
        print("❌ 没有有效Token，跳过提交测试")
        return
        
    print("\n📝 测试提交端点...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        # 测试查看我的提交
        response = requests.get("http://127.0.0.1:8000/api/v1/submissions/my-submissions", headers=headers, timeout=10)
        print(f"✅ 查看我的提交: {response.status_code}")
        if response.status_code == 200:
            print(f"   提交数量: {len(response.json())}")
        
        # 测试查看待提交任务
        response = requests.get("http://127.0.0.1:8000/api/v1/submissions/my-submissions/pending", headers=headers, timeout=10)
        print(f"✅ 查看待提交任务: {response.status_code}")
        if response.status_code == 200:
            print(f"   待提交任务数量: {len(response.json())}")
            
    except Exception as e:
        print(f"❌ 提交测试失败: {e}")

if __name__ == "__main__":
    print("🚀 开始简化API测试")
    print("=" * 40)
    
    # 等待服务器启动
    print("⏳ 等待服务器启动...")
    time.sleep(3)
    
    # 测试连接
    if test_connection():
        # 测试认证
        token = test_auth_endpoints()
        
        # 测试提交
        test_submission_endpoints(token)
    
    print("\n🎉 测试完成！")
