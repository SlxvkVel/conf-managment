@echo off
echo Test 1: Minimal VFS
python src/vfs.py --vfs-path "data/minimal.vfs" --startup-script "scripts/test_commands.vfs"
pause