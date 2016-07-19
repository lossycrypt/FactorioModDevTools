import sys
import os
import math

#sys.argv = ["sc.py",96,91,33,34]
#sys.argv = ["sc.py",96,91,32.5,33.5]
#sys.argv = ["sc.py",64,64,31.5,31.5]

# width/height in total pixels
# x/y is zero-indexed from left upper corner
# x/y is coordinate of the center of a pixel
# i.e the middle of a 64x64 picture is between pixels 31 and 32 (31.5)
# usually the x/y pixel you want is -0.5 from what your program shows
# also guesses the selection and collision boxes.

if len(sys.argv) not in [5,6]:
    print('Incorrect number of arguments.')
    print('Usage: this.py <width> <height> <center x> <center y> <scale>')
    exit(1)
try:
    w,h,x,y = [float(x) for x in sys.argv[1:5]]
except:
    print('Incorrect argument type.')
    exit(1)
try:
    if len(sys.argv) == 6:
        s = float(sys.argv[5])
except:
    print('Incorrect scale.')
    exit(1)

if not ('s' in locals()):
  #print('Using default scale = 1.0')
  s = 1.0
else:
  #print('Using custom scale = {}'.format(s))
  pass

if x == int(x) or y == int(y):
    print('Did you forget to account for half pixels?')
 
# w -= 1 ; h -= 1 # make w/h zero-indexed
w,h,x,y = [arg*s for arg in [w,h,x,y]]


shiftx  = ((w-1)/2 - x) / 32
shifty  = ((h-1)/2 - y) / 32
shiftx -= shiftx % (1/256) # clip to factorio internal resolution?
shifty -= shifty % (1/256) # clip to factorio internal resolution?


# trying to guess selection and collision box up to two decimal points
sel_corner_real   = [math.ceil(i * 100)/100 for i in ((w-x)/64, (h-y)/64)]
sel_corner_square = [(sel_corner_real[0]+sel_corner_real[1]) / 2 for x in range(2)]
selreal   = [ i*x for i in (-1,1) for x in sel_corner_real ] # mirror to opposite corner
selsquare = [ i*x for i in (-1,1) for x in sel_corner_square ] # mirror to opposite corner


colreal   = [ x-0.15 if x > 0 else x+0.15 for x in selreal]
colsquare = [ x-0.15 if x > 0 else x+0.15 for x in selsquare]

# adjusting scale
#selreal,colreal,selsquare,colsquare = [ [elm*s for elm in lst] for lst in [selreal,colreal,selsquare,colsquare]]

def toarea (a):
  return '{{ {{ {:.2f}, {:.2f} }}, {{ {:.2f}, {:.2f} }} }}'.format(a[0],a[1],a[2],a[3])
  
shift   = "shift         = {{ {0}, {1} }}, -- {2}x{3} x={4} y={5} s={6}".format(shiftx, shifty,int(w/s),int(h/s),x/s,y/s,s)
scale   = "scale         = {},".format(s)

sreal   = 'selection_box = {}, -- actual selection box'.format(toarea(selreal))
ssquare = 'selection_box = {}, -- square selection box'.format(toarea(selsquare))

creal   = 'collision_box = {}, -- actual collision box'.format(toarea(colreal))
csquare = 'collision_box = {}, -- square collision box'.format(toarea(colsquare))





print(sreal)
print(creal)
print(ssquare)
print(csquare)
print(shift)
print(scale)

if os.name == 'nt':
    try: # http://stackoverflow.com/a/9409898
        clipstring = '\\n'.join([sreal,creal,ssquare,csquare,shift,scale])
        cmdstring = ("{} -c \"print('{}')\" | clip".format(sys.executable,clipstring)) # quoteception with escaped newlines.
        os.system(cmdstring)
        print('(Copied to clipboard!)')
    except:
        print('(Not copied to clipboard.)')
else:
    print('No clipboard support for platform "{}" yet.'.format(os.name))


    
