@echo off
echo Test 3: Deep structure VFS
python src/vfs.py --vfs-path "data/deep.vfs" --startup-script "scripts/test_commands.vfs"
pause