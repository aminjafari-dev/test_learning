from pathlib import Path

path = Path("email")
path1 = Path()

if(path.exists()):

    path.rmdir()
else:
    path.mkdir()

for file in path1.glob('*.py'):
    print(file)

