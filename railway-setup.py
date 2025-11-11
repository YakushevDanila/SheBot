import os

print("=== DIAGNOSTIC INFORMATION ===")
print("Current directory:", os.getcwd())
print("\nFiles and folders in root:")
for item in sorted(os.listdir('.')):
    print(f" - {item}")

print("\nLooking for main.py...")
if os.path.exists('main.py'):
    print("✅ main.py found in root")
elif os.path.exists('bot/main.py'):
    print("✅ main.py found in bot/ folder")
else:
    print("❌ main.py not found anywhere")

print("\nFull structure:")
for root, dirs, files in os.walk('.'):
    level = root.replace('.', '').count(os.sep)
    indent = ' ' * 2 * level
    print(f"{indent}{os.path.basename(root)}/")
    subindent = ' ' * 2 * (level + 1)
    for file in files:
        if file.endswith('.py') or file in ['Procfile', 'requirements.txt']:
            print(f"{subindent}{file}")
