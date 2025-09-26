@echo off
echo Test 2: Multiple files VFS
python src/vfs.py --vfs-path "data/files.vfs" --startup-script "scripts/test_commands.vfs"
pause