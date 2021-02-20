import pygame
import os
from glob import glob
import sys
import time
from mutagen.mp3 import MP3
import Sound
from datetime import datetime, timedelta
import random, math
import os.path
from threading import Thread
from PlayList import PlayList
from Button import Button
from OnlineMusic import OnlineMusic

pygame.init()
clock = pygame.time.Clock()

win = pygame.display.set_mode( (250,400) )
pygame.display.set_caption("Music")
path_for_image = os.path.normpath(os.getcwd() + os.sep + os.pardir) + "\\images" #'D:\\python\\player\\images'
pygame.display.set_icon(pygame.image.load(path_for_image + "\\icon.png"))


#a class for creating song buttons and finding them
music_list = []
music_class_list = []
peremotka = 1
class Dict():

	def __init__(self, x, y, text, index_num):
		global Theme
		self.x = x
		self.y = y	
		self.text = text
		self.index_num = index_num
		try:
			self.font = font_type.render( self.text, True, (0,0,0) )
		except UnicodeError:
			self.font = None
		self.Theme = "wite"

	#drawing buttons to select any song
	def music_button(self, win=win):
		global num_music, text_x, peremotka_on, music_list, music_time_now_test, Theme
		height = 28

		keys = pygame.key.get_pressed()

		if self.y + height >= 50 and self.y + height <= 250:
			text = str(self.index_num + 1) + ". " + self.text

			if Theme == 'gradient':
				self.font_color = (0,0,0)
			if Theme == 'dark':
				self.font_color = (255,255,255)
			if Theme == 'white':
				self.font_color = (0,0,0)

			pygame.draw.rect( win, self.font_color, (self.x,self.y + height - 2,220,1) )

			try:
				if Theme != self.Theme or self.font.get_size()[0] > 220 or self.font == None:
					self.Theme = Theme
					font_type = pygame.font.Font( shrift, 16 )
					self.font = font_type.render( text, True, self.font_color )

					if self.font.get_size()[0] > 220:
						self.text = self.text[:-1]

				win.blit( self.font, (self.x,self.y + 7) )
			except UnicodeError:
				self.text = str(self.index_num + 1) + ". "
				text = str(self.index_num + 1) + ". " + self.text
				self.font = font_type.render( text, True, self.font_color )



		keys = pygame.key.get_pressed()
		pos = pygame.mouse.get_pos()
		mouse_x, mouse_y = pos[0], pos[1]
		MOUSE_CLICK = pygame.mouse.get_pressed()
	#	print( str(mouse_x) + " " + str(mouse_y) )

		#moving buttons and handling keystrokes
		if mouse_x >= self.x and mouse_x <= self.x + 220 and mouse_y >= 50 and mouse_y <= 250:
			
			Dict.roll_mouse_wheel()

			if mouse_y >= self.y and mouse_y <= self.y + height and MOUSE_CLICK[0] == 1:
				music_list = sorted(music_list2)
				num_music = self.index_num
				peremotka_on = False
				music_time_now_test = 0
				text_x = 10
				play_music()

	#scrolling songs
	def roll_mouse_wheel():
		height = 28
		keys = pygame.key.get_pressed()

		for i in pygame.event.get():

			if i.type == pygame.MOUSEBUTTONDOWN:

				if i.button == 4:
					for liste in music_class_list:	
						liste.y += height
						if liste.index_num - 1 < 0 and liste.y > 50:
							for liste in music_class_list:
								liste.y -= height

				if i.button == 5:
					for liste in music_class_list:
						liste.y -= height
						if liste.index_num + 2 > len(music_class_list) and liste.y + height < 230:
							for liste in music_class_list:
								liste.y += height

		if keys[pygame.K_UP]:
			for liste in music_class_list:
				liste.y += height
				if liste.index_num - 1 < 0 and liste.y > 50:
					for liste in music_class_list:
						liste.y -= height
								

		if keys[pygame.K_DOWN]:
			for liste in music_class_list:
				liste.y -= height
				if liste.index_num + 2 > len(music_class_list) and liste.y + height < 230:
					for liste in music_class_list:
						liste.y += height


	#search all music files
	def catalog():
		music_list = []

		name = os.getenv('USERPROFILE')
		
		for file in glob(name + '\\Music\\*.mp3'):
			music_list.append(file)

		for file in glob(name + '\\Download\\*.mp3'):
			music_list.append(file)

		if os.path.exists(name + '\\OnlineMusic') == True:
			for file in glob(name + '\\OnlineMusic\\*.mp3'):
				music_list.append(file)

		# search in all directories that are in this tuple
		dicter = ('A', 'B', 'D', 'E', 'F','G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z')	
		for dicte in dicter:
			if os.path.exists(dicte + ':/') == True:
				for rootdir, dirs, files in os.walk(dicte + ':\\'):
					for file in files:
						if file.split('.')[-1] =='mp3':
							music_list.append(os.path.join(rootdir, file))
		
		return music_list



def vertical(size, startcolor, endcolor):
    """
    Draws a vertical linear gradient filling the entire surface. Returns a
    surface filled with the gradient (numeric is only 2-3 times faster).
    """
    height = size[1]
    bigSurf = pygame.Surface( (1,height) ).convert_alpha()
    dd = 1.0/height
    sr, sg, sb, sa = startcolor
    er, eg, eb, ea = endcolor
    rm = (er-sr)*dd
    gm = (eg-sg)*dd
    bm = (eb-sb)*dd
    am = (ea-sa)*dd
    for y in range(height):
        bigSurf.set_at((0,y),
                        (int(sr + rm*y),
                         int(sg + gm*y),
                         int(sb + bm*y),
                         int(sa + am*y))
                      )
    return pygame.transform.scale(bigSurf, size)


# a one-time loop to load an image and fill the list with music using the Dict.catalog () function
load = True
next_button = None
last_button = None
pause_button = None
play_button = None
peremeshat1 = None
peremeshat2 = None
povtor1 = None
povtor2 = None
playlistimg = None
internet = None
back_ground = None
while load:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

	start = pygame.transform.scale(pygame.image.load(path_for_image + "/playerBG.png"), (250, 400)).convert_alpha()
	win.blit(start, (0,0))
	pygame.draw.rect(win, (104,104,104), (20,380,210, 10))
	pygame.display.update()

	#------------gradient---------------
	next_button_gradient = pygame.transform.scale(pygame.image.load(path_for_image + "/next.png"), (35, 35)).convert_alpha()
	last_button_gradient = pygame.transform.scale(pygame.image.load(path_for_image + "/last.png"), (35, 35)).convert_alpha()

	pygame.draw.rect(win, (0,255,0), (20,380,20, 10))
	pygame.display.update()

	pause_button_gradient = pygame.transform.scale(pygame.image.load(path_for_image + "/pause.png"), (35, 35)).convert_alpha()
	play_button_gradient = pygame.transform.scale(pygame.image.load(path_for_image + "/play.png"), (50, 40)).convert_alpha()

	pygame.draw.rect(win, (0,255,0), (20,380,70, 10))
	pygame.display.update()

	peremeshat1_gradient = pygame.transform.scale(pygame.image.load(path_for_image + "/peremeshat1.png"), (25, 25)).convert_alpha()
	peremeshat2_gradient = pygame.transform.scale(pygame.image.load(path_for_image + "/peremeshat2.png"), (25, 25)).convert_alpha()

	pygame.draw.rect(win, (0,255,0), (20,380,120, 10))
	pygame.display.update()

	povtor1_gradient = pygame.transform.scale(pygame.image.load(path_for_image + "/povtor1.png"), (30, 30)).convert_alpha()
	povtor1_gradient = pygame.transform.flip(povtor1_gradient, True, False)
	povtor2_gradient = pygame.transform.scale(pygame.image.load(path_for_image + "/povtor2.png"), (30, 30)).convert_alpha()
	playlistimg_gradient = pygame.transform.scale(pygame.image.load(path_for_image + "/playlist.png"), (29, 29)).convert_alpha()
	internet_gradient = pygame.transform.scale(pygame.image.load(path_for_image + "/internet.png"), (32, 32)).convert_alpha()
	back_ground_gradient = vertical((250,400), (0, 255,255,255), (0,255,0,255))
	#-------------gradient------------
	

	#-------------white Theme----------
	back_ground_white = pygame.image.load(path_for_image + '/back_groundw.jpg')
	next_button_white = pygame.transform.scale(pygame.image.load(path_for_image + "/nextd.png"), (35, 35)).convert_alpha()
	last_button_white = pygame.transform.scale(pygame.image.load(path_for_image + "/lastd.png"), (35, 35)).convert_alpha()
	pause_button_white = pygame.transform.scale(pygame.image.load(path_for_image + "/paused.png"), (35, 35)).convert_alpha()
	play_button_white = pygame.transform.scale(pygame.image.load(path_for_image + "/playd.png"), (35, 35)).convert_alpha()
	peremeshat1_white = pygame.transform.scale(pygame.image.load(path_for_image + "/peremeshat1.png"), (25, 25)).convert_alpha()
	peremeshat2_white = pygame.transform.scale(pygame.image.load(path_for_image + "/peremeshat2.png"), (25, 25)).convert_alpha()
	povtor1_white = pygame.transform.scale(pygame.image.load(path_for_image + "/povtor1.png"), (30, 30)).convert_alpha()
	povtor1_white = pygame.transform.flip(povtor1_white, True, False)
	povtor2_white = pygame.transform.scale(pygame.image.load(path_for_image + "/povtor2.png"), (30, 30)).convert_alpha()
	playlistimg_white = pygame.transform.scale(pygame.image.load(path_for_image + "/playlist.png"), (29, 29)).convert_alpha()
	internet_white = pygame.transform.scale(pygame.image.load(path_for_image + "/internet.png"), (32, 32)).convert_alpha()

	#-------------white Theme----------


	#-------------dark Theme----------
	back_ground_dark = pygame.image.load(path_for_image + '/back_ground.jpg')
	next_button_dark = pygame.transform.scale(pygame.image.load(path_for_image + "/nextw.png"), (35, 35)).convert_alpha()
	last_button_dark = pygame.transform.scale(pygame.image.load(path_for_image + "/lastw.png"), (35, 35)).convert_alpha()
	pause_button_dark = pygame.transform.scale(pygame.image.load(path_for_image + "/pausew.png"), (35, 35)).convert_alpha()
	play_button_dark = pygame.transform.scale(pygame.image.load(path_for_image + "/playw.png"), (35, 35)).convert_alpha()
	peremeshat1_dark = pygame.transform.scale(pygame.image.load(path_for_image + "/peremeshat1w.png"), (25, 25)).convert_alpha()
	peremeshat2_dark = pygame.transform.scale(pygame.image.load(path_for_image + "/peremeshat2w.png"), (25, 25)).convert_alpha()
	povtor1_dark = pygame.transform.scale(pygame.image.load(path_for_image + "/povtor1w.png"), (30,30)  ).convert_alpha()
	povtor1_dark = pygame.transform.flip(povtor1_dark, True, False)
	povtor2_dark = pygame.transform.scale(pygame.image.load(path_for_image + "/povtor2w.png"), (30, 30)).convert_alpha()
	playlistimg_dark = pygame.transform.scale(pygame.image.load(path_for_image + "/playlistw.png"), (29, 29)).convert_alpha()
	internet_dark = pygame.transform.scale(pygame.image.load(path_for_image + "/internetw.png"), (32, 32)).convert_alpha()
	#-------------dark Theme----------


	pygame.draw.rect(win, (0,255,0), (20,380,150, 10))
	pygame.display.update()

	shrift = "C:/Windows/Fonts/Calibri.ttf"

	pygame.draw.rect(win, (0,255,0), (20,380,190, 10))
	pygame.display.update()

	music_list = Dict.catalog()
	pygame.draw.rect(win, (0,255,0), (20,380,200, 10))
	pygame.display.update()
	music_list2 = sorted(music_list)
	load = False
	pygame.draw.rect(win, (0,255,0), (20,380,210, 10))
	pygame.display.update()


#function to change theme
Theme = 'gradient'
def Themes():
	global Themes, next_button, last_button, pause_button, play_button, peremeshat1, peremeshat2, povtor1, povtor2, playlistimg, internet, back_ground

	if Theme == 'gradient':
		next_button = next_button_gradient
		last_button = last_button_gradient
		pause_button = pause_button_gradient
		play_button = play_button_gradient
		peremeshat1 = peremeshat1_gradient
		peremeshat2 = peremeshat2_gradient
		povtor1 = povtor1_gradient
		povtor2 = povtor2_gradient
		playlistimg = playlistimg_gradient
		internet = internet_gradient
		back_ground = back_ground_gradient
	if Theme == 'dark':
		next_button = next_button_dark
		last_button = last_button_dark
		pause_button = pause_button_dark
		play_button = play_button_dark
		peremeshat1 = peremeshat1_dark
		peremeshat2 = peremeshat2_dark
		povtor1 = povtor1_dark
		povtor2 = povtor2_dark
		playlistimg = playlistimg_dark
		internet = internet_dark
		back_ground = back_ground_dark
	if Theme == 'white':
		next_button = next_button_white
		last_button = last_button_white
		pause_button = pause_button_white
		play_button = play_button_white
		peremeshat1 = peremeshat1_white
		peremeshat2 = peremeshat2_white
		povtor1 = povtor1_white
		povtor2 = povtor2_white
		playlistimg = playlistimg_white
		internet = internet_white
		back_ground = back_ground_white
Themes()


# renders all objects stored in music_class_list
num = 0
def make_list_win():
	global num
	height = 28
	y = 50

	if num < len(music_list2):
		for liste in music_list2:
			music_title = os.path.basename(music_list2[num])
			music_title_print = music_title.rstrip('.mp3')		

			music_class_list.append(Dict(15,y, music_title_print, num))
			y += height
			num += 1
	
	for liste in music_class_list:
		if liste.y + height >= 78 and liste.y + height <= 250: 
			liste.music_button()

#draws a pause button and tracks its pressing and its actions
pause_on = False
btn_pause = Button.round_button(win,125,320,22, (0,0,0))
def pause():
	global pause_on, btn_pause
	keys = pygame.key.get_pressed()

	if pause_on ==False:
		pause_button_on = pause_button
	if pause_on == True:
		pause_button_on = play_button

	win.blit(pause_button_on,(107,302))

	btn_pause_on = Button.click_button_round(btn_pause)
	if btn_pause_on == True and pause_on == False:
		pause_on = True
		btn_pause_on = False
		pygame.mixer.music.pause()
		time.sleep(0.3)

	elif btn_pause_on == True and pause_on == True:
		pause_on = False
		pygame.mixer.music.unpause()	
		time.sleep(0.3)

	if keys[pygame.K_2] and pause_on == False:
		pause_on = True
		btn_pause_on = False
		pygame.mixer.music.pause()
		time.sleep(0.3)

	elif keys[pygame.K_2] and pause_on == True:
		pause_on = False
		pygame.mixer.music.unpause()	
		time.sleep(0.3)	

#buttons for switching tracks
def button_last_on():
	global peremotka, num_music, pause_on, text_x, povtor_on, music_time_now_test

	peremotka = -1
	num_music += peremotka
	pause_on = False
	time.sleep(0.3)
	text_x = 10
	music_time_now_test = 0
	if povtor_on == True:
		peremotka = 0
	if num_music < 0:
		num_music = len(music_list)
		num_music += peremotka
	play_music()

def button_next_on():
	global peremotka, num_music, pause_on, text_x, music_time_now_test, povtor_on

	peremotka = 1
	num_music += peremotka
	pause_on = False
	text_x = 10
	time.sleep(0.3)
	music_time_now_test = 0
	if povtor_on == True:
		peremotka = 0
	if num_music > len(music_list) - 1:
		num_music =0
	play_music()

#shuffle button
peremotka_on = False
btn_random = Button.round_button(win,190, 370, 15, (0,0,0), 1)
def random_list():
	global peremotka_on, pause_on, num_music, music_list, text_x, peremotka, music_time_now_test, btn_random

	keys = pygame.key.get_pressed()

	if peremotka_on == False:
		peremotkaimg = peremeshat1
	if peremotka_on == True:
		peremotkaimg = peremeshat2
	win.blit(peremotkaimg, (178,357))

	btn_random_on = Button.click_button_round(btn_random)
	if btn_random_on == True and peremotka_on == False:
		peremotka_on = True
		random.shuffle(music_list)
		peremotka = 1
		play_music()
		text_x = 10
		music_time_now_test = 0
		pause_on = False
		time.sleep(0.3)

	elif btn_random_on == True and peremotka_on == True:
		peremotka_on = False
		music_list = sorted(music_list)
		peremotka = 1
		num_music =0 
		play_music()
		text_x = 10
		music_time_now_test = 0
		pause_on = False
		time.sleep(0.3)

	if keys[pygame.K_5] and peremotka_on == False:
		peremotka_on = True
		random.shuffle(music_list)
		peremotka = 1
		play_music()
		text_x = 10
		music_time_now_test = 0
		pause_on = False
		time.sleep(0.3)

	elif keys[pygame.K_5] and peremotka_on == True:
		peremotka_on = False
		music_list = sorted(music_list)
		peremotka = 1
		num_music =0 
		play_music()
		text_x = 10
		music_time_now_test = 0
		pause_on = False
		time.sleep(0.3)

#repeat button
povtor_on = False
btn_povtor = Button.round_button(win,49, 370, 15, (0,0,0),1)
def povtor():
	global povtor_on, peremotka, btn_povtor

	keys = pygame.key.get_pressed()


	if povtor_on == False:
		povtoimg = povtor1
	if povtor_on == True:
		povtoimg = povtor2
	win.blit(povtoimg, (35, 355))

	btn_povtor_on = Button.click_button_round(btn_povtor)
	if btn_povtor_on == True and povtor_on == False:
		povtor_on = True
		peremotka = 0
		time.sleep(0.3)

	elif btn_povtor_on == True and povtor_on == True:
		povtor_on = False
		peremotka = 1
		time.sleep(0.3)

	if keys[pygame.K_4] and povtor_on == False:
		povtor_on = True
		peremotka = 0
		time.sleep(0.3)

	elif keys[pygame.K_4] and povtor_on == True: 
		povtor_on = False
		peremotka = 1
		time.sleep(0.3)


	if peremotka == 1 or peremotka == -1:
		povtor_on = False


#draws rewind buttons, is responsible for pressing and action of rewind and forward buttons
def Art():
	global Theme
	keys = pygame.key.get_pressed()

	if keys[pygame.K_q]:
		Theme = 'gradient'
		Themes()
		pygame.display.update()
	if keys[pygame.K_w]:
		Theme = "white"
		Themes()
		pygame.display.update()
	if keys[pygame.K_e]:
		Theme = 'dark'
		Themes()
		pygame.display.update()


	btn_last = Button.round_button(win,40,320, 22, (0,0,0))
	btn_next = Button.round_button(win,210,320,22,(0,0,0))

	win.blit(back_ground, (0,0))

	make_list_win()
	
	win.blit(last_button, (22,303))
	win.blit(next_button,(195,303))

	btn_last_on = Button.click_button_round(btn_last)
	if btn_last_on == True:
		button_last_on()
	if keys[pygame.K_1]:
		button_last_on()
		

	btn_next_on = Button.click_button_round(btn_next)
	if btn_next_on == True:
		button_next_on()
	if keys[pygame.K_3]:
		button_next_on()

	random_list()
	povtor()
	pause()
	Art_text()
	polzunok_volume()
	music_line()

#runs the playlist class
btn_playlist = Button.round_button(win, 15, 370, 15, (0,0,0), 1)
def playlist():
	global text_x, num_music, music_list, peremotka_on, music_time_now_test, btn_playlist, Theme

	keys = pygame.key.get_pressed()

	win.blit(playlistimg, (2,357))
	if Button.click_button_round(btn_playlist) == True: 
		playliste = True
		pygame.mixer.music.pause()
		music_time_now_test = 0
		PlayList.Themes(Theme)

		#loop for drawing playlists
		while playliste:
			#run the playlist class
			PlayList.main(win, music_list2)

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					OnlineMusic.clear_cash()
					sys.exit()

			#tracking button press to exit loop
			if PlayList.exite(win) == True :
				decore()
				text_x = 10
				playliste = False

			#get the contents of the playlist
			music_listp = PlayList.retturn() 

			#if the playlist is not empty then we start playing it
			if music_listp != None:
				if peremotka_on == True:
					peremotka_on = False
				num_music = 0
				music_list = sorted(music_listp)
				time.sleep(0.3)
				decore()
				text_x = 10
				playliste = False

			clock.tick(20)
			pygame.display.update()

#function includes music from the Internet
btn_internet = Button.round_button(win, 225, 370, 15, (0,0,0), 1)
def online():
	global music_time_now_test, text_x, btn_internet, Theme

	keys = pygame.key.get_pressed()

	onlinem = False

	win.blit(internet, (208,354))

	if Button.click_button_round(btn_internet) == True:
		music_time_now_test = 0
		pygame.mixer.music.stop()
		onlinem = True
		OnlineMusic.Themes(Theme)

		while onlinem:

			OnlineMusic.main(win)

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					OnlineMusic.clear_cash()
					sys.exit()

			if OnlineMusic.exite(win) == True:
				decore()
				text_x = 10
				music_list.clear()
				Dict.catalog()
				onlinem = False


			pygame.display.update()


# progress bar for playing music
music_time_now_test = 0
def music_line():
	global num_music, peremotka, text_x, povtor_on, music_time_now_test

	if len(music_list) > 0:

		keys = pygame.key.get_pressed()

		#tracking current song length and full song length
		try:
			music_time = MP3(music_list[num_music]).info.length
			music_time_now = music_time_now_test + round(pygame.mixer.music.get_pos() / 1000, 2)
		except Exception:
			num_music += peremotka
			decore()

		pos = pygame.mouse.get_pos()
		mouse_x, mouse_y = pos[0], pos[1]
		MOUSE_CLICK = pygame.mouse.get_pressed()

		#percentage to fill the progress bar
		proc = music_time / 100
		proc = round(music_time_now / proc )
		proc = proc * 2
		music_line_round_x = 20 + proc



		pygame.draw.rect(win,(104,104,104), (20, 270,200,5))
		pygame.draw.circle(win,(255,0,0),(music_line_round_x, 272), 8)


		#tracking the end of a track
		if round(music_time_now) >= math.floor(music_time):
			music_time_now_test = 0
			if povtor_on == True:
				peremotka = 0
			num_music += peremotka
			text_x = 10
			play_music()


		if music_line_round_x > 20:
			pygame.draw.rect(win, (255,0,0), (20, 270,music_line_round_x - 20 , 5))

		#setting a track at a specific second
		if mouse_x >= 20 and mouse_x <= 220 and mouse_y >= 265 and mouse_y <= 275:
			procen = (mouse_x - 20)
			procen = procen * music_time / 100 / 2

			secondes3 = timedelta(seconds=procen)
			timer3 = datetime(1,1,1) + secondes3
			print_text(str(timer3.minute) + ":" + str(timer3.second), mouse_x - 20, 255)

			if MOUSE_CLICK[0] == 1:
				music_time_now_test = procen
				music_time_now = music_time_now_test + round(pygame.mixer.music.get_pos() / 1000 / 60, 2)

				pygame.mixer.music.stop()
				pygame.mixer.music.play(-1,round(procen))
				time.sleep(0.2)


		try:
			secondes1 = timedelta(seconds=music_time_now)
			timer1 = datetime(1,1,1) + secondes1

			secondes2 = timedelta(seconds=music_time)
			timer2 = datetime(1,1,1) + secondes2

			print_text(str(timer1.minute) + ":" + str(timer1.second), 20, 278, font_size = 15)
			print_text(str(timer2.minute) + ":" + str(timer2.second), 200, 278, font_size=15)
		except OverflowError:
			pass


#song title stamp	
text_x = 10
font_type = pygame.font.Font(shrift, 20)
def Art_text():
	global num_music, text_x, font_type,Theme
	text_x_test = 10

	if len(music_list) > 0:
		if Theme == 'gradient':
			text_color = (0,0,0)
		if Theme == 'dark':
			text_color = (255,255,255)
		if Theme == 'white':
			text_color = (0,0,0)

		#get song title
		text_window_print = os.path.basename(music_list[num_music])
		text_window_print1 = text_window_print.rstrip('.mp3')

		try:
			text = font_type.render(text_window_print1, True, (text_color))
			win.blit(text, (text_x,10))


			if text_x + text.get_size()[0] > 250 or text_x <= 0:
				text_x -= 1

			if text_x + text.get_size()[0] <=0:
				text_x = 251
			if text_x_test+ text.get_size()[0] < 250:
				text_x = 10
		except UnicodeError:
			pass
	else:
		print_text("Tracks not found", 10, 10)



#playing all music
num_music = 0
def play_music():
	global num_music, peremotka, music_list

	try:
		if len(music_list) > 0:
			pygame.mixer.music.load(music_list[num_music])
			pygame.mixer.music.play(-1)
	except Exception:
		num_music += peremotka


def print_text(massage, x, y, font_color=(0,0,0), font_type=None, font_size=20):
	global Theme
	if Theme == 'gradient':
		font_color = (0,0,0)
	if Theme == 'dark':
		font_color = (255,255,255)
	if Theme == 'white':
		font_color = (0,0,0)

	if font_type == None:
		font_type = pygame.font.Font(shrift, font_size)
	text = font_type.render(massage, True, font_color)
	win.blit(text, (x,y))


#lider to adjust volume
polzunok_volume_round_x= 115
def polzunok_volume():
	global polzunok_volume_round_x, Theme

	if Theme == 'gradient' or Theme == 'white':
		polzunok_color = (0,0,0)
	if Theme == 'dark':
		polzunok_color = (255,255,255)

	pygame.draw.rect(win, (105,105,105), (70, 370,100, 5))
	pygame.draw.circle(win, polzunok_color,  (polzunok_volume_round_x,372), 8)	
	
	if polzunok_volume_round_x >= 70:
		polzunok_volume_round_x = Sound.Sound.current_volume() + 70
		pygame.draw.rect(win, polzunok_color, (70, 370,polzunok_volume_round_x - 70 , 5))


	pos = pygame.mouse.get_pos()
	mouse_x, mouse_y = pos[0], pos[1]
	MOUSE_CLICK = pygame.mouse.get_pressed()

	if mouse_x >= 70 and mouse_x <= 170 and mouse_y >= 368 and mouse_y <= 378:
		if MOUSE_CLICK[0] == 1:
			polzunok_volume_round_x = mouse_x
			print_text(str(mouse_x - 70), mouse_x - 15, 376)
			Sound.Sound.volume_set(mouse_x - 70 + 2)

	keys = pygame.key.get_pressed()


	if polzunok_volume_round_x < Sound.Sound.current_volume():
		polzunok_volume_round_x += 1

	if polzunok_volume_round_x > Sound.Sound.current_volume():
		polzunok_volume_round_x -= 1

	if polzunok_volume_round_x < 70:
		polzunok_volume_round_x = 70


#main loop
def decore():
	global num_music
	play_music()
	while True:	
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				OnlineMusic.clear_cash()
				sys.exit()

		try:
			Art()	
		except Exception:
			num_music += 1
			play_music()

		playlist()
		online()
		clock.tick(25)
		pygame.display.update()


decore()
pygame.quit()