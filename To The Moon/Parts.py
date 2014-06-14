#Parts data for To The Moon/Breakdown Countdown
#Blayne 'Luthwyhn' White
#wow
import os, sys, time, pygame, random, math
from pygame.locals import *
from math import *
from Consts import *

class Part:
	def __init__(self):
		#Location on the screen of individual instance of part
		self.X_Loc=0
		self.Y_Loc=0
		
		#Scoring Data
		self.Thrust=0
		self.Fuel=0
		self.Weight=0
		self.Control=0
		
		#Top-Left Position and size on sprite sheet 
		self.X_Pos=0
		self.Y_Pos=0
		self.X_Size=1
		self.Y_Size=1
		
		#Attachment needs lists
		self.Needs=[]
		self.Allows=[]
	
	def Draw(self,Screen,SpriteSheet,UseOffset=False,X=-1,Y=-1):
		if(X<0):
			X=self.X_Loc
		if(Y<0):
			Y=self.Y_Loc
		if(UseOffset==True):
			if(self.X_Size==1):
				X=X+1
			elif(self.X_Size==2):
				X=X+0.5
			if(self.Y_Size==1):
				Y=Y+1
			elif(self.Y_Size==2):
				Y=Y+0.5
		Screen.blit(SpriteSheet,(TILE_SIZE*X,TILE_SIZE*Y),(TILE_SIZE*self.X_Pos,TILE_SIZE*self.Y_Pos,TILE_SIZE*self.X_Size,TILE_SIZE*self.Y_Size))
		
class Nose11(Part):
	def __init__(self):	
		self.X_Loc=0
		self.Y_Loc=0
		self.X_Pos=0
		self.Y_Pos=0
		self.X_Size=1
		self.Y_Size=1
		self.Thrust=0
		self.Fuel=1
		self.Weight=1
		self.Control=1
		#Attachment needs lists
		self.Needs=[]
		self.Allows=[(0,0,DOWN)]
		
class Nose22(Part):
	def __init__(self):
		self.X_Loc=0
		self.Y_Loc=0
		self.X_Pos=1
		self.Y_Pos=0
		self.X_Size=2
		self.Y_Size=2
		self.Thrust=0
		self.Fuel=2
		self.Weight=2
		self.Control=2
		#Attachment needs lists
		self.Needs=[]
		self.Allows=[(0,1,DOWN),(1,1,DOWN)]
		
class Nose33(Part):
	def __init__(self):
		self.X_Loc=0
		self.Y_Loc=0
		self.X_Pos=3
		self.Y_Pos=0
		self.X_Size=3
		self.Y_Size=3
		self.Thrust=0
		self.Fuel=3
		self.Weight=3
		self.Control=3
		#Attachment needs lists
		self.Needs=[]
		self.Allows=[(0,2,DOWN),(1,2,DOWN),(2,2,DOWN)]
		
class Body11(Part):
	def __init__(self):
		self.X_Loc=0
		self.Y_Loc=0
		self.X_Pos=0
		self.Y_Pos=1
		self.X_Size=1
		self.Y_Size=1
		self.Thrust=0
		self.Fuel=1
		self.Weight=1
		self.Control=-1
		#Attachment needs lists
		self.Needs=[]
		self.Allows=[(0,0,UP),(0,0,DOWN),(0,0,LEFT),(0,0,RIGHT)]
		
class Body12(Part):
	def __init__(self):
		self.X_Loc=0
		self.Y_Loc=0
		self.X_Pos=0
		self.Y_Pos=2
		self.X_Size=1
		self.Y_Size=2
		self.Thrust=0
		self.Fuel=2
		self.Weight=sqrt(2)
		self.Control=-1.5
		#Attachment needs lists
		self.Needs=[]
		self.Allows=[(0,0,UP),(0,0,LEFT),(0,0,RIGHT),(0,1,DOWN),(0,1,LEFT),(0,1,RIGHT)]
		
class Body21(Part):
	def __init__(self):
		self.X_Loc=0
		self.Y_Loc=0
		self.X_Pos=1
		self.Y_Pos=2
		self.X_Size=2
		self.Y_Size=1
		self.Thrust=0
		self.Fuel=2
		self.Weight=sqrt(2)
		self.Control=-1.5
		#Attachment needs lists
		self.Needs=[]
		self.Allows=[(0,0,UP),(0,0,DOWN),(0,0,LEFT),(1,0,UP),(1,0,DOWN),(1,0,RIGHT)]
		
class Body22(Part):
	def __init__(self):
		self.X_Loc=0
		self.Y_Loc=0
		self.X_Pos=1
		self.Y_Pos=3
		self.X_Size=2
		self.Y_Size=2
		self.Thrust=0
		self.Fuel=4
		self.Weight=2
		self.Control=-2
		#Attachment needs lists
		self.Needs=[]
		self.Allows=[(0,0,UP),(0,0,LEFT),(1,0,UP),(1,0,RIGHT),(0,1,DOWN),(0,1,LEFT),(1,1,DOWN),(1,1,RIGHT)]
		
class Body31(Part):
	def __init__(self):
		self.X_Loc=0
		self.Y_Loc=0
		self.X_Pos=3
		self.Y_Pos=3
		self.X_Size=3
		self.Y_Size=1
		self.Thrust=0
		self.Fuel=3
		self.Weight=sqrt(3)
		self.Control=-2
		#Attachment needs lists
		self.Needs=[]
		self.Allows=[(0,0,UP),(0,0,DOWN),(0,0,LEFT),(1,0,UP),(1,0,DOWN),(2,0,UP),(2,0,DOWN),(2,0,RIGHT)]
		
class Body32(Part):
	def __init__(self):
		self.X_Loc=0
		self.Y_Loc=0
		self.X_Pos=3
		self.Y_Pos=4
		self.X_Size=3
		self.Y_Size=2
		self.Thrust=0
		self.Fuel=6
		self.Weight=sqrt(6)
		self.Control=-2.5
		#Attachment needs lists
		self.Needs=[]
		self.Allows=[(0,0,UP),(0,0,LEFT),(1,0,UP),(2,0,UP),(2,0,RIGHT),(0,1,DOWN),(0,1,LEFT),(1,1,DOWN),(2,1,DOWN),(2,1,RIGHT)]
		
class Body33(Part):
	def __init__(self):
		self.X_Loc=0
		self.Y_Loc=0
		self.X_Pos=3
		self.Y_Pos=6
		self.X_Size=3
		self.Y_Size=3
		self.Thrust=0
		self.Fuel=9
		self.Weight=3
		self.Control=-3
		#Attachment needs lists
		self.Needs=[]
		self.Allows=[(0,0,UP),(0,0,LEFT),(1,0,UP),(2,0,UP),(2,0,RIGHT),(0,1,LEFT),(2,1,RIGHT),(0,2,DOWN),(0,2,LEFT),(1,2,DOWN),(2,2,DOWN),(2,2,RIGHT)]
		
class Frame11(Part):
	def __init__(self):
		self.X_Loc=0
		self.Y_Loc=0
		self.X_Pos=0
		self.Y_Pos=4
		self.X_Size=1
		self.Y_Size=1
		self.Thrust=0
		self.Fuel=0
		self.Weight=0.25
		self.Control=0
		#Attachment needs lists
		self.Needs=[]
		self.Allows=[(0,0,UP),(0,0,DOWN),(0,0,LEFT),(0,0,RIGHT)]
		
class Frame12(Part):
	def __init__(self):
		self.X_Loc=0
		self.Y_Loc=0
		self.X_Pos=0
		self.Y_Pos=5
		self.X_Size=1
		self.Y_Size=2
		self.Thrust=0
		self.Fuel=0
		self.Weight=0.5
		self.Control=0
		#Attachment needs lists
		self.Needs=[]
		self.Allows=[(0,0,UP),(0,0,LEFT),(0,0,RIGHT),(0,1,DOWN),(0,1,LEFT),(0,1,RIGHT)]
		
class Frame22(Part):
	def __init__(self):
		self.X_Loc=0
		self.Y_Loc=0
		self.X_Pos=1
		self.Y_Pos=5
		self.X_Size=2
		self.Y_Size=2
		self.Thrust=0
		self.Fuel=0
		self.Weight=1
		self.Control=0
		#Attachment needs lists
		self.Needs=[]
		self.Allows=[(0,0,UP),(0,0,LEFT),(1,0,UP),(1,0,RIGHT),(0,1,DOWN),(0,1,LEFT),(1,1,DOWN),(1,1,RIGHT)]
		
class Frame31(Part):
	def __init__(self):
		self.X_Loc=0
		self.Y_Loc=0
		self.X_Pos=0
		self.Y_Pos=7
		self.X_Size=3
		self.Y_Size=1
		self.Thrust=0
		self.Fuel=0
		self.Weight=0.75
		self.Control=0
		#Attachment needs lists
		self.Needs=[]
		self.Allows=[(0,0,UP),(0,0,DOWN),(0,0,LEFT),(1,0,UP),(1,0,DOWN),(2,0,UP),(2,0,DOWN),(2,0,RIGHT)]
		
class Frame32(Part):
	def __init__(self):
		self.X_Loc=0
		self.Y_Loc=0
		self.X_Pos=0
		self.Y_Pos=8
		self.X_Size=3
		self.Y_Size=2
		self.Thrust=0
		self.Fuel=0
		self.Weight=1.5
		self.Control=0
		#Attachment needs lists
		self.Needs=[]
		self.Allows=[(0,0,UP),(0,0,LEFT),(1,0,UP),(2,0,UP),(2,0,RIGHT),(0,1,DOWN),(0,1,LEFT),(1,1,DOWN),(2,1,DOWN),(2,1,RIGHT)]
		
class Frame21(Part):
	def __init__(self):
		self.X_Loc=0
		self.Y_Loc=0
		self.X_Pos=3
		self.Y_Pos=9
		self.X_Size=2
		self.Y_Size=1
		self.Thrust=0
		self.Fuel=0
		self.Weight=0.5
		self.Control=0
		#Attachment needs lists
		self.Needs=[]
		self.Allows=[(0,0,UP),(0,0,DOWN),(0,0,LEFT),(1,0,UP),(1,0,DOWN),(1,0,RIGHT)]
		
class Thrust11(Part):
	def __init__(self):
		self.X_Loc=0
		self.Y_Loc=0
		self.X_Pos=5
		self.Y_Pos=9
		self.X_Size=1
		self.Y_Size=1
		self.Thrust=1
		self.Fuel=0
		self.Weight=0.5
		self.Control=0
		#Attachment needs lists
		self.Needs=[(0,-1)]
		self.Allows=[(0,0,UP)]
		
class Thrust21(Part):
	def __init__(self):
		self.X_Loc=0
		self.Y_Loc=0
		self.X_Pos=6
		self.Y_Pos=9
		self.X_Size=2
		self.Y_Size=1
		self.Thrust=3
		self.Fuel=0
		self.Weight=1
		self.Control=0
		#Attachment needs lists
		self.Needs=[(0,-1),(1,-1)]
		self.Allows=[(0,0,UP),(1,0,UP)]
		
class Thrust22(Part):
	def __init__(self):
		self.X_Loc=0
		self.Y_Loc=0
		self.X_Pos=8
		self.Y_Pos=8
		self.X_Size=2
		self.Y_Size=2
		self.Thrust=8
		self.Fuel=0
		self.Weight=2
		self.Control=0
		#Attachment needs lists
		self.Needs=[(0,-1),(1,-1)]
		self.Allows=[(0,0,UP),(1,0,UP)]
		
class Thrust32(Part):
	def __init__(self):
		self.X_Loc=0
		self.Y_Loc=0
		self.X_Pos=6
		self.Y_Pos=4
		self.X_Size=3
		self.Y_Size=2
		self.Thrust=15
		self.Fuel=0
		self.Weight=3
		self.Control=0
		#Attachment needs lists
		self.Needs=[(0,-1),(1,-1),(2,-1)]
		self.Allows=[(0,0,UP),(1,0,UP),(2,0,UP)]
		
class Thrust12(Part):
	def __init__(self):
		self.X_Loc=0
		self.Y_Loc=0
		self.X_Pos=9
		self.Y_Pos=4
		self.X_Size=1
		self.Y_Size=2
		self.Thrust=3
		self.Fuel=0
		self.Weight=1
		self.Control=0
		#Attachment needs lists
		self.Needs=[(0,-1)]
		self.Allows=[(0,0,UP)]
		
class LT11(Part):
	def __init__(self):
		self.X_Loc=0
		self.Y_Loc=0
		self.X_Pos=7
		self.Y_Pos=8
		self.X_Size=1
		self.Y_Size=1
		self.Thrust=1
		self.Fuel=0
		self.Weight=0.5
		self.Control=0
		#Attachment needs lists
		self.Needs=[(1,0)]
		self.Allows=[(0,0,RIGHT)]
		
class LT22(Part):
	def __init__(self):
		self.X_Loc=0
		self.Y_Loc=0
		self.X_Pos=8
		self.Y_Pos=6
		self.X_Size=2
		self.Y_Size=2
		self.Thrust=8
		self.Fuel=0
		self.Weight=2
		self.Control=0
		#Attachment needs lists
		self.Needs=[(2,0),(2,1)]
		self.Allows=[(1,0,RIGHT),(1,1,RIGHT)]
		
class RT11(Part):
	def __init__(self):
		self.X_Loc=0
		self.Y_Loc=0
		self.X_Pos=6
		self.Y_Pos=8
		self.X_Size=1
		self.Y_Size=1
		self.Thrust=0
		self.Fuel=0
		self.Weight=0
		self.Control=0
		#Attachment needs lists
		self.Needs=[(-1,0)]
		self.Allows=[(0,0,LEFT)]
		
class RT22(Part):
	def __init__(self):
		self.X_Loc=0
		self.Y_Loc=0
		self.X_Pos=6
		self.Y_Pos=6
		self.X_Size=2
		self.Y_Size=2
		self.Thrust=1
		self.Fuel=0
		self.Weight=0.5
		self.Control=0
		#Attachment needs lists
		self.Needs=[(-1,0),(-1,1)]
		self.Allows=[(0,0,LEFT),(0,1,LEFT)]
		
class LW12(Part):
	def __init__(self):
		self.X_Loc=0
		self.Y_Loc=0
		self.X_Pos=6
		self.Y_Pos=0
		self.X_Size=1
		self.Y_Size=2
		self.Thrust=0
		self.Fuel=0
		self.Weight=0.5
		self.Control=2
		#Attachment needs lists
		self.Needs=[(1,0),(1,1)]
		self.Allows=[(0,0,RIGHT),(0,1,RIGHT)]
		
class LW21(Part):
	def __init__(self):
		self.X_Loc=0
		self.Y_Loc=0
		self.X_Pos=8
		self.Y_Pos=0
		self.X_Size=2
		self.Y_Size=1
		self.Thrust=0
		self.Fuel=0
		self.Weight=0.5
		self.Control=2
		#Attachment needs lists
		self.Needs=[(2,0)]
		self.Allows=[(1,0,RIGHT)]
		
class LW22(Part):
	def __init__(self):
		self.X_Loc=0
		self.Y_Loc=0
		self.X_Pos=6
		self.Y_Pos=2
		self.X_Size=2
		self.Y_Size=2
		self.Thrust=0
		self.Fuel=0
		self.Weight=1
		self.Control=4
		#Attachment needs lists
		self.Needs=[(2,0),(2,1)]
		self.Allows=[(1,0,RIGHT),(1,1,RIGHT)]
		
class RW12(Part):
	def __init__(self):
		self.X_Loc=0
		self.Y_Loc=0
		self.X_Pos=7
		self.Y_Pos=0
		self.X_Size=1
		self.Y_Size=2
		self.Thrust=0
		self.Fuel=0
		self.Weight=0.5
		self.Control=2
		#Attachment needs lists
		self.Needs=[(-1,0),(-1,1)]
		self.Allows=[(0,0,LEFT),(0,1,LEFT)]
		
class RW21(Part):
	def __init__(self):
		self.X_Loc=0
		self.Y_Loc=0
		self.X_Pos=8
		self.Y_Pos=1
		self.X_Size=2
		self.Y_Size=1
		self.Thrust=0
		self.Fuel=0
		self.Weight=0.5
		self.Control=2
		#Attachment needs lists
		self.Needs=[(-1,0)]
		self.Allows=[(0,0,LEFT)]
		
class RW22(Part):
	def __init__(self):
		self.X_Loc=0
		self.Y_Loc=0
		self.X_Pos=8
		self.Y_Pos=2
		self.X_Size=2
		self.Y_Size=2
		self.Thrust=0
		self.Fuel=0
		self.Weight=1
		self.Control=4
		#Attachment needs lists
		self.Needs=[(-1,0),(-1,1)]
		self.Allows=[(0,0,LEFT),(0,1,LEFT)]
		
def GetPart():
	num=random.randint(1,31)
	if(num==1):
		return Nose11()
	if(num==2):
		return Nose22()
	if(num==3):
		return Nose33()
	if(num==4):
		return Body11()
	if(num==5):
		return Body12()
	if(num==6):
		return Body21()
	if(num==7):
		return Body22()
	if(num==8):
		return Body31()
	if(num==9):
		return Body32()
	if(num==10):
		return Body33()
	if(num==11):
		return Frame11()
	if(num==12):
		return Frame12()
	if(num==13):
		return Frame22()
	if(num==14):
		return Frame31()
	if(num==15):
		return Frame32()
	if(num==16):
		return Frame32()
	if(num==17):
		return Thrust11()
	if(num==18):
		return Thrust21()
	if(num==19):
		return Thrust22()
	if(num==20):
		return Thrust32()
	if(num==21):
		return Thrust12()
	if(num==22):
		return LT11()
	if(num==23):
		return LT22()
	if(num==24):
		return RT11()
	if(num==25):
		return RT22()
	if(num==26):
		return LW12()
	if(num==27):
		return LW21()
	if(num==28):
		return LW22()
	if(num==29):
		return RW12()
	if(num==30):
		return RW21()
	if(num==31):
		return RW22()
	
	
#Such comments




#wow