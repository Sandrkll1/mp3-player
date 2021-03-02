import pygame
import requests
from bs4 import BeautifulSoup as BS
from Button import Button
import time, sys, os, os.path
from mutagen.mp3 import MP3
from datetime import datetime, timedelta
import random, math, glob, shutil
import Sound

pygame.font.init()
clock = pygame.time.Clock()

screen = pygame.Surface((250, 400))

def vertical(size, startcolor, endcolor):
    """
    Draws a vertical linear gradient filling the entire surface. Returns a
    surface filled with the gradient (numeric is only 2-3 times faster).
    """
    height = size[1]
    bigSurf = pygame.Surface((1,height))
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
gradient = vertical((250,400), (0, 255,255,255), (0,255,0,255))


back2 = None
next_button = None
last_button = None
pause_button = None
play_button = None
search = None
peremeshat1 = None
peremeshat2 = None
povtor1 = None
povtor2 = None
back_ground = None
path_for_image = os.path.normpath(os.getcwd() + os.sep + os.pardir) + "\\images" #'D:\\python\\player\\images'
#------------gradient------------

shrift = "C:/Windows/Fonts/Calibri.ttf"
back2_gradient = pygame.transform.scale(pygame.image.load(path_for_image + "/back2.png"), (30,25))
next_button_gradient = pygame.transform.scale(pygame.image.load(path_for_image + "/next.png"), (35,35) )
last_button_gradient = pygame.transform.scale(pygame.image.load(path_for_image + "/last.png"),(35,35) )
pause_button_gradient = pygame.transform.scale(pygame.image.load(path_for_image + "/pause.png"), (35,35)  )
play_button_gradient = pygame.transform.scale(pygame.image.load(path_for_image + "/play.png"), (35,35)  )
search_gradient = pygame.transform.scale(pygame.image.load(path_for_image + "/search.png"), (30,30))
peremeshat1_gradient = pygame.transform.scale(pygame.image.load(path_for_image + "/peremeshat1.png"), (25,25)  )
peremeshat2_gradient = pygame.transform.scale(pygame.image.load(path_for_image + "/peremeshat2.png"), (25,25)  )
povtor1_gradient = pygame.transform.scale(pygame.image.load(path_for_image + "/povtor1.png"), (30,30)  )
povtor1_gradient = pygame.transform.flip(povtor1_gradient, True, False)
povtor2_gradient = pygame.transform.scale(pygame.image.load(path_for_image + "/povtor2.png"), (30,30)  )
back_ground_gradient = vertical((250,400), (0, 255,255,255), (0,255,0,255))

#-------------gradient-----------


#-------------white--------------

back2_white = back2_gradient
next_button_white = pygame.transform.scale(pygame.image.load(path_for_image + "/nextd.png"), (35,35) )
last_button_white = pygame.transform.scale(pygame.image.load(path_for_image + "/lastd.png"),(35,35) )
pause_button_white = pygame.transform.scale(pygame.image.load(path_for_image + "/paused.png"), (35,35)  )
play_button_white = pygame.transform.scale(pygame.image.load(path_for_image + "/playd.png"), (35,35)  )
search_white = search_gradient
peremeshat1_white = peremeshat1_gradient
peremeshat2_white = peremeshat2_gradient
povtor1_white = povtor1_gradient
povtor2_white = povtor2_gradient
back_ground_white = pygame.image.load(path_for_image + "/back_ground_onlinew.jpg")

#-------------white--------------


#-------------dark---------------

back2_dark = pygame.transform.scale(pygame.image.load(path_for_image + "/back2w.png"), (30,25))
next_button_dark = pygame.transform.scale(pygame.image.load(path_for_image + "/nextw.png"), (35,35) )
last_button_dark = pygame.transform.scale(pygame.image.load(path_for_image + "/lastw.png"),(35,35) )
pause_button_dark = pygame.transform.scale(pygame.image.load(path_for_image + "/pausew.png"), (35,35)  )
play_button_dark = pygame.transform.scale(pygame.image.load(path_for_image + "/playw.png"), (35,35)  )
search_dark = pygame.transform.scale(pygame.image.load(path_for_image + "/searchw.png"), (30,30))
peremeshat1_dark = pygame.transform.scale(pygame.image.load(path_for_image + "/peremeshat1w.png"), (25,25)  )
peremeshat2_dark = pygame.transform.scale(pygame.image.load(path_for_image + "/peremeshat2w.png"), (25,25)  )
povtor1_dark = pygame.transform.scale(pygame.image.load(path_for_image + "/povtor1w.png"), (30,30)  )
povtor1_dark = pygame.transform.flip(povtor1_dark, True, False)
povtor2_dark = pygame.transform.scale(pygame.image.load(path_for_image + "/povtor2w.png"), (30,30)  )
back_ground_dark = pygame.image.load(path_for_image + "/back_ground_onlined.jpg")

#-------------dark---------------

music_list = []
peremotka = 1


def print_text(win, massage, x, y, font_color=None, font_type=shrift, font_size=20):
	try:
		if font_color != None:
			font_color = font_color
		elif Theme == 'gradient' or Theme == 'white':
			font_color = (0,0,0)
		elif Theme == 'dark':
			font_color = (255,255,255)
		font_type = pygame.font.Font(font_type, font_size)
		text = font_type.render(massage, True, font_color)
		win.blit(text, (x,y))
	except UnicodeError:
		pass


num_music = 0
class OnlineMusic:

	#class launch
	def main(win):
		global screen
		screen = win
		OnlineMusic.clear_cash()
		parse_music()
		OnlineMusic.play_music()
		input_text(win)

	#leaving class
	def exite(win):
		global play_lists_y, music_list, num

		btn_back = Button.rect_button(win, 0, 0, 50 ,50, (0,255,240))
		if Button.click_button_rect(btn_back) == True: 
			music_list = []
			num = 0
			return True
			OnlineMusic.clear_cash()

	#playing music
	def play_music():
		global num_music, music_list, povtor_on
		try:

			name_dict = os.getenv('USERPROFILE')

			path_music = name_dict + '\\OnlineMusic\\'
			url = music_list[num_music].get('url')

			#saving music
			path_save_url = path_music + music_list[num_music].get('name')
			if os.path.isfile(path_save_url + '.mp3') == False:
				with open(path_save_url + '.mp3', 'wb') as file:
					download = requests.get(url)
					file.write(download.content)

		#urllib.request.urlretrieve(url, path_save_url + '.mp3')

			if len(music_list) > 0:
				music_load = path_save_url + '.mp3'
				try:
					pygame.mixer.music.load(music_load)
					pygame.mixer.music.play()
				except Exception:
					num_music += 1
				#deleting downloaded tracks
				OnlineMusic.clear_cash()
		except Exception:
			num_music += 1


	#garbage cleaning
	def clear_cash():

		name_dict = os.getenv('USERPROFILE')
		path_music = name_dict + '\\OnlineMusic\\'

		try:
			shutil.rmtree(path_music)
		except Exception:
			pass

		if os.path.isfile(path_music) == True:
			for file in glob.glob(path_music):
				try:
					shutil.rmtree(file)
					os.remove(file)
				except Exception:
					continue


	Theme = None
	def Themes(Themeo):
		global Theme, back2, next_button, last_button, pause_button, play_button, search, peremeshat1, peremeshat2, povtor1, povtor2, back_ground

		Theme = Themeo

		if Theme == 'gradient':
			back2 = back2_gradient
			next_button = next_button_gradient
			last_button = last_button_gradient
			pause_button = pause_button_gradient
			play_button = play_button_gradient
			search = search_gradient
			peremeshat1 = peremeshat1_gradient
			peremeshat2 = peremeshat2_gradient
			povtor1 = povtor1_gradient
			povtor2 = povtor2_gradient
			back_ground = back_ground_gradient
		if Theme == 'white':
			back2 = back2_white
			next_button = next_button_white
			last_button = last_button_white
			pause_button = pause_button_white
			play_button = play_button_white
			search = search_white
			peremeshat1 = peremeshat1_white
			peremeshat2 = peremeshat2_white
			povtor1 = povtor1_white
			povtor2 = povtor2_white
			back_ground = back_ground_white
		if Theme == 'dark':
			back2 = back2_dark
			next_button = next_button_dark
			last_button = last_button_dark
			pause_button = pause_button_dark
			play_button = play_button_dark
			search = search_dark
			peremeshat1 = peremeshat1_dark
			peremeshat2 = peremeshat2_dark
			povtor1 = povtor1_dark
			povtor2 = povtor2_dark
			back_ground = back_ground_dark


music_list2 = []

def parse_music(name=''):
	global music_list2, music_list, num_music

	OnlineMusic.clear_cash()

	num_music = 0

	name_dict = os.getenv('USERPROFILE')
	music_list_test = music_list

	if os.path.exists(name_dict + '\\OnlineMusic\\') == False:
		os.mkdir(name_dict + '\\OnlineMusic')


	try:

		siteUrl = 'https://muzebra.me/'

		if name == '':
			URL = 'https://muzebra.me/'
			index = 5

		else:
			URL = 'https://muzebra.me/song/' + str(name)
			index = 4

		respons = requests.get(URL)
		soup = BS(respons.content, 'html.parser')
		items = soup.findAll("div", class_="trackItem")

		music_list = []

		for el in items:
			url = (str(el).split("=")[2] + str(el).split("=")[3].replace(">", "").replace("<button class", "")).replace('"', "").replace("<button classtrackItem__playStop btn-play title", "").replace(">", "")

			names = str(el).split("=")[index].replace(">", "").replace("<svg viewbox", "").split(" ")[2:-1]
			name = " ".join(names)

			if name != "":
				music_list.append({
					"name" : name,
					"url" : siteUrl + url.replace("\n", "")
					})

		music_list2 = music_list.copy()
		#if the search was unsuccessful, then restore the previous search
		if music_list == None or music_list == []:
			music_list = music_list_test
			music_list_test= []

	except Exception:
		print("Internet")


#music search bar
def input_text(screen):
	global num_music, num, music_time_now_test, pause_on, peremotka_on, povtor_on, peremotka, Theme

	font = shrift 
	input_box = pygame.Rect(27, 10, 190, 32)
	color_inactive = pygame.Color(0,0,0)
	color_active = pygame.Color(255,255,255)
	color = color_inactive
	active = False 
	text = ''  
	done = False
	render_text_x = 29

	try:
		name_dict = os.getenv('USERPROFILE')
		path_music = name_dict + '\\OnlineMusic\\'
		path_save_url = path_music + music_list[num_music].get('name').rstrip('.jpg')
		music_load = path_save_url + '.mp3'
	except IndexError:
		pass

	keys = pygame.key.get_pressed()


	# Render the current text.
	font_type = pygame.font.Font(font, 25)
	txt_surface = font_type.render(text, True, (0,0,0))


	while not done:

		if Theme == 'gradient':
			txt_surface_color = (0,0,0)
		if Theme == 'dark':
			txt_surface_color = (255,255,255)
		if Theme == 'white':
			txt_surface_color = (0,0,0)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.mixer.music.stop()
				OnlineMusic.clear_cash()
				sys.exit()

			if event.type == pygame.MOUSEBUTTONDOWN:
	                # If the user clicked on the input_box rect.
				if input_box.collidepoint(event.pos):
	                    # Toggle the active variable.
					active = not active
				else:
					active = False
	               # Change the current color of the input box.
				color = color_active if active else color_inactive
			if event.type == pygame.KEYDOWN:
				if active:
					if event.key == pygame.K_BACKSPACE:
						text = text[:-1]

						if render_text_x >= 29:
							render_text_x = 29
						else:
							render_text_x += 10

					else:
						text += event.unicode

						if render_text_x + txt_surface.get_size()[0] > 180:
							render_text_x -= 25
				txt_surface = font_type.render(text, True, txt_surface_color)


		exite_to_play = Button.rect_button(screen, 2, 10, 22,32, (0,255,215), 1)
		btn_search = Button.rect_button(screen, 218, 10, 30,32, (0,255,215), 1)
		Art(screen)

	    # Blit the text.
		screen.blit(txt_surface, (render_text_x, input_box.y+5))
	    # Blit the input_box rect.
		pygame.draw.rect(screen, color, input_box, 2)
		if Theme == 'dark':
			pygame.draw.rect(screen, (41,42,41), (0,10,27,32))
		if Theme == 'white':
			pygame.draw.rect(screen, (255,255,255), (0,10,27,32))
		if Theme == 'gradient':
			pygame.draw.rect(screen, (0,255,215), (0,0,27,45))


	    #button back
		screen.blit(back2, (-2,12))
		if Button.click_button_rect(exite_to_play) == True:
			num_music = 0
			pygame.mixer.music.stop()
			OnlineMusic.clear_cash()
			break


		make_list_win(screen)
		Art_text(screen)

		#search button
		screen.blit(search, (217,10))
		if Button.click_button_rect(btn_search) == True or keys[pygame.K_RETURN]:
			name = text
			parse_music(name)
			num_music = 0
			pygame.mixer.music.stop()
			OnlineMusic.clear_cash()
			OnlineMusic.play_music()
			num = 0
			music_time_now_test = 0
			pause_on = False
			peremotka_on = False
			povtor_on = False
			peremotka = 1

		pygame.display.update()
		clock.tick(20)


#button mapping
btn_next = Button.round_button(screen,210,320,23,(0,0,0), 1)
btn_last = Button.round_button(screen,40,320, 23, (0,0,0), 1)
def Art(win):
	global btn_next, btn_last
	keys = pygame.key.get_pressed()

	win.blit(back_ground, (0,0))
	
	win.blit(last_button, (20,301))
	win.blit(next_button,(195,301))

	btn_last_on = Button.click_button_round(btn_last)
	if btn_last_on == True:
		button_last_on()
		

	btn_next_on = Button.click_button_round(btn_next)
	if btn_next_on == True:
		button_next_on()

	pause(win)
	random_list(win)
	povtor(win)
	polzunok_volume(win)
	music_line(win)

#rewind
def button_last_on():
	global num_music, music_time_now_test, text_x, peremotka, povtor_on
	peremotka = -1
	num_music += peremotka
	time.sleep(0.3)
	music_time_now_test = 0
	text_x = 10
	if povtor_on == True:
		peremotka = 0
	if num_music < 0:
		num_music = len(music_list)
		num_music += peremotka
	OnlineMusic.play_music()

#flash forward
def button_next_on():
	global num_music, music_time_now_test, text_x, peremotka, povtor_on
	peremotka = 1
	num_music += peremotka
	time.sleep(0.3)
	music_time_now_test = 0
	text_x = 10
	if povtor_on == True:
		peremotka = 0
	if num_music > len(music_list) - 1:
		num_music =0
	OnlineMusic.play_music()

#music tape
music_class_list = []
class Dict():

	def __init__(self, x, y, text, index_num):
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
	def music_button(self, win):
		global num_music, music_time_now_test, text_x, pause_on, music_list, peremotka_on, peremotka
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

			pygame.draw.rect(win, self.font_color, (self.x,self.y + height - 2,220,1))


			try:
				if Theme != self.Theme or self.font.get_size()[0] > 220 or self.font == None:
					self.Theme = Theme
					font_type = pygame.font.Font( shrift, 16 )
					self.font = font_type.render( text, True, self.font_color )

					if self.font.get_size()[0] > 220:
						self.text = self.text[:-1]
			except UnicodeError:
				self.text = str(self.index_num + 1) + ". "
				text = str(self.index_num + 1) + ". " + self.text
				self.font = font_type.render( text, True, self.font_color )

			try:
				win.blit(self.font, (self.x,self.y + 7))
			except UnboundLocalError:
				pass


		keys = pygame.key.get_pressed()
		pos = pygame.mouse.get_pos()
		mouse_x, mouse_y = pos[0], pos[1]
		MOUSE_CLICK = pygame.mouse.get_pressed()
	#	print(str(mouse_x) + " " + str(mouse_y))

		#movement of buttons using the mouse wheel and stelochek
		if mouse_x >= self.x and mouse_x <= self.x + 220 and mouse_y >= 50 and mouse_y <= 250:

			Dict.roll_mouse_wheel()

			if mouse_y >= self.y and mouse_y <= self.y + height and MOUSE_CLICK[0] == 1:
				num_music = self.index_num
				music_time_now_test = 0
				text_x = 10
				pause_on = False
				if peremotka_on == True:
					peremotka_on = False
					peremotka = 1
					music_list = music_list2.copy()
				OnlineMusic.play_music()

	#scrolling songs
	def roll_mouse_wheel():
		keys = pygame.key.get_pressed()
		height = 28

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


#creating items for the ribbon and displaying them
num = 0
def make_list_win(win):
	global num, music_class_list, music_list
	height = 28
	y = 50
	if len(music_list) > 0:
		if num < len(music_list):
			music_class_list = []
			try:
				for liste in music_list2:
					music_title = os.path.basename(music_list2[num].get("name"))
					music_title_print =  music_title.rstrip('.mp3')

					music_class_list.append(Dict(15,y, music_title_print, num))
					y += height
					num += 1
			except IndexError:
				num = 0
				music_list = []

	
	for liste in music_class_list:
		if liste.y >= 50 and liste.y + height <= 265: 
			liste.music_button(win)


#pause
pause_on = False
btn_pause = Button.round_button(screen,127,321,25,(0,0,0), 1)
def pause(win):
	global pause_on,Theme, btn_pause

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


#progress bar for music
music_time_now_test = 0
def music_line(win):
	global num_music, music_time_now_test, text_x, peremotka, povtor_on, music_list

	if len(music_list) > 0:

		name_dict = os.getenv('USERPROFILE')
		path_music = name_dict + '\\OnlineMusic\\'

		try:
			path_save_url = path_music + music_list[num_music].get('name')
			music_load = path_save_url + '.mp3'
		except IndexError:
			music_list = []


		#tracking current song length and full song length
		try:
			music_time = MP3(music_load).info.length
			music_time_now = music_time_now_test + round(pygame.mixer.music.get_pos() / 1000, 2)
		except Exception:
			num_music += peremotka
			OnlineMusic.play_music()


		pos = pygame.mouse.get_pos()
		mouse_x, mouse_y = pos[0], pos[1]
		MOUSE_CLICK = pygame.mouse.get_pressed()

		#percentage to fill the progress bar
		try:
			proc = music_time / 100
			proc = round(music_time_now / proc )
			proc = proc * 2
			music_line_round_x = 20 + proc
		except UnboundLocalError:
			music_time = 0
			music_time_now = 0
			music_line_round_x = 20



		pygame.draw.rect(win,(104,104,104), (20, 270,200,5))
		pygame.draw.circle(win,(255,0,0),(music_line_round_x, 272), 8)


		#tracking the end of a track
		if round(music_time_now) >= math.floor(music_time):
			music_time_now_test = 0
			if povtor_on == True:
				peremotka = 0
			num_music += peremotka
			text_x = 10
			OnlineMusic.play_music()


		if music_line_round_x > 20:
			pygame.draw.rect(win, (255,0,0), (20, 270,music_line_round_x - 20 , 5))

		#setting a track at a specific second
		if mouse_x >= 20 and mouse_x <= 220 and mouse_y >= 265 and mouse_y <= 275:
			procen = (mouse_x - 20)
			procen = procen * music_time / 100 / 2

			secondes3 = timedelta(seconds=procen)
			timer3 = datetime(1,1,1) + secondes3
			print_text(win, str(timer3.minute) + ":" + str(timer3.second), mouse_x - 20, 255)

			if MOUSE_CLICK[0] == 1:
				music_time_now_test = procen
				music_time_now = music_time_now_test + round(pygame.mixer.music.get_pos() / 1000 / 60, 2)

				pygame.mixer.music.stop()
				pygame.mixer.music.play(-1,round(procen))
				time.sleep(0.2)

		#time stamp
		try:
			secondes1 = timedelta(seconds=music_time_now)
			timer1 = datetime(1,1,1) + secondes1

			secondes2 = timedelta(seconds=music_time)
			timer2 = datetime(1,1,1) + secondes2

			print_text(win, str(timer1.minute) + ":" + str(timer1.second), 20, 278, font_size = 15)
			print_text(win, str(timer2.minute) + ":" + str(timer2.second), 200, 278, font_size=15)
		except OverflowError:
			pass



#progress bar for sound
polzunok_volume_round_x= 115
def polzunok_volume(win):
	global polzunok_volume_round_x, Theme

	if Theme == 'gradient':
		polzunok_volume_color = (0,0,0)
	if Theme == 'white':
		polzunok_volume_color = (0,0,0)
	if Theme == 'dark':
		polzunok_volume_color = (255,255,255)

	pygame.draw.rect(win, (105,105,105), (70, 360,100, 5))
	pygame.draw.circle(win, polzunok_volume_color,  (polzunok_volume_round_x,362), 8)	
	
	if polzunok_volume_round_x >= 70:
		polzunok_volume_round_x = Sound.Sound.current_volume() + 70
		pygame.draw.rect(win, polzunok_volume_color, (70, 360,polzunok_volume_round_x - 70 , 5))


	pos = pygame.mouse.get_pos()
	mouse_x, mouse_y = pos[0], pos[1]
	MOUSE_CLICK = pygame.mouse.get_pressed()

	#setting the volume in certain units
	if mouse_x >= 70 and mouse_x <= 170 and mouse_y >= 358 and mouse_y <= 368:
		if MOUSE_CLICK[0] == 1:
			polzunok_volume_round_x = mouse_x
			print_text(win, str(mouse_x - 70), mouse_x - 10, 367)
			Sound.Sound.volume_set(mouse_x - 70 + 2)

	keys = pygame.key.get_pressed()


	if polzunok_volume_round_x < Sound.Sound.current_volume():
		polzunok_volume_round_x += 1

	if polzunok_volume_round_x > Sound.Sound.current_volume():
		polzunok_volume_round_x -= 1

	if polzunok_volume_round_x < 70:
		polzunok_volume_round_x = 70


#music title stamp
font_type = pygame.font.Font(shrift, 20)
text_x = 10
def Art_text(win):
	global num_music, text_x, font_type, Theme
	text_x_test = 10

	if len(music_list) > 0:

		try:
			#get song title
			text_window_print = os.path.basename(music_list[num_music].get("name"))
			text_window_print1 = text_window_print.rstrip('.mp3')

			if Theme == 'gradient' or Theme == 'white':
				font_color = (0,0,0)
			if Theme == 'dark':
				font_color = (255,255,255)

		
			text = font_type.render(text_window_print1, True, font_color)
			win.blit(text, (text_x,380))


			if text_x + text.get_size()[0] > 250 or text_x <= 0:
				text_x -= 1

			if text_x + text.get_size()[0] <=0:
				text_x = 251
			if text_x_test + text.get_size()[0] < 250:
				text_x = 10
		except Exception:
			num_music += 1
			OnlineMusic.play_music()
	else:
		print_text(win,"No Internet connection", 25, 200)


#stir function
peremotka_on = False
btn_random = Button.round_button(screen,201, 367, 15, (0,0,0), 1)
def random_list(win):
	global peremotka_on, num_music, music_list, text_x, music_time_now_test, peremotka, Theme, btn_random

	keys = pygame.key.get_pressed()

	if peremotka_on == False:
		peremotkaimg = peremeshat1
	if peremotka_on == True:
		peremotkaimg = peremeshat2
	win.blit(peremotkaimg, (187,352))

	btn_random_on = Button.click_button_round(btn_random)
	if btn_random_on == True and peremotka_on == False:
		peremotka_on = True
		random.shuffle(music_list)
		peremotka = 1
		OnlineMusic.play_music()
		text_x = 10
		music_time_now_test = 0
		time.sleep(0.3)

	elif btn_random_on == True and peremotka_on == True:
		peremotka_on = False
		music_list = music_list2.copy()
		peremotka = 1
		num_music =0 
		OnlineMusic.play_music()
		text_x = 10
		music_time_now_test = 0
		time.sleep(0.3)


#repeat function 
povtor_on = False
btn_povtor = Button.round_button(screen,37, 367, 15, (0,0,0), 1)
def povtor(win):
	global povtor_on, peremotka, Theme

	keys = pygame.key.get_pressed()

	if povtor_on == False:
		povtoimg = povtor1
	if povtor_on == True:
		povtoimg = povtor2
	win.blit(povtoimg, (22, 352))

	btn_povtor_on = Button.click_button_round(btn_povtor)
	if btn_povtor_on == True and povtor_on == False:
		povtor_on = True
		peremotka = 0
		time.sleep(0.3)

	elif btn_povtor_on == True and povtor_on == True:
		povtor_on = False
		peremotka = 1
		time.sleep(0.3)

	if peremotka == 1 or peremotka == -1:
		povtor_on = False
