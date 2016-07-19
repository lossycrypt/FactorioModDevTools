# Crunches a sequence of images into sprite sheets via the following steps:
# 1) Trim transparent edges to minimize size.
# 2) Apply resize and/or other extra options.
# 3) Determine minimum number of sprite sheets required.
# 3) Determine optimal columns : rows ratio to minimize wasted space.
# 4) Attempt to make the sprite sheets square-like if possible without wasting space.
# 5) ???
# 6) Profit
#
# license: no license
#
# dependency: imagemagick
#
# usage: see --help

import os, sys
import re, math
import operator
import argparse

# start
print( 'Factorio Optimized Sprite Sheet Maker (v1.0)\n' )

def error(*args, **kwargs): # http://stackoverflow.com/questions/5574702/how-to-print-to-stderr-in-python
    print(*args, file=sys.stderr, **kwargs)

# environment verification
has_convert = re.findall(r'ImageMagick',os.popen(r'convert -version').read())
has_montage = re.findall(r'ImageMagick',os.popen(r'montage -version').read())
has_mogrify = re.findall(r'ImageMagick',os.popen(r'mogrify -version').read())
if not has_convert or not has_montage or not has_mogrify:
    error('Error: Could not find ImageMagick. If you think it is installed check your path.')
    exit(2)

# argument parsing
parser = argparse.ArgumentParser(add_help = False)
#parser.add_help = False # used for short --height
parser.add_argument('-y','--yes','-z','--zes',dest='yes',action='store_true',default=False,
                  help='skips the user prompt.')
parser.add_argument('-i',dest='infilepattern',metavar='IN_FILE_PATTERN',default='0*.png',
                  help='the pattern is passed to montage to determine input files. (default: 0*.png)')
parser.add_argument('-o',dest='outfileprefix',metavar='OUT_FILE_PREFIX',default='',
                  help='output files will be prefixed with this (postfix: "<x-resolution>x<y-resolution>_<columns>x<rows>")')
parser.add_argument('--extra',metavar='"OPTIONS"',default='',
                  help='extra options passed directly to imagemagick after trimming (i.e. "-resize <X>x<Y>")')
parser.add_argument('-v','--version',action='version',version='1.0')
parser.add_argument('-a','--auto',action='store_true',default=True # dummy argument used in combination with  len(sys.argv) == 1 to prevent running without any args.
                    ,help='automatic mode with default settings.')
parser.add_argument('-w','--width',help='maximum width of one sprite sheet (default: 2048)',default=2048)
parser.add_argument('-h','--height',help='maximum height of one sprite sheet (default: 2048)',default=2048)
parser.add_argument('--help',action='store_true',default=False,help='show this help message and exit')
parser.add_argument('-s','--sample',default='0000.png',metavar='IN_FILE_NAME',help='additionally creates a sample frame that can be used to determine shift values later. (default: 0000.png)')
parser.add_argument('--nosample',action='store_true',default=False,help='disable creation of the sample frame.')

parser.description = ( 'Crunches a sequence of images into sprite sheets via the following steps:'
                      +'\n1) Trim transparent edges to minimize size.'
                      +'\n2) Apply resize and/or other extra options.'
                      +'\n3) Determine minimum number of sprite sheets required.'
                      +'\n3) Determine optimal columns : rows ratio to minimize wasted space.'
                      +'\n4) Attempt to make the sprite sheets square-like if possible without wasting space.'
                      +'\n5) ???'
                      +'\n6) Profit'
                     )

parser.epilog = 'Factorio! (The default expected input is a sequence of 0000.png to 9999.png.)'

try:
    args = parser.parse_args()
except:
    print('Use --help for help.')
    exit(1)

#print(args) ; exit()

if len(sys.argv) == 1 or args.help == True: # print help when no arguments given
    parser.print_help()
    parser.exit(0)

if args.outfileprefix != '': args.outfileprefix = args.outfileprefix + '_'

try:
    sheet_max_x = int(args.width)
    sheet_max_y = int(args.height)
except:
    error('Invalid sheet size specification. Must be integer')
    exit(1)

# gets maximum trimming info per image
trimcmd = (  r'convert ' + args.infilepattern
           + r' -trim '
           # + args.extra # resize etc mustn't be used before determining trim.
           + r' -format "%w %h %O %g\n" -identify null:'
          )
imgdata = (os.popen(trimcmd)  # launch imagemagick
            .read()       # get input (singular string)
            .strip()      # remove newline at the end
            .split("\n")) # split one file per line

# convert string to table of four integers
imgdata = [re.findall(r"\d+",x) # convert to quad of integers
           for x in imgdata]    # example: "126 89 +2+15 128x128+2+15" (x,y,geometry)

# determine image geometry for -crop and montage
frames  = len(imgdata)
org_x   = set([x[5] for x in imgdata]) # original image dimentions
org_y   = set([x[5] for x in imgdata])
min_x   = max([int(x[0]) for x in imgdata]) # minimum size of one frame 
min_y   = max([int(x[1]) for x in imgdata]) # minimum size of one frame 
shift_x = min([int(x[2]) for x in imgdata]) # shift from original size
shift_y = min([int(x[3]) for x in imgdata]) # shift from original size
geometry_crop = "{}x{}+{}+{}".format(min_x,min_y,shift_x,shift_y)

if args.extra != '': # now that we know the trim values we can add extra arguments like resize
    extracmd = ( r'convert ' + args.infilepattern
               + r' -crop ' + geometry_crop
               + r' +repage '
               + args.extra
               + r' -format "%w %h %O %g\n" -identify null:'
              )
    
    imgdata = (os.popen(extracmd)  # launch imagemagick
                .read()       # get input (singular string)
                .strip()      # remove newline at the end
                .split("\n")) # split one file per line
    
    # convert string to table of four integers
    imgdata = [re.findall(r"\d+",x) # convert to quad of integers
               for x in imgdata]    # example: "126 89 +2+15 128x128+2+15" (x,y,geometry)

    min_x   = max([int(x[0]) for x in imgdata]) # minimum size of one frame 
    min_y   = max([int(x[1]) for x in imgdata]) # minimum size of one frame 
geometry_mont = "{}x{}".format(min_x,min_y)


# size verification
if min_x > sheet_max_x or min_y > sheet_max_y:
    error('The sheet is to small to fit any frames!')
    exit(2)


# input verification
if len(org_x) > 1 or len(org_y) > 1:
    error('Error: All frames must have the same size.')
    exit(1)
else:
    org_x = list(org_x)[0]
    org_y = list(org_y)[0]



# determine best fit for sheet
def rowcols (max_frames,max_cols,max_rows):
    '''Given a maximum number of columns and rows, calculates the ratio of columns to rows
       that produces the least amount of empty frames for a given number of frame to fit.'''

    c = max_cols
    r = math.ceil(max_frames/c)
    if r > max_rows:
        print('Info: {} frames can not fit a {}*{} sheet'.format(max_frames,max_cols,max_rows))
        return

    # FIRST: find all col:row combinations that can fit at least
    #        max_frames into max_cols and max_rows
    factors = [(c,r)]
    for i in range(1,max_cols+1):
        if   (c-1) * r >= max_frames and c-1 >= r:
            c -= 1
        elif (c-1) * (r+1) >= max_frames and c-1 >= r+1 and r+1 <= max_rows:
            c -= 1
            r += 1
        factors.append((c,r))

    # SECOND: see if there is a col:row combination that wastes 0 frames
    perfects = [x for x in factors if x[0]*x[1] == max_frames]
    if perfects:
        factors = perfects # perfect fits override others
    else: 
        # THIRD: filter non-perfect col:row combinations that waste more frames than nessecary
        count = [x[0]*x[1] for x in factors]
        factors = [factors[idx] for idx,elm in enumerate(count) if elm == min(count)]

    # FOURTH: from the remaining col:row combinations use the one that is closest to a square (i.e. 3*4 overrides 2*6)
    sr = math.sqrt(max_frames)
    rootdist = [(math.fabs(sr-x[0]) + math.fabs(sr-x[1])) for x in factors]
    idx = rootdist.index(min(rootdist))

    # FIFTH: retun the best col:row combination found
    best = factors[idx]
    wasted = (best[0] * best[1] - max_frames)
    return best, wasted

# determine best sheet count
def sheetrows(total_frames,max_cols,max_rows):
    '''Determines which amount of sheets results in the lowest amount of wasted frames.'''
    '''In most cases the space saved on the last sheet by using more but better fitting sheets is insignificant.'''
    fps = max_cols*max_rows # frames per sheet
    # ZERO: Calculate waste
    def wasted(c,r):
        '''Determines the amount of wasted frames and amount of sheets for a given col:row ratio'''
        # TODO: option to not count completely empty rows as waste in the last sheet (because they can be trimmed)? Space wastes by this seems insignificant.
        scount = math.ceil(total_frames/(r*c))
        wls = (scount*r*c) - total_frames # waste in the last sheet
        wps = (rowcols(r*c,r,c))[1] # waste per sheet
        return ((scount*wps) + wls),scount

    # FIRST: varies amount of rows or columns to determine total waste and sheet count
    wastes = []
    if total_frames <= fps: # exactly one sheet
        rc,w = rowcols(total_frames,max_cols,max_rows)
        return [(w,1,rc[0],rc[1])] # same format as filtered multi-sheet
    else: # more than one sheet!
        for test_rows in range(1,max_rows+1):
            total_waste,sheet_count = wasted(max_cols,test_rows)
            wastes.append((total_waste,sheet_count,max_cols,test_rows))
        for test_cols in range(1,max_cols+1):
            total_waste,sheet_count = wasted(test_cols,max_rows)
            wastes.append((total_waste,sheet_count,test_cols,max_rows))

    # SECOND: remove doubletes and sort for later printing
    wastes = sorted(set(wastes),key=operator.itemgetter(1)) # sort by total waste

    # THIRD: filter out inferior permutations
    filtered = list(wastes) #copy list because manipulating wastes while iterating it is ugly
    def dofilter(elm):
        if elm in filtered: filtered.remove(elm)
    for this in range(len(wastes)):
        for other in range(len(wastes)):
            t = wastes[this]
            o = wastes[other]
            if t[0] == o[0] and t[1] < o[1]: #same waste more sheets
                dofilter(o)
            if t[1] == o[1] and t[0] < o[0]: #same sheets more waste
                dofilter(o)
            if t[0]  < o[0] and t[1] < o[1]: #more waste more sheets
                dofilter(o)
    return filtered

# Reaping the harvest.
max_cols = math.floor(sheet_max_x/min_x)  # maximum possibe frames per sheet
max_rows = math.floor(sheet_max_y/min_y)
waste,scount,cols,rows = sheetrows(frames,max_cols,max_rows)[0]

filename = "{}{}x{}_{}x{}.png".format(args.outfileprefix,min_x,min_y,cols,rows)
montagecmd = (   r'montage ' + args.infilepattern
               + r' -crop '    + geometry_crop
               + r' +repage ' # repage after crop
               + args.extra
               + r' +repage ' # repage after resize
               + r' -tile {}x{}'.format(cols,rows)
               + r' -geometry ' + geometry_mont
               + r' -background transparent'
               #+ r' -quality 95'
               + r' -define png:compression-level=9' # get okaish compression
               #+ r' -define png:compression-filter=5'
               #+ r' -define png:compression-strategy=2'
               + r' PNG32:' + filename )

print(
     'Found:'
    +'\nFrame count          : {}'.format(frames)
    +'\nFrame size (original): {}x{}'.format(org_x, org_y)
    +'\nFrame size (trimmed) : {}x{}'.format(min_x, min_y)
    +'\nAllowed sheet size   : {}x{}'.format(sheet_max_x,sheet_max_y)
    +'\nTarget sheet size    : {}x{} * {}'.format(cols*min_x, rows*min_y,scount)
    +'\nTarget sheet format  : {} * {}'.format(cols,rows)
    +'\nEmpty frames on last sheet: {}'.format(waste)
    +'\nExtra options: {}'.format(args.extra)
    +'\nCommand:\n' + montagecmd
    )

if args.yes == False:
    a = input('\n Proceed with sheet creation? (yes/zes/no): ')
    try:
        if a not in ['y','yes','sure','z','zes']: raise Exception()
    except:
        error(' Aborted by user.')
        exit(3)

print(os.popen(montagecmd).read())

if args.nosample == False:
    samplename = "{}{}x{}_{}x{}_sample.png".format(args.outfileprefix,min_x,min_y,cols,rows)
    samplecmd  = (   r'convert ' + args.sample
                 + r' -crop '    + geometry_crop
                 + r' +repage ' # repage after crop
                 + args.extra
                 + r' +repage ' # repage after resize
                 + r' -define png:compression-level=9' # get okaish compression
                 + r' PNG32:' + samplename
                 )
    print(os.popen(samplecmd).read())
