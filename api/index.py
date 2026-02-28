import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

print("="*50)
print("开始加载应用...")
print("="*50)

try:
    from app.main import app
    print(f"应用加载成功: {app}")
except Exception as e:
    print(f"加载应用时出错: {e}")
    import traceback
    traceback.print_exc()

print("="*50)
print("设置 handler...")
print("="*50)

handler = app
