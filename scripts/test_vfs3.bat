@echo off
echo Test 3: Complex structure VFS
python src/vfs.py --vfs-path "data/complex_structure.vfs" --startup-script "scripts/test_commands.vfs"
pause