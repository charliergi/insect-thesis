import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from math import sqrt,ceil,floor


def plot_rect(xmin,ymin,width,height,color):
    currentAxis.add_patch(Rectangle((xmin, ymin), width, height, fill=None, alpha=1,color=color,linewidth=2.0))

plt.figure()
currentAxis = plt.gca()

scale_factor_x = 800
scale_factor_y = 800

xmin, xmax = plt.xlim()
ymin, ymax = plt.ylim()

plt.xlim(xmin * scale_factor_x-100, xmax * scale_factor_x)
plt.ylim(ymin * scale_factor_y-100, ymax * scale_factor_y)

dimension=128
center=320
for scale in [(1,"r"),(2,"b"),(4,"g")]:
    formula_half=sqrt((dimension*scale[0])*(dimension*scale[0])/2)
    formula_normal = 2*formula_half
    for size in [[dimension*scale[0],dimension*scale[0]],[formula_half,formula_normal],[formula_normal,formula_half]]:
        color=scale[1]
        width=floor(size[0])
        height=ceil(size[1])
        xmin=(center-width/2)
        ymin=(center-height/2)
        plot_rect(xmin,ymin,width,height,color)
        print(str.format("xmin {}, ymin {}, width {}, height {}",xmin,ymin,width,height))
plt.title("Anchors generation with dimensions \n 128x128, 256x256, 512x512 with ratios (1,1),(1,2),(2,1)")
plt.show()
