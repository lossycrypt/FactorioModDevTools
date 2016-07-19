# FactorioModDevTools
A collection of small scripts to aid factorio mod making.  


### Factorio Optimized Sprite Sheet Maker (v1.0)  

usage: make_optimized_sprite_sheet.py [-y] [-i IN_FILE_PATTERN]  
                                      [-o OUT_FILE_PREFIX] [--extra "OPTIONS"]  
                                      [-v] [-a] [-w WIDTH] [-h HEIGHT]  
                                      [--help] [-s IN_FILE_NAME] [--nosample]  

Crunches a sequence of images into sprite sheets via the following steps: 1)  
Trim transparent edges to minimize size. 2) Apply resize and/or other extra  
options. 3) Determine minimum number of sprite sheets required. 3) Determine  
optimal columns : rows ratio to minimize wasted space. 4) Attempt to make the  
sprite sheets square-like if possible without wasting space. 5) ??? 6) Profit  

optional arguments:  
  -y, --yes, -z, --zes  skips the user prompt.  
  -i IN_FILE_PATTERN    the pattern is passed to montage to determine input  
                        files. (default: 0*.png)  
  -o OUT_FILE_PREFIX    output files will be prefixed with this (postfix:  
                        "<x-resolution>x<y-resolution>_<columns>x<rows>")  
  --extra "OPTIONS"     extra options passed directly to imagemagick after  
                        trimming (i.e. "-resize <X>x<Y>")  
  -v, --version         show program's version number and exit  
  -a, --auto            automatic mode with default settings.  
  -w WIDTH, --width WIDTH  
                        maximum width of one sprite sheet (default: 2048)  
  -h HEIGHT, --height HEIGHT  
                        maximum height of one sprite sheet (default: 2048)  
  --help                show this help message and exit  
  -s IN_FILE_NAME, --sample IN_FILE_NAME  
                        additionally creates a sample frame that can be used  
                        to determine shift values later. (default: 0000.png)  
  --nosample            disable creation of the sample frame.  
  
Factorio! (The default expected input is a sequence of 0000.png to 0999.png.)  


### Factorio Sprite Shift Calculator

usage: factorio_sprite_shift_calculator.py <width> <height> <center x> <center y> <scale>

<width>    <height>   Total width and height of the frame. (1-indexed)
<center x> <center y> Desired center point of the shifted frame. (0-indexed)
<scale>               The scaling factor if any because shift is applied after scale
                      by factorio. (default: 1.0)

Remember that the real center of an even-numbered width/height frame is _between_
two rows of pixels. I.e. the center of a 64x64 frame is 31.5/31.5 . So usually the
center point you want, will be half a pixel less (-0.5) than what your program shows
you.

Output: The required shift and approximate collision and selection boxes, preformatted
as commented lua code. Also automatically copied to clipboard if you're on windows.

Example:
```batch
python factorio_sprite_shift_calculator.py 96 91 32.5 33.5 1.5
```
```lua
selection_box = { { -1.49, -1.35 }, { 1.49, 1.35 } }, -- actual selection box
collision_box = { { -1.39, -1.25 }, { 1.39, 1.25 } }, -- actual collision box
selection_box = { { -1.42, -1.42 }, { 1.42, 1.42 } }, -- square selection box
collision_box = { { -1.32, -1.32 }, { 1.32, 1.32 } }, -- square collision box
shift         = { 0.7109375, 0.546875 }, -- 96x91 x=32.5 y=33.5 s=1.5
scale         = 1.5,
```