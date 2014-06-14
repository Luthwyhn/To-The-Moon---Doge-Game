#TO THE MOON!  A Doge Game!
#			wow
#
#Originally created as Breakdown Countdown
#By Blayne 'Luthwyhn' White
#August 24-25, 2013
#
#Made For Ludum Dare #27
#With the theme of "10 Seconds"
#
#Modified for Doge goodness 12/15/13
#
#	very game				wow
#				such entrepreneurship
#
#  	Plz donate DOGE!				wow
# DMm3z82kgpuBZQkApX1dix1NMRDZ36GzEk
# 											very wallet

#Import from built-in libraries
import os, sys, time, pygame, random
from pygame.locals import *
from math import *

#Import from local libraries
from Helper import *
from Parts import *
from Consts import *

class BreakdownCountdown:
	def __init__(self, width=1024,height=768): 
		#Initialize PyGame
		pygame.init()
		pygame.mixer.init()
		pygame.font.init()
		self.Font=pygame.font.SysFont( "Comic Sans MS",128)
		self.ScoreFont=pygame.font.SysFont( "Comic Sans MS",23)
		
		#Set the window Size
		self.width = width
		self.height = height
		
		#Create the Screen
		self.GAME_TITLE="To The Moon!"
		pygame.display.set_caption(self.GAME_TITLE)
		self.screen = pygame.display.set_mode((self.width, self.height))
		
		#Black Screen for clearing
		self.BlankScreen=pygame.Surface((self.width, self.height))
		self.BlankScreen.convert()
		self.BlankScreen.fill((0,0,0))

		#Surfaces for rendering ship/pieces upon
		self.ShipCanvas=self.screen.subsurface(Rect(X_OFFSET+SHIP_X*TILE_SIZE,Y_OFFSET+SHIP_Y*TILE_SIZE,TILE_SIZE*NUM_COLS, TILE_SIZE*NUM_ROWS))
		self.ShipCanvas.set_clip((0,0,TILE_SIZE*NUM_COLS, TILE_SIZE*NUM_ROWS))
		self.PurpleCanvas=self.screen.subsurface((X_OFFSET+PURPLE_X*TILE_SIZE,PURPLE_Y*TILE_SIZE+Y_OFFSET,TILE_SIZE*3,TILE_SIZE*3))
		self.RedCanvas=self.screen.subsurface((X_OFFSET+RED_X*TILE_SIZE,RED_Y*TILE_SIZE+Y_OFFSET,TILE_SIZE*3,TILE_SIZE*3,))
		self.GreenCanvas=self.screen.subsurface((X_OFFSET+GREEN_X*TILE_SIZE,GREEN_Y*TILE_SIZE+Y_OFFSET,TILE_SIZE*3,TILE_SIZE*3))
		self.BlueCanvas=self.screen.subsurface((X_OFFSET+BLUE_X*TILE_SIZE,BLUE_Y*TILE_SIZE+Y_OFFSET,TILE_SIZE*3,TILE_SIZE*3))
		self.ShipCanvas.convert()
		self.PurpleCanvas.convert()
		self.RedCanvas.convert()
		self.GreenCanvas.convert()
		self.BlueCanvas.convert()
		
		#Initialize Data		
		self.RefreshTime = 1000.0/30.0
		self.LastRefresh=0
		self.CurrentTime=pygame.time.get_ticks()
		self.ScreenChanged=True
		
		#Data related to end game scoring
		self.Complete=False
		self.Thrust=0
		self.Fuel=0
		self.Weight=0
		self.Control=0

		
		#Data related to the countdown timer
		self.CountdownTime=18900
		self.StartTime=0
		self.TimeRemaining=0
		self.TimeMult=1
		self.Minutes=0
		self.Hours=0
		self.Sign=0
		
		#For fly away 'animation
		self.LastLift=0
		
		#For Score Display
		self.Text=[]
		
		#Track sound state
		self.Beep=0
		
		#Spaces to hold data about the various parts on the screen
		self.OnMouse=None
		
		self.PurplePart=None
		self.RedPart=None
		self.GreenPart=None
		self.BluePart=None
		self.ShipParts=[]
		
		#Generate an enpty 9x12 board (2 hidden spaces off right and bottom ends)
		self.ShipBoard=[]
		for i in range(9):
			self.ShipBoard.append([])
			for j in range(12):
				self.ShipBoard[i].append([False,[]])
				
		#Load artwork
		self.LaunchPadBG = load_image('LaunchPadBG.png')
		self.PlayField = load_image('PlayField.png',)
		self.FullField = load_image('FullField.png',)
		self.Clock = load_image('Clock.png')
		self.Numbers = load_image('Numbers.png')
		self.PlusMinus = load_image('PlusMinus.png',-1)
		self.Parts = load_image('Parts.png',-1)
		
		#Load sounds
		self.Beep1=load_sound('Beep1.wav')
		self.Beep2=load_sound('Beep2.wav')
		self.Liftoff=load_sound('Liftoff.wav')
		self.Collapse=load_sound('Collapse.wav')
		self.Change=load_sound('Change.wav')
		self.Place=load_sound('Place.wav')

		self.BG=self.LaunchPadBG

	def MainLoop(self):
		#Main game loop starts here
		self.screen.blit(self.BlankScreen,(0,0,self.width, self.height))
		self.StartTime=pygame.time.get_ticks()
		
		#Show the intro where the screens appear
		self.Intro()
		
		#Place initial parts
		self.PurplePart=GetPart()
		self.RedPart=GetPart()
		self.GreenPart=GetPart()
		self.BluePart=GetPart()
		
		self.OnMouse=GetPart()
		
		#Generate the initial nose cone
		rand=random.randint(1,3)
		if rand==1:
			Nose=Nose11()
			X=3
		elif rand==2:
			Nose=Nose22()
			X=3
		elif rand==3:
			Nose=Nose33()
			X=2
		
		self.TryPart(Nose,X,0)
		
		#Be sure to draw the initial screen
		self.ScreenChanged=True
		
		while 1:  #The lonliest number
			#Get the game time
			self.CurrentTime = pygame.time.get_ticks()
			
			self.Mouse_X=pygame.mouse.get_pos()[0]
			self.Mouse_Y=pygame.mouse.get_pos()[1]
			self.Mouse_X=(self.Mouse_X-X_OFFSET)/TILE_SIZE
			self.Mouse_Y=(self.Mouse_Y-Y_OFFSET)/TILE_SIZE
			
			#Check if enough time has passed for the next cycle (Framerate control)
			if(self.LastRefresh+self.RefreshTime<=self.CurrentTime):
				#Time for next cycle!  Do main game processes			
				self.LastRefresh = self.CurrentTime
				
				#Event Handling
				for event in pygame.event.get():
					if event.type == pygame.QUIT: 
						sys.exit()
					elif (event.type == KEYDOWN):
						if (event.key == K_ESCAPE):
							sys.exit()
						if (event.key == K_F1):
							return
						if(self.Sign==0):
							if (event.key == K_TAB):
								self.PurplePart=GetPart()
								self.RedPart=GetPart()
								self.GreenPart=GetPart()
								self.BluePart=GetPart()
								self.Change.play()
							if (event.key == K_1):
								self.Swap1()
							if (event.key == K_2):
								self.Swap2()
							if (event.key == K_3):
								self.Swap3()
							if (event.key == K_4):
								self.Swap4()
					elif (event.type == MOUSEBUTTONDOWN):
						if self.Sign==0:
							if(self.Mouse_X>=0)and(self.Mouse_X<=2):
								if(self.Mouse_Y>=4)and(self.Mouse_Y<=6):
									self.Swap1()
							elif(self.Mouse_X>=4)and(self.Mouse_X<=6):
								if(self.Mouse_Y>=4)and(self.Mouse_Y<=6):
									self.Swap2()
							if(self.Mouse_X>=0)and(self.Mouse_X<=2):
								if(self.Mouse_Y>=8)and(self.Mouse_Y<=10):
									self.Swap3()
							elif(self.Mouse_X>=4)and(self.Mouse_X<=6):
								if(self.Mouse_Y>=8)and(self.Mouse_Y<=10):
									self.Swap4()
							if(self.Mouse_X>=8)and(self.Mouse_X<=14):
								if(self.Mouse_Y>=0)and(self.Mouse_Y<=9):
									if(self.TryPart(self.OnMouse,self.Mouse_X-8,self.Mouse_Y)==True):
										self.OnMouse=GetPart()

				self.TimeRemaining=self.CountdownTime-self.TimeMult*(self.CurrentTime-self.StartTime)
				if (self.TimeRemaining<50):
					self.Sign=1
					self.TimeMult=-1
					self.LastLift=self.CurrentTime
					self.Score()
					if(self.Beep==4):
						if(self.Complete):
							self.Liftoff.play()
						else:
							self.Collapse.play()
						self.CountdownTime=-1*self.CountdownTime + 1001
					self.Beep=6
				elif (self.TimeRemaining >= 59990):
					self.CountdownTime=self.CountdownTime-60000
					self.Minutes=self.Minutes+1
					if(self.Minutes>=60):
						self.Minutes=0
						self.Hours=self.Hours+1

				#Lift off animation
				if(self.Sign==1 and self.Complete==True):
					if(self.CurrentTime-self.LastLift>1234):
						self.LastLift=self.CurrentTime
						for part in self.ShipParts:
							if(part.Y_Loc>-4):
								part.Y_Loc=part.Y_Loc-1
				elif(self.Sign==1):
					if(self.CurrentTime-self.LastLift>987):
						self.LastLift=self.CurrentTime
						for part in self.ShipParts:
							if(part.Y_Loc<14):
								part.Y_Loc=part.Y_Loc+1
						
				#Draw everything that goes on the screen
				if(self.ScreenChanged==True) or True: #No time to optimize this.
					#Redraw the whole screen if parts have updated
					self.screen.blit(self.BG,(0,0))
					self.ScreenChanged=False
					
					if(self.PurplePart!=None):
						self.PurplePart.Draw(self.PurpleCanvas,self.Parts,True)
					if(self.RedPart!=None):
						self.RedPart.Draw(self.RedCanvas,self.Parts,True)
					if(self.GreenPart!=None):
						self.GreenPart.Draw(self.GreenCanvas,self.Parts,True)
					if(self.BluePart!=None):
						self.BluePart.Draw(self.BlueCanvas,self.Parts,True)		
						
					for part in self.ShipParts:
						part.Draw(self.ShipCanvas,self.Parts)						
				
					self.PurpleCanvas.blit(self.Font.render("1",True,(180,180,0)),(64,64))
					self.RedCanvas.blit(self.Font.render("2",True,(180,180,0)),(64,64))
					self.GreenCanvas.blit(self.Font.render("3",True,(180,180,0)),(64,64))
					self.BlueCanvas.blit(self.Font.render("4",True,(180,180,0)),(64,64))
				
				#Glow the available spots
				if(self.Sign==0):
					self.Glow()
				#Update the timer
				self.BlitClock()

				if(self.OnMouse!=None and self.Sign==0):
					#Update mose position
					if(self.Mouse_X>=8)and(self.Mouse_X<=14)and(self.Mouse_Y>=0)and(self.Mouse_Y<=9):
						#self.screen.blit(self.Parts, (self.Mouse_X*TILE_SIZE+X_OFFSET,self.Mouse_Y*TILE_SIZE+Y_OFFSET), (TILE_SIZE*self.OnMouse.X_Pos,TILE_SIZE*self.OnMouse.Y_Pos,TILE_SIZE*self.OnMouse.X_Size,TILE_SIZE*self.OnMouse.Y_Size))
						self.OnMouse.Draw(self.ShipCanvas,self.Parts,False,self.Mouse_X-8,self.Mouse_Y)
						#Glow the OnMouse piece's required spaces
						for need in self.OnMouse.Needs:
							pygame.draw.circle(self.screen,(0,0,255),(int((self.Mouse_X+need[0]+0.5)*TILE_SIZE)+X_OFFSET,int((self.Mouse_Y+need[1]+0.5)*TILE_SIZE)+Y_OFFSET),14,2)
					else:
						self.screen.blit(self.Parts, (pygame.mouse.get_pos()[0]-32*self.OnMouse.X_Size,pygame.mouse.get_pos()[1]-32*self.OnMouse.Y_Size), (TILE_SIZE*self.OnMouse.X_Pos,TILE_SIZE*self.OnMouse.Y_Pos,TILE_SIZE*self.OnMouse.X_Size,TILE_SIZE*self.OnMouse.Y_Size))
				
				for i in range(len(self.Text)):
					self.ShipCanvas.blit(self.ScoreFont.render(self.Text[i],True,(180,255,0)),(8,8+32*i))

				self.screen.blit(self.ScoreFont.render("[TAB] for New Parts!     Wow!",True,(255,128,128),(64,64,64)),(527,700))
				self.screen.blit(self.ScoreFont.render("[ESC] to Exit.  [F1] for New Game.",True,(255,128,128),(64,64,64)),(527,732))
				
				#Update screen
				pygame.display.flip()
				
	def Score(self):
		self.Thrust=0
		self.Fuel=0
		self.Weight=0
		self.Control=0
		for part in self.ShipParts:
			self.Thrust+=(part.Thrust * 1.5)
			self.Fuel+=(part.Fuel * 1.5)
			self.Weight+=part.Weight
			self.Control+=part.Control
		if(self.Thrust>=self.Weight and self.Control>0):
			self.Complete=True
		
		self.Text=[]
		
		self.Text.append("Very parts: "+str('%.2f' %len(self.ShipParts)))
		self.Text.append("Such Thrust: "+str('%.2f' %self.Thrust)+"  wow")
		self.Text.append("Many Fuel: "+str('%.2f' %self.Fuel))
		self.Text.append("So Weight: "+str('%.2f' %self.Weight))
		self.Text.append("Plz Control: "+str('%.2f' %self.Control))
		self.Text.append(" ")
		if self.Complete:
			self.Text.append("Wow!")
		elif(self.Thrust<self.Weight):
			self.Text.append("Many failures!")
			self.Text.append("Much weight!")
		elif(self.Control<=0):
			self.Text.append("Such collapse!")
			self.Text.append("Few controls!")

		Score=0
		self.Text.append(" ")
		self.Text.append("Wow!  Such score:")
		if(self.Complete):
			Score= pow(10,sqrt(len(self.ShipParts)))*(self.Thrust/self.Weight)*log(self.Fuel+.01)*sqrt(self.Control)
			#Such maths!
		self.Text.append(str('%.2f' %Score))
		self.Text.append(" ")
		self.Text.append(" ")
		self.Text.append(" ")
		self.Text.append("Very game over!")
		self.Text.append("                    Much thanks")
		self.Text.append("   Plz Donate DOGE")
		self.Text.append(" ")
		self.Text.append("Wallet address in SUCH READ ME.txt")
		self.Text.append("")
				
	def Glow(self):
		for i in range(9):
			for j in range(12):
				if(self.ShipBoard[i][j][0]==False):
					continue
				if(self.ShipBoard[i][j][1].count(DOWN)>0):
					pygame.draw.line(self.ShipCanvas,(0,255,0),(i*64,j*64+61),(i*64+63,j*64+61),4)
				if(self.ShipBoard[i][j][1].count(UP)>0):
					pygame.draw.line(self.ShipCanvas,(0,255,0),(i*64,j*64+3),(i*64+63,j*64+3),4)
				if(self.ShipBoard[i][j][1].count(LEFT)>0):
					pygame.draw.line(self.ShipCanvas,(0,255,0),(i*64+3,j*64),(i*64+3,j*64+63),4)
				if(self.ShipBoard[i][j][1].count(RIGHT)>0):
					pygame.draw.line(self.ShipCanvas,(0,255,0),(i*64+61,j*64),(i*64+61,j*64+63),4)

	def Intro(self):
		while(1):
			self.CurrentTime = pygame.time.get_ticks()
			if(self.LastRefresh+self.RefreshTime<=self.CurrentTime):		
				self.LastRefresh = self.CurrentTime
			
				if((self.CurrentTime>=self.StartTime+0) and (self.Beep==0)):
					self.Beep1.play()
					self.Beep=1
				elif((self.CurrentTime>=self.StartTime+1000) and (self.Beep==1)):
					self.Beep1.play()
					self.BG=self.PlayField
					self.Beep=2
				elif((self.CurrentTime>=self.StartTime+1950) and (self.Beep==2)):
					self.Beep1.play()
					self.BG=self.FullField
					self.Beep=3
				elif((self.CurrentTime>=self.StartTime+2890) and (self.Beep==3)):
					self.Beep2.play()
					self.Beep=4
					return
				self.TimeRemaining=self.CountdownTime-self.TimeMult*(self.CurrentTime-self.StartTime)
				
				self.screen.blit(self.BG,(0,0))
				self.BlitClock()
				
				#Update screen
				pygame.display.flip()
			else:
				time.sleep(50.0/1000.0)
			
	def BlitClock(self):
		self.screen.blit(self.Clock,(8,8))
		self.screen.blit(self.Numbers,(60,19),((TILE_SIZE*int(self.Hours/10)),0,TILE_SIZE,128))
		self.screen.blit(self.Numbers,(130,19),((TILE_SIZE*int(self.Hours%10)),0,TILE_SIZE,128))
		self.screen.blit(self.Numbers,(210,19),((TILE_SIZE*int(self.Minutes/10)),0,TILE_SIZE,128))
		self.screen.blit(self.Numbers,(280,19),((TILE_SIZE*int(self.Minutes%10)),0,TILE_SIZE,128))
		self.screen.blit(self.Numbers,(364,19),((TILE_SIZE*((int(self.TimeRemaining/1000)/10)%10)),0,TILE_SIZE,128))
		self.screen.blit(self.Numbers,(434,19),((TILE_SIZE*(int(self.TimeRemaining/1000)%10)),0,TILE_SIZE,128))
		self.screen.blit(self.PlusMinus,(13,63),(40*self.Sign,0,40,40))
	
	def Swap1(self):
		temp=self.PurplePart
		self.PurplePart=self.OnMouse
		if self.PurplePart==None:
			self.PurplePart=GetPart()
		self.OnMouse=temp
	
	def Swap2(self):
		temp=self.RedPart
		self.RedPart=self.OnMouse
		if self.RedPart==None:
			self.RedPart=GetPart()
		self.OnMouse=temp
		
	def Swap3(self):
		temp=self.GreenPart
		self.GreenPart=self.OnMouse
		if self.GreenPart==None:
			self.GreenPart=GetPart()
		self.OnMouse=temp
		
	def Swap4(self):
		temp=self.BluePart
		self.BluePart=self.OnMouse
		if self.BluePart==None:
			self.BluePart=GetPart()
		self.OnMouse=temp
	
	def TryPart(self,Part,X,Y):
		#Check if the spots are empty
		for x in range(X,X+Part.X_Size):
			for y in range(Y,Y+Part.Y_Size):
				if(self.ShipBoard[x][y][0]==True):
					return False
		
		Connections=[]
		ToRemove=[]
		if(Y>0):
			for above in range(Part.X_Size):
				if(self.ShipBoard[X+above][Y-1][0]==True):
					#if not (above,0,UP) in Part.Allows:
					#	return False
					if (above,0,UP) in Part.Allows:
						ToRemove.append((above,0,UP))
					Connections.append((X+above,Y-1,DOWN))
		if(Y+Part.Y_Size<10):
			for below in range(Part.X_Size):
				if(self.ShipBoard[X+below][Y+Part.Y_Size][0]==True):
					#if not (below,Part.Y_Size-1,DOWN) in Part.Allows:
					#	return False
					if (below,Part.Y_Size-1,DOWN) in Part.Allows:
						ToRemove.append((below,Part.Y_Size-1,DOWN))
					Connections.append((X+below,Y+Part.Y_Size,UP))
		if(X>0):
			for left in range(Part.Y_Size):
				if(self.ShipBoard[X-1][Y+left][0]==True):
					#if not (0,left,LEFT) in Part.Allows:
					#	return False
					if (0,left,LEFT) in Part.Allows:
						ToRemove.append((0,left,LEFT))
					Connections.append((X-1,Y+left,RIGHT))
		if(X+Part.X_Size<7):
			for right in range(Part.Y_Size):
				if(self.ShipBoard[X+Part.X_Size][Y+right][0]==True):
					#if not (Part.X_Size-1,right,RIGHT) in Part.Allows:
					#	return False
					if (Part.X_Size-1,right,RIGHT) in Part.Allows:
						ToRemove.append((Part.X_Size-1,right,RIGHT))
					Connections.append((X+Part.X_Size,Y+right,LEFT))
		if (not ToRemove) and self.ShipParts:
			return False
		
		#If not connected to a previous piece, not a valid move.
		if ((not Connections) and self.ShipParts):
			return False
		
		#Check connection validity for each neighbor
		for con in Connections:
			if (not(con[2] in self.ShipBoard[con[0]][con[1]][1])):
				return False
		
		#Check that all needed spots are attached
		for need in Part.Needs:
			if not (((X+need[0],Y+need[1],UP) in Connections) or ((X+need[0],Y+need[1],DOWN) in Connections) or ((X+need[0],Y+need[1],LEFT) in Connections) or ((X+need[0],Y+need[1],RIGHT) in Connections)):
				return False
		
		#Update full spots
		for x in range(X,X+Part.X_Size):
			for y in range(Y,Y+Part.Y_Size):
				self.ShipBoard[x][y][0]=True
		
		#Remove used allows (for glow purposes)
		for con in Connections:
			self.ShipBoard[con[0]][con[1]][1].remove(con[2])
		
		#Update ShipBoard allowed list
		for rem in ToRemove:
			Part.Allows.remove(rem)
		for allow in Part.Allows:
			self.ShipBoard[X+allow[0]][Y+allow[1]][1].append(allow[2])
		
		#Add part to display list
		Part.X_Loc=X
		Part.Y_Loc=Y
		self.ShipParts.append(Part)
		self.Place.play()
		return True
		
if __name__ == "__main__":
	while(True):
		MainWindow = BreakdownCountdown()
		MainWindow.MainLoop()
		
		#      wow
