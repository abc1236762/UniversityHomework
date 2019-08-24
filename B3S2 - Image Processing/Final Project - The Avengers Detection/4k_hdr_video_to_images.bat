@echo off
rem usage: 4k_hdr_video_to_images.cmd <video file> <output dir> <per seconds>
ffmpeg -i %1 -vf zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p,fps=1/%3 -crf 18 %2/%%08d.jpg
pause
