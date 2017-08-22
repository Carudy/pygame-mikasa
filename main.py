# -*- coding: utf-8 -*-
import pygame
import math
import random
from pygame.locals import *
from sys import exit
import os
import copy

pygame.init()
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.mixer.set_num_channels(25)

_width,_height=1280,720
_size=(_width,_height)
pygame.display.init()
screen = pygame.display.set_mode(_size,0,32)
#screen = pygame.display.set_mode(_size,FULLSCREEN,32)
pygame.display.set_caption("game")

p_img=lambda x,y,z:pygame.transform.scale(pygame.image.load(x).convert_alpha(),(y,z))
j_img=lambda x,y,z:pygame.transform.scale(pygame.image.load(x).convert(),(y,z))
v_dist =lambda x1,y1,x2,y2:(x1-x2)**2+(y1-y2)**2
v_make =lambda x1,y1,x2,y2:((x2-x1),(y2-y1))
v_mak  =lambda x,y:(y[0]-x[0],y[1]-x[1])
v_cha  =lambda x,y:x[0]*y[1]-x[1]*y[0]
v_dan  =lambda x,y:x[0]*x[1]+y[1]*y[0]
v_dis  =lambda x1,y1,x2,y2:math.sqrt(v_dist(x1,y1,x2,y2))
isze   =lambda x:0 if abs(x)<0.000001 else 1 if x>0 else -1
v_cro  =lambda x,y,z:isze(v_cha(v_mak(x,y),v_mak(x,z)))

boder=(40,940,20,700)
bod_lines 	= 		[]
danmu	  	= 		[]
dijis	  	= 		[]
animes	  	= 		[]
buffs		=		[]
harm_id   	= 		0
diji_id   	= 		0

mapping 	= 		1
mcd		 	= 		0
g 			=		0
fp=open('out.txt','w')

bk=j_img('pics/map1.jpg',900,680)
ak=j_img('pics/tt.jpg',300,680) 
ak.fill(0xffcc66)
#*****************************************************************************************
def anime_ins(id,x,y):
	global animes,anis
	n_ani=copy.copy(anis.an[id])
	n_ani._x,n_ani._y=x,y
	animes.append(n_ani)

def v_ori(x1,y1,x2,y2):
	vec=v_make(x1,y1,x2,y2)
	dis=math.sqrt(v_dist(x1,y1,x2,y2))
	if dis==0:
		dis=0.0001
	return (vec[0]/dis,vec[1]/dis)

def dec(x,y):
	if x>0:
		return x-min(x,y)
	else:
		x=-x
		return -(x-min(x,y))

def bod_init():
	global bod_lines
	bod_lines = []
	bod_lines.append((40,20,940,20,2))
	bod_lines.append((40,20,40,700,2))
	bod_lines.append((940,20,940,700,2))
	bod_lines.append((40,700,940,700,2))

def dis_db(x,y,z):
	v0=v_make(z[0],z[1],z[2],z[3])
	v1=v_make(z[0],z[1],x,y)
	v2=v_make(z[2],z[3],x,y)
	if v_dan(v0,v1)*v_dan(v0,v2)>=0:
		return min(v_dis(z[0],z[1],x,y),v_dis(z[2],z[3],x,y))
	else:
		return abs(v_cha(v0,v1))/v_dis(z[0],z[1],z[2],z[3])

def yes_xy(x,y,z):
	global bod_lines
	for i in bod_lines:
		if i[4]>=z and dis_db(x,y,i)<5:
			return False
	return True

def yes_xy0(x,y,z):
	global dijis
	bo=yes_xy(x,y,z)
	if bo==False:
		return False
	for i in dijis:
		if v_dis(x,y,i._x,i._y)<i.r+5:
			return False
	return True

def yes_xy1(x,y,z,w):
	global dijis,mika
	bo=yes_xy(x,y,z)
	if bo==False:
		return False
	if v_dis(x,y,mika._x,mika._y)<10:
		return False
	for i in dijis:
		if i.did!=w and v_dis(x,y,i._x,i._y)<i.r+5:
			return False
	return True

def rota(x,y):
	if y==0:
		return 0
	du=math.asin(v_cha((x,y),(1,0))/v_dis(0,0,x,y))*180/math.pi
	if x>=0:
		return du
	else:
		return 180-du 

def can_see(x1,y1,x2,y2,z):
	global bod_lines
	if v_dis(x1,y1,x2,y2)>z:
		return False
	d0,d1=(x1,y1),(x2,y2)
	for i in filter(lambda x:x[4]==1,bod_lines):
		d2,d3=(i[0],i[1]),(i[2],i[3])
		if v_cro(d0,d2,d3)^v_cro(d1,d2,d3)==-2 and v_cro(d2,d0,d1)^v_cro(d3,d0,d1)==-2:
			return False
	return True

#*****************************************************************************************
#******************** x: 40-940  y: 20-700 ***********************************************
#********************************** class ************************************************
class buff_r0():
	def __init__(self):
		global mika
		self.t=0
		mika.atk+=100
		mika.dfd+=50
		mika.speed+=0.1
	def run(self,timep):
		self.t+=timep
		if self.t>=mika.r0_t:
			mika.atk-=100
			mika.dfd-=50
			mika.speed-=0.1
			return False
		return True

class danmu_piao():
	def __init__(self,x,y,z):
		global moji
		self._x,self._y = x+5,y-10
		self.img=moji.rd(2,str(z),2)
		self.type=1
		self.gong=0
		self.friend=0
		self.t=0

	def run(self,timep):
		self.t+=timep
		self._y-=timep*0.05
		return self.t<1000

class danmu_tar():
	def __init__(self,x,y):
		self._x,self._y=x,y
		self.friend=0
		self.type=1
		self.img = p_img("pics/tar.png",35,35)
		self.gong=0
	def run(self,timep):
		return True

class danmu_sheng():
	def __init__(self,x,y,dx,dy):
		self.x,self.y,self.dx,self.dy = x,y,dx,dy
		self.type=0
		self.t=0
		self.sta=0
		self.gong=0

	def run(self,timep):
		global bod_lines,mika,sound
		self.t+=timep
		if self.sta==0:
			self.x+=self.dx
			self.y+=self.dy
			for i in bod_lines:
				if i[4]==1 and dis_db(self.x,self.y,i)<5:
					vec=v_ori(mika._x,mika._y,self.x,self.y)
					dis=v_dis(mika._x,mika._y,self.x,self.y)*0.01
					dis=3.3 if dis>3.3 else dis
					vx,vy=vec[0]*dis,vec[1]*dis
					mika.get_speed(vx,vy,800)
					self.sta=1
					break
		pygame.draw.line(screen,0x775510,(self.x,self.y),(mika._x,mika._y),2)
		if self.sta==0 and self.t>600:
			mika.sheng+=1
			return False
		if self.t<1500 and (self.sta==0 or math.sqrt(v_dist(mika._x,mika._y,self.x,self.y))>50):
			return True
		else:
			mika.sheng+=1
			return False

class danmu_q():
	def __init__(self,x,y,dx,dy,z):
		self._x,self._y,self.dx,self.dy = x,y,dx,dy
		self.friend=1
		self.type=1
		self.r=4
		self.gong=1
		self.speed=0.6
		self.img = p_img("pics/q.png",16,6)
		self.img = pygame.transform.rotate(self.img,rota(dx,dy))
		self.hid=z
		bao=random.choice(range(100))
		self.harm=mika.atk*(2 if bao<mika.crit else 1)
		self.t=0

	def run(self,timep):
		nx=self._x+self.dx*timep*self.speed
		ny=self._y+self.dy*timep*self.speed
		if yes_xy(nx,ny,1):
			self._x,self._y=nx,ny
		else:
			return False
		self.t+=timep
		return self.t<500

class danmu_w():
	def __init__(self,x):
		global mika
		self.hid=x
		self.t=0
		self.harm=int((mika.fxy[0]**2+mika.fxy[0]**2)*2+mika.atk*(1 if mika.fwing<=0 else (1+0.3*(4-mika.sheng))))
		self._x,self._y=0,0
		self.r=25
		self.friend=1
		self.type=0
		self.gong=1
	def run(self,timep):
		global mika
		self._x,self._y=mika._x,mika._y
		self.t+=timep
		return self.t<=800

class danmu_d0():
	def __init__(self,x,y,z):
		global mika,harm_id
		harm_id+=1
		self.hid=harm_id
		self.t=0
		self.harm=z
		self._x,self._y=x,y
		self.r=10
		self.friend=2
		self.type=0
		self.gong=1
		self.te=0
	def run(self,timep):
		self.t+=timep
		return self.t<=800


#*****************************************************************************************
class diji_0():
	def __init__(self,x,y,life=100,atk=25,sight=300):
		global diji_id
		diji_id+=1
		self.did=diji_id
		self._x,self._y = x,y
		self.life,self.atk=life,atk
		self.img = p_img("pics/diji_0.png",30,30)
		self.ww,self.hh=15,15
		self.harmd=[]
		self.harming=0
		self.r=15
		self.t=0
		self.sight=sight
		self.speed=0.1
		self.fuck=25
		self.cd0=0
		self.cd1=0

	def get_harm(self,x):
		global danmu
		self.life-=x
		self.img = p_img("pics/diji_01.png",30,30)
		danmu.append(danmu_piao(self._x,self._y,x))
		self.harming+=300

	def run(self,timep):
		global mika,danmu,sound
		if mika.hp<=0:
			return True
		#bian= 1 if self.harming>0 else 0
		seeing=can_see(self._x,self._y,mika._x,mika._y,self.sight)
		dis=v_dis(self._x,self._y,mika._x,mika._y)
		self.harming-=min(self.harming,timep)

		if self.harming<=0 and seeing==False:
			self.img = p_img("pics/diji_0.png",30,30)
		if dis<self.sight/2:
			self.cd1-=min(self.cd1,timep)
		else:
			self.cd1+=10 if self.cd1<1300 else 0

		self.t+=timep
		if self.t>1500:
			self.cd0+=1200
			self.cd0=min(self.cd0,2500)
			self.t=0

		if self.harming<=0 and seeing:
			if dis>self.fuck and self.cd0>0:
				self.cd0-=min(self.cd0,timep)
				vec=v_ori(self._x,self._y,mika._x,mika._y)
				nx,ny=self._x+vec[0]*self.speed*timep,self._y+vec[1]*self.speed*timep
				if yes_xy1(nx,ny,0,self.did):
					self._x,self._y=nx,ny
			elif dis<self.fuck and self.cd1<=0:
				self.cd1=2500
				vec=v_ori(self._x,self._y,mika._x,mika._y)
				nx,ny=self._x+vec[0]*12,self._y+vec[1]*12
				danmu.append(danmu_d0(mika._x,mika._y,self.atk))
				sound.sd[6].play()
				anime_ins(3,nx,ny)
		return self.life>0
		

#*****************************************************************************************
class Moji():
	def __init__(self):
		self.font=range(10)
		self.color=range(10)
		self.font[0]=pygame.font.Font("font/hanyi.ttf", 25)
		self.font[1]=pygame.font.Font("font/yuwei.ttf", 30)
		self.font[2]=pygame.font.Font("font/hanyi.ttf", 16)
		#self.conts=open("diag.txt","r").readlines()
		#self.conts=map(lambda x:unicode(x,"utf8"),self.conts)
		self.color[0]=(0,0,0)
		self.color[1]=(250,0,0)
		self.color[2]=(255,255,255)

	def rd(self,x,y,z=0):
		return self.font[x].render(unicode(y,"utf8"),True,self.color[z])

	def run(self,time_pass):
		global mika
		t0=self.rd(0,"生命：")
		t1=self.rd(0,"气体：")
		t2=self.rd(0,"攻击：")
		t3=self.rd(0,"防御：")
		t8=self.rd(0,"速度：")
		t4=self.rd(0,str(mika.hp))
		t5=self.rd(0,str(mika.gas))
		t6=self.rd(0,str(mika.atk))
		t7=self.rd(0,str(mika.dfd))
		t9=self.rd(0,str(mika.speed*10))
		screen.blit(t0,(1000,50))
		screen.blit(t1,(1000,80))
		screen.blit(t2,(1000,110))
		screen.blit(t3,(1000,140))
		screen.blit(t8,(1000,170))
		screen.blit(t4,(1080,50))
		screen.blit(t5,(1080,80))
		screen.blit(t6,(1080,110))
		screen.blit(t7,(1080,140))
		screen.blit(t9,(1080,170))

		m0=self.rd(0,"风格：")
		m1=self.rd(0,"刺客" if mika.type==0 else "三狗")
		screen.blit(m0,(1000,210))
		screen.blit(m1,(1080,210))
		m2=self.rd(0,"技能：")
		screen.blit(m2,(1000,240))
		m3=self.rd(0,mika.skill[mika.type][0],1 if mika.choose==1 else 0)
		m4=self.rd(0,mika.skill[mika.type][1],1 if mika.choose==2 else 0)
		m7=self.rd(0,mika.skill[mika.type][2],1 if mika.choose==3 else 0)
		m5=self.rd(0,str((mika.qcd[mika.type]/100)))
		m6=self.rd(0,str((mika.wcd[mika.type]/100)))
		m8=self.rd(0,str((mika.rcd[mika.type]/100)))
		screen.blit(m3,(1050,270))
		screen.blit(m4,(1050,300))
		screen.blit(m7,(1050,330))
		screen.blit(m5,(1200,270))
		screen.blit(m6,(1200,300))
		screen.blit(m8,(1200,330))

		f0=self.rd(0,"飞刀：")
		f1=self.rd(0,"暴击：")
		f2=self.rd(0,str(mika.knife))
		f3=self.rd(0,str(mika.crit))
		screen.blit(f0,(1000,370))
		screen.blit(f1,(1000,400))
		screen.blit(f2,(1080,370))
		screen.blit(f3,(1080,400))



class Anime():
	def __init__(self,x):
		src='pics/ani_'+str(x)+'_'
		self.num=1
		self.tu=[]
		self.al=0
		self.now=0
		self.aid=x
		self._x,self._y=0,0
		while os.path.exists(src+self.cal(self.num)+'.png'):
			self.tu.append(pygame.image.load(src+self.cal(self.num)+'.png').convert_alpha())
			self.num+=1
		self.num-=1

	def next(self,timep):
		global mika
		self.al+=timep
		if self.aid==1:
			self._x,self._y=mika._x-mika.ww-10,mika._y-mika.hh-10
		if self.al>=83:
			self.al=0
			self.now+=1
		return self.now<self.num

	def cal(self,x):
		if x<10:
			return '000'+str(x)
		elif x<100:
			return '00'+str(x)
		elif x<1000:
			return '0'+str(x)
		else:
			return str(x)

class Anis():
	def __init__(self):
		self.an=[]
		for i in range(4):
			self.an.append(Anime(i))

class Sound:
	def __init__(self):
		n=100
		self.sd=[]
		src='sound/sd_'
		for i in range(n):
			if os.path.exists(src+str(i)+'.wav'):
				now=pygame.mixer.Sound(src+str(i)+'.wav')
				now.set_volume(.1)
				self.sd.append(now)
			else:
				break
	

class Ziji():
	def __init__(self):
		self._w,self._h=30,30
		self.ww,self.hh=self._w/2,self._h/2
		self.im0=p_img("pics/mika2.png",self._w,self._h)
		self.img=p_img("pics/mika2.png",self._w,self._h)
		self._x,self._y=800,600
		self.tarx,self.tary=0,0
		self.dx,self.dy=0,0
		self.vx,self.vy=0,0
		self.status=0
		self.speed=0.1
		self.fpeed=0.2
		self.rot=0
		self.rpeed=1
		self.sheng=4
		self.ssp=8.5
		self.qcd,self.wcd,self.rcd=range(2),range(2),range(2)
		self.qcd[0]=self.qcd[1]=0
		self.wcd[0]=self.wcd[1]=0
		self.rcd[0]=self.rcd[1]=0
		self.anicd=0
		self.tcd=0
		self.fxy=(0,0)
		self.ftime=0
		self.fwing=0
		self.wing=0
		self.type=0
		self.pcd=150
		self.hpmax,self.gasmax,self.atk,self.dfd,self.knife,self.crit=100,100,50,10,20,5
		self.gasx=1
		self.wdis=3.5
		self.init()

	def init(self):
		self.hp,self.gas=self.hpmax,self.gasmax
		self.choose=0
		self.skill=[]
		self.ps=range(5)
		self.ps[0]=self.ps[1]=self.ps[2]=self.ps[3]=0
		for i in range(3):
			self.skill.append(range(5))
		self.skill[0][0]='飞刀'
		self.skill[0][1]='冲刺'
		self.skill[0][2]='过载'
		self.skill[1][0]='钩爪'
		self.skill[1][1]='旋转斩击'
		self.skill[1][2]='决死之心'
		self.r0_t=10000
		self.harmd=[]

	def no_speed(self):
		self.fxy=(0,0)
		self.tarx=self.tary=0	

	def get_speed(self,x,y,z):
		self.ftime+=z
		self.fxy=(self.fxy[0]+x,self.fxy[1]+y)

	def get_harm(self,x,y):
		x-=min(self.dfd,x)
		self.hp-=x
		if self.hp<=0:
			self.miss()

	def miss(self):
		pass

	def run(self,timep):
		global moup,keyp,mou_pos,danmu,sound,harm_id

		if self.hp<=0:
			return
		for i in range(2):
			self.qcd[i]-=min(timep,self.qcd[i])
			self.wcd[i]-=min(timep,self.wcd[i])
			self.rcd[i]-=min(timep,self.rcd[i])
		self.tcd-=min(timep,self.tcd)
		self.ftime-=min(timep,self.ftime)
		self.fwing-=min(timep,self.fwing)
		self.wing-=min(timep,self.wing)
		self.anicd-=min(timep,self.anicd)
		for i in range(4):
			self.ps[i]-=min(timep,self.ps[i])

		if keyp[K_TAB] and self.tcd<=0:
			self.tcd=500
			self.type^=1
			self.im0=p_img("pics/mika1.png" if self.type==1 else "pics/mika2.png",self._w,self._h)

		if keyp[K_q] and self.ps[0]<=0:
			self.ps[0]=self.pcd
			self.choose=1 if self.choose!=1 else 0
		elif keyp[K_w] and self.ps[1]<=0 and self.type==0:
			self.ps[1]=self.pcd
			self.choose=2 if self.choose!=2 else 0

		if self.type==1:
			if moup[0] and self.choose==1 and self.gas>=self.gasx and self.sheng>0 and self.qcd[1]<=0:
				self.qcd[1]=200
				self.sheng-=1
				self.gas-=self.gasx
				self.choose=0
				vec=v_ori(self._x,self._y,mou_pos[0],mou_pos[1])
				sound.sd[21].play()
				danmu.append(danmu_sheng(self._x,self._y,vec[0]*self.ssp,vec[1]*self.ssp))
				

			if keyp[K_w] and self.wcd[1]<=0:
				self.wcd[1]=1500
				sound.sd[23].play()
				self.wing+=800
				if self.status==1:
					self.fwing+=800
				harm_id+=1
				danmu.append(danmu_w(harm_id))

		elif self.type==0:
			if moup[0] and self.choose==1 and self.qcd[0]<=0 and self.knife>0:
				self.qcd[0]=2000
				self.knife-=1
				self.choose=0
				harm_id+=1
				vec=v_ori(self._x,self._y,mou_pos[0],mou_pos[1])
				danmu.append(danmu_q(self._x,self._y,vec[0],vec[1],harm_id))
				sound.sd[22].play()
			if moup[0] and self.choose==2 and self.wcd[0]<=0:
				vec=v_ori(self._x,self._y,mou_pos[0],mou_pos[1])
				self.get_speed(vec[0]*self.wdis,vec[1]*self.wdis,300)
				self.wcd[0]=7000
				self.choose=0
				sound.sd[2].play()
				anime_ins(1,self._x-self.ww-10,self._y-self.hh-10)
			if keyp[K_r] and self.rcd[0]<=0:
				self.rcd[0]=60000
				sound.sd[0].play()
				buffs.append(buff_r0())

		
		self.status=1 if self.ftime>0  and (self.fxy[0]!=0 or self.fxy[1]!=0) else 0

		if self.wing>0:
			self.rot+=timep*self.rpeed
			if self.anicd<=0:
				self.anicd=20
				anime_ins(2,self._x-self.ww-5,self._y-self.hh-5)
		else:
			self.rot=0
		self.img=pygame.transform.rotate(self.im0,self.rot)

		if self.status==1:
			self.tarx=self.tary=self.dx=self.dy=0
			nx=self._x+self.fxy[0]*timep*self.fpeed
			ny=self._y+self.fxy[1]*timep*self.fpeed
			if yes_xy(nx,ny,self.status):
				self._x,self._y=nx,ny
			else:
				self.fxy=(0,0)
				return 
		elif self.status==0:
			self.fxy=(0,0)
			if moup[2]:
				self.tarx,self.tary=mou_pos
			if self.tarx>0:
				if v_dist(self._x,self._y,self.tarx,self.tary)<10:
					self.tarx,self.tary=0,0
					self.dx,self.dy=0,0
				else:
					vec=v_make(self._x,self._y,self.tarx,self.tary)
					spe=math.sqrt(v_dist(self._x,self._y,self.tarx,self.tary))
					self.dx,self.dy=vec[0]*self.speed/spe,vec[1]*self.speed/spe
			if self.dx!=0 or self.dy!=0:
				nx=self._x+self.dx*timep
				ny=self._y+self.dy*timep
				if yes_xy0(nx,ny,self.status):
					self._x,self._y=nx,ny

		
		#screen.blit(self.img,(self._x-self.ww,self._y-self.hh))

class Rule():
	def dline(self):
		global bod_lines
		for i in bod_lines:
			pygame.draw.line(screen,0x666666,(i[0],i[1]),(i[2],i[3]))

	global moji
	def run(self,timep):
		global danmu,animes,buffs,dijis,mika,bk,ak

		screen.fill(0)
		screen.blit(bk,(boder[0],boder[2]))
		screen.blit(ak,(960,20))

		danmu=filter(lambda x:x.run(timep),danmu)
		animes=filter(lambda x:x.next(timep),animes)
		buffs=filter(lambda x:x.run(timep),buffs)
		dijis=filter(lambda x:x.run(timep),dijis)
		map(lambda x:screen.blit(x.tu[x.now],(x._x,x._y)),animes)
		map(lambda x:screen.blit(x.img,(x._x-x.ww,x._y-x.hh)),dijis)
		map(lambda x:screen.blit(x.img,(x._x,x._y)) if x.type!=0 else 0,danmu)

		for i in filter(lambda x:x.gong==1 and x.friend==2,danmu):
			if v_dis(i._x,i._y,mika._x,mika._y)<=i.r+mika.ww and (i.hid not in mika.harmd):
				mika.harmd.append(i.hid)
				mika.get_harm(i.harm,i.te)

		for i in filter(lambda x:x.gong==1 and x.friend==1,danmu):
			for j in dijis:
				if v_dis(i._x,i._y,j._x,j._y)<=i.r+j.r and (i.hid not in j.harmd):
					j.harmd.append(i.hid)
					j.get_harm(i.harm)

		if mika.hp>0:
			screen.blit(mika.img,(mika._x-mika.ww,mika._y-mika.hh))
		moji.run(time_pass)

class Story():
	def __init__(self):
		self.event=1

	def read_map(self,fp):
		global bod_lines
		bod_init()
		for i in fp:
			if len(i)>1:
				j=i.split(' ')
				bod_lines.append((int(j[0]),int(j[1]),int(j[2]),int(j[3]),int(j[4])))

	def run(self,timep):
		global bod_lines,bk,dijis,mika,danmu

		if self.event==1:
			self.event=2
			mika._x,mika._y=800,600
			bk=j_img('pics/map0.jpg',900,680)
			self.read_map(open('misson/m0.txt').readlines())
			danmu.append(danmu_tar(50,30))
			dijis.append(diji_0(400,600,300))
			dijis.append(diji_0(200,250,300))
			dijis.append(diji_0(100,150,300))
			dijis.append(diji_0(580,400,300))

		if self.event==2:
			if len(dijis)<=0 and mika._x<=90 and mika._y<=60:
				self.event+=1
				bk=j_img('pics/map1.jpg',900,680)
				self.read_map(open('misson/m1.txt').readlines())
				dijis=[]
				danmu=[]
				mika.no_speed()
				mika._x,mika._y=850,650
				dijis.append(diji_0(120,650,200))
				dijis.append(diji_0(520,450,200,sight=220))
				dijis.append(diji_0(520,550,200,sight=250))
				dijis.append(diji_0(630,450,200,sight=200))
				dijis.append(diji_0(620,550,200,sight=250))
				dijis.append(diji_0(780,370,200))
				dijis.append(diji_0(290,120,200,sight=250))
				dijis.append(diji_0(290,200,200,sight=250))
				dijis.append(diji_0(380,150,200,sight=250))
				dijis.append(diji_0(600,130,250))
				dijis.append(diji_0(700,230,250))
				dijis.append(diji_0(800,130,250))

class Maap():
	def run(self):
		global mcd,g,ls,rx,fp,mou_pos,moup
		mcd-=min(mcd,time_pass)
		if moup[0] and mcd<=0:
			mcd=500
			g+=1
			if g==1:
				ls=mou_pos
			else:
				g=0
				rx=mou_pos
				li=str(ls[0])+' '+str(ls[1])+' '+str(ls[0])+' '+str(rx[1])+' 1\n'
				print li
				fp.write(li)
				li=str(ls[0])+' '+str(ls[1])+' '+str(rx[0])+' '+str(ls[1])+' 1\n'
				fp.write(li)
				li=str(rx[0])+' '+str(rx[1])+' '+str(ls[0])+' '+str(rx[1])+' 1\n'
				fp.write(li)
				li=str(rx[0])+' '+str(rx[1])+' '+str(rx[0])+' '+str(ls[1])+' 1\n'
				fp.write(li)
			print mou_pos


#*****************************************************************************************
mapping 	= 	0
ls,rx		=	(0,0),(0,0)
clock 		= 	pygame.time.Clock()
mika 		=	Ziji()
story 		=	Story()
guize		= 	Rule()
sound 		=	Sound()
moji 		= 	Moji()
anis 		=	Anis()
maap 		= 	Maap()
#********************************** main *************************************************
while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			exit()

	keyp=pygame.key.get_pressed()
	moup=pygame.mouse.get_pressed()
	mou_pos=pygame.mouse.get_pos()
	time_pass = clock.tick(120)

	if keyp[K_z]:
		exit()		

	if mapping==1:
		maap.run()
	else:
		mika.run(time_pass)
		story.run(time_pass)
		guize.run(time_pass)

	
	pygame.display.update()