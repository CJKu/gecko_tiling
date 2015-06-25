
1. Enable tiling log.
   https://dxr.mozilla.org/mozilla-central/source/gfx/layers/TiledLayerBuffer.h#37
2. Dump tiling log to a file
   $ adb logcat | grep TILING > sample2.txt
   ^C
3. Parse tiling log
   $python logparser.py sample2.txt
