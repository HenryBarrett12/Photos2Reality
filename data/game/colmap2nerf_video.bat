@setlocal enableextensions
@cd /d "%~dp0"

python ./../../../scripts/colmap2nerf.py --video_in images/video.mp4 --video_fps 1 --run_colmap --aabb_scale 16
pause