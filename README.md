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
  
Factorio! (The default expected input is a sequence of 0000.png to 9999.png.)  
  
D:\GAME／W7F\blender\blender-eradication-logo\anim>p make_optimized_sprite_sheet.py -o foxdamage --extra "-resize 96x" -y -h  
Factorio Compressed Sprite Sheet Maker (v1.0)  
  
usage: make_optimized_sprite_sheet.py [-y] [-i IN_FILE_PATTERN]  
                                      [-o OUT_FILE_PREFIX] [--extra "OPTIONS"]  
                                      [-v] [-a] [-w WIDTH] [-h HEIGHT]  
                                      [--help] [-s IN_FILE_NAME] [--nosample]  
make_optimized_sprite_sheet.py: error: argument -h/--height: expected one argument  
Use --help for help.  
