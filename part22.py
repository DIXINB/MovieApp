"""
We create 2D objects analytically and save in a dxf file (d26.dxf).
The meaning of execution in obtaining a list of necessary objects for a particular case
Iterating then this list, we call the available functions. With each execution, an object is added to our drawing
© Vadim Stetsenko, 2020
"""

import dxfwrite
from dxfwrite import DXFEngine as dxf   #connect the executing library and extract the engine
xp=[]
yp=[]
"""
The following parameter values ​​are only needed for testing without user interface
"""
#center=(8,2) #coordinates of the center of the circle
#radius=0.2   #circle radius
#xs=0         #x coordinate of the bottom left corner of the rectangle for block1 
#ys=0         #y coordinate for the same
#ws=1         #rectangle width for block1
#hs=1         #rectangle height for block1
#xs2=3        #x coordinate of the bottom left corner of the rectangle for block2
#ys2=3        #y coordinate for the same
#ws2=1        #rectangle width for block2
#hs2=1        #rectangle height for block2
#ws2obj=2     #width of the second piece in block 2
#hs2obj=1     #height of the second piece in block 2
#(xe,ye)=(1,1)#coordinates of the center of the ellipse
#rx=5.        #x-axis radius of the ellipse
#ry=2.        #x-axis radius of the ellipse
#alfa=0       #ellipse axis rotation angle
#list_for_polyline=[(0,3.5), (1.5,3.5), (2.7,4.5), (2,5.5), (0.5,5.5), (0,3.5)]

name="d26"
drawing=dxf.drawing('d26.dxf')


    #argument to function gives lst list
def circle (arg):
    center=arg[0]
    radius=arg[1]
    drawing.add(dxf.circle(center=center, radius=radius))

	#warning: ellipse coordinates are given as a tuple
def ellipse (arg):
    (xe,ye)=arg[0]
    rx=arg[1]
    ry=arg[2]
    alfa=arg[3]
    drawing.add(dxf.ellipse((xe,ye), rx, ry, rotation=alfa, segments=200))
	
	
    #create a polyline using the vertices whose coordinates are generated inside the function    
def create_polyline(arg):
    l=len(arg)
    polyline= dxf.polyline(thickness=3.)
    for n in range(l):
        (xpp,ypp)=arg[n]
        xp.append(xpp)
        yp.append(ypp)
    polyline.add_vertices( [(xp[n],yp[n])for n in range(l)])     
    drawing.add(polyline)
	
	
    #create a rectangle from segments using the standard dxfwrite library function
	#x, y are the coordinates of the lower left corner
    #w is the width, h is the height
def dxflist_1(x=0,y=0,w=1,h=1):
    rect=dxfwrite.DXFList()
    rect.append(dxf.line(start=(x,y), end=(x+w,y),color=7))
    rect.append(dxf.line(start=(x+w,y), end=(x+w,y+h),color=7))
    rect.append(dxf.line(start=(x+w,y+h), end=(x,y+h),color=7))
    rect.append(dxf.line(start=(x,y+h), end=(x,y),color=7))
    return rect

	
	#building a composite graphic object(block)
	#it's a rectangle with a hole inside
	#its position and radius are unchanged
	#input parameters are similar to those given for dxflist_1 function
def bl1(arg):
    xs=arg[0]
    ys=arg[1]
    ws=arg[2]
    hs=arg[3]  
    block=dxf.block(name='A')
    block.add(dxflist_1(xs,ys,ws,hs))
    block.add(dxf.circle(center=(0.5, 0.5),radius=0.1))
    attdef=dxf.attdef(
        insert=(.2, .2),
        tag='TEST'
    )
    block.add(attdef)
    drawing.blocks.add(block)
    block_ref=dxf.insert(blockname='A')
    drawing.add(block_ref)
	
	
    #building a composite graphic object
	#it is a whole indivisible figure made up of two rectangles
	#for the second rectangle only width and height (ws2obj,hs2obj)
    #are transmitted because it is rigidly attached to the first
    #input parameters are similar to those given for dxflist_1 function	
def bl2(arg):
    xs2=arg[0]
    ys2=arg[1]
    ws2=arg[2]
    hs2=arg[3]
    ws2obj=arg[4]
    hs2obj=arg[5]    
    block=dxf.block(name='B')
    block.add(dxflist_1(xs2,ys2,ws2,hs2))
    xs2obj=xs2
    ys2obj=ys2+hs2
    block.add(dxflist_1(xs2obj,ys2obj,ws2obj,hs2obj))
    attdef=dxf.attdef(
        insert=(.2, .2),
        tag='TEST'
    )
    block.add(attdef)
    drawing.blocks.add(block)
    block_ref=dxf.insert(blockname='B')
    drawing.add(block_ref)  

	
#list of drawing objects   
#lst=((circle, (center,radius)), (bl1,(xs,ys,ws,hs)), (bl2,(xs2,ys2,ws2,hs2,ws2obj,hs2obj)), (ellipse, ((xe,ye,),rx,ry,alfa)), (create_polyline, list_for_polyline))


#we create all the objects from the list (meaning lst) in the general figure
def main ():
    for (func,arg) in lst:
        func(arg)
    drawing.save() 

from sys import argv

lst=[]
list_for_polyline=[]
	
def e_circle():
    xc=float(input("Enter the X coordinate of the center of the circle :"))
    yc=float(input("Enter the Y coordinate of the center of the circle :"))
    rc=float(input("Enter the radius of the circle :"))
    
    obj=(circle,((xc,yc),rc))
    lst.append(obj)

   
def e_ellipse():
    xe=float(input("Enter the X coordinate of the center of the ellipse :"))
    ye=float(input("Enter the Y coordinate of the center of the ellipse :"))
    rx=float(input("Enter the rx of the ellipse :"))
    ry=float(input("Enter the ry of the ellipse :"))
    alfa=int(input("Enter the rotation angle :"))
    
    obj=(ellipse,((xe,ye,),rx,ry,alfa))
    lst.append(obj)
	

def e_bl1():
    xs=float(input("Enter the x coordinate of the bottom left corner of the rectangle for block1 :"))  
    ys=float(input("Enter the y coordinate for the same :"))
    ws=float(input("Enter the rectangle width for block1 :")) 
    hs=float(input("Enter the rectangle height for block1 :"))

    obj=(bl1,(xs,ys,ws,hs))
    lst.append(obj)
	
	
def e_bl2():
    xs2=float(input("Enter the x coordinate of the bottom left corner of the rectangle for block2 :"))  
    ys2=float(input("Enter the y coordinate for the same :"))
    ws2=float(input("Enter the rectangle width for block2 :")) 
    hs2=float(input("Enter the rectangle height for block2 :"))	
    ws2obj=float(input("Enter the rectangle width of the second piece in block 2 :"))
    hs2obj=float(input("Enter the rectangle height of the second piece in block 2 :"))	

    obj=(bl2,(xs2,ys2,ws2,hs2,ws2obj,hs2obj))
    lst.append(obj)


def e_polyline():
    for _ in range(1,7):
        x=float(input("Enter the X coordinate of point of the polyline :"))
        y=float(input("Enter the Y coordinate of the center of the polyline :"))
        list_for_polyline.append ([x,y])
    obj=(create_polyline,list_for_polyline)
    lst.append(obj)	
		
functions={'circle':e_circle, 'ellipse':e_ellipse, 'bl1':e_bl1, 'bl2':e_bl2, 'polyline':e_polyline}

	
for func in argv[1:]:
  functions[func]()
	
print(lst)
	
	
if __name__ == "__main__":
    main()
