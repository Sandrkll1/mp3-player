import pygame
from Button import Button
import sys
import os, time
import os.path, json
from threading import Thread

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

path_for_image = os.path.normpath(os.getcwd() + os.sep + os.pardir) + "\\images" #'D:\\python\\player\\images'#
back = None
back2 = None
music = pygame.transform.scale(pygame.image.load(path_for_image + "\\music.png"), (90, 90))
play_button = None
delet_button = None
back_ground = None
back_ground2 = None
back_ground3 = None
back_ground4 = None
#-----------gradient------------

shrift = "C:/Windows/Fonts/Calibri.ttf"
back_gradient = pygame.transform.scale(pygame.image.load(path_for_image + "/back.png"), (35, 30))
back2_gradient = pygame.transform.scale(pygame.image.load(path_for_image + "/back2.png"), (30, 25))
play_button_gradient = pygame.transform.scale(pygame.image.load(path_for_image + "/play.png"), (40, 25))
delet_button_gradient = pygame.transform.scale(pygame.image.load(path_for_image + "/delet.png"), (26, 26))
back_ground_gradient = vertical((250,400), (0, 255,255,255), (0,255,0,255))
back_ground2_gradient = vertical((250,400),(0,0,0,0), (255,0,0,0) )
back_ground3_gradient = back_ground2_gradient
back_ground4_gradient = back_ground2_gradient

#----------gradient-----------


#----------white--------------

back_white = back2_gradient
back2_white = back_white
play_button_white = pygame.transform.scale(pygame.image.load(path_for_image + "/playd.png"), (25, 25))
delet_button_white = delet_button_gradient
back_ground_white = pygame.image.load(path_for_image + "/back_groundwp.jpg")
back_ground2_white = pygame.image.load(path_for_image + "/back_groundwp2.jpg")
back_ground3_white = pygame.image.load(path_for_image + "/back_groundwp3.jpg")
back_ground4_white = pygame.image.load(path_for_image + "/back_groundwp4.jpg")

#----------white--------------


#----------dark---------------

back_dark = pygame.transform.scale(pygame.image.load(path_for_image + "/back2w.png"), (30,25))
back2_dark = back_dark
play_button_dark = pygame.transform.scale(pygame.image.load(path_for_image + "/playw.png"), (25,25)  )
delet_button_dark = pygame.transform.scale(pygame.image.load(path_for_image + "/deletw.png"), (26,26)  )
back_ground_dark = pygame.image.load(path_for_image + "/back_grounddp.jpg")
back_ground2_dark = pygame.image.load(path_for_image + "/back_grounddp2.jpg")
back_ground3_dark = pygame.image.load(path_for_image + "/back_grounddp3.jpg")
back_ground4_dark = pygame.image.load(path_for_image + "/back_grounddp4.jpg")

#----------dark---------------



#list for all instances of ready-made playlists
play_lists = []
#a list of buttons to fill the playlist
music_list = []
#start position y for playlist
play_lists_y = 50
play_playlist = False

#playlist class
button_add_playlist = Button.rect_button(screen, 25, 10, 20,20, (0,0,0))
btn_back = Button.round_button(screen, 222, 20, 23 , (0,0,0), 1)
class PlayList():
	def __init__(self, name, x, y, tracks, num, addd=False):
		self.name = name
		self.x = x
		self.y = y
		self.tracks = tracks
		self.num = num
		self.addd = addd

	#drawing all playlists from the play_lists list
	def draw_all(self, win):
		global play_lists_y, play_lists, play_playlist
		width, height = 100, 100

		play_list_button = Button.rect_button(win, self.x, self.y, 90, 90, (255,255,255))
		win.blit(music, (self.x, self.y))
		try:
			print_text(win,self.name, self.x + 1, self.y, font_color=(255,255,255))
		except Exception:
			pass

		#button for playing the playlist
		play_playlist_btn = Button.rect_button(win, self.x + 90 - 25, self.y + 90 - 25, 25, 25, (217,103,11), 1)
		win.blit(play_button, (self.x + 90 - 35, self.y + 90 - 25))		

		PlayList.roll_mouse_wheel()		

		#start playlist by pressing a button
		if Button.click_button_rect(play_playlist_btn) == True:
			self.addd = True
			play_playlist = True

		#monitors clicks on the playlist and edit it
		if Button.click_button_rect(play_list_button) == True:
			time.sleep(0.3)
			redact_playlist(win, self.tracks, self.name)

		#delete the playlist if the right mouse button was pressed
		if Button.click_button_rect(play_list_button) == 0:
			play_lists =[]

			remove_plalist(self.name)
			play_lists_y = 50
			open_playlists()
			time.sleep(0.3)

	#method to run the class
	def main(win, music_list1):
		global music_list, num, Theme, screen, button_add_playlist

		screen = win

		if music_list == []:
			music_list = music_list1

		win.blit(back_ground, (0,0))
		if Theme == 'gradient' or Theme == 'white':
			add_color = (0,0,0)
		if Theme == 'dark':
			add_color = (255,255,255)

		print_text(win,"+" ,26, 4, font_color=add_color, font_size=37)
		open_playlists()

		#returns the playlist to its initial position, i.e., it turns off the selected tracks
		for playing in play_lists:
			if playing.addd == True:
				playing.addd = False

		#run the function to create a playlist
		if Button.click_button_rect(button_add_playlist) == True:
			num = 0
			input_text(win)
			time.sleep(0.3)

		draw_list(win)


	#function to exit the class
	def exite(win):
		global play_lists_y, Theme, btn_back

		win.blit(back2, (205,7))
		if Button.click_button_round(btn_back) == True: 
			music_list = []
			return True

		
	#returns to the initial class all the tracks of the playlist that was clicked
	def retturn():
		for playing in play_lists:
			if playing.addd == True:
				playing.addd = False
				return playing.tracks

	#scrolling playlists
	def roll_mouse_wheel():	
		height = 100

		keys = pygame.key.get_pressed()
		pos = pygame.mouse.get_pos()
		mouse_x, mouse_y = pos[0], pos[1]
		MOUSE_CLICK = pygame.mouse.get_pressed()

		if mouse_x >= 0 and mouse_x <= 250 and mouse_y >= 50 and mouse_y <= 300:

			for i in pygame.event.get():

				if i.type == pygame.MOUSEBUTTONDOWN:

					if i.button == 4:
						for playing in play_lists:
							playing.y += height
							if playing.num == 0 and playing.y > 50:
								for playing in play_lists:
									playing.y -= height

					if i.button == 5:
						for playing in play_lists:
							playing.y -= height
							if playing.num + 1 == len(play_lists) and playing.y + height < 350:
								for playing in play_lists:
									playing.y += height

		if keys[pygame.K_UP]:
			for playing in play_lists:
				playing.y += height
				if playing.num  == 0 and playing.y > 50:
					for liste in music_class_list:
						liste.y -= height 
							

		if keys[pygame.K_DOWN]:
			for playing in play_lists:
				playing.y -= height
				if playing.num + 1 == len(play_lists) and playing.y + height < 350:
					for playing in play_lists:
						playing.y += height

		for playing in play_lists:			
			if playing.num == 0 and playing.y > 50:
				for playing in play_lists:
					playing.y -= height 


	Theme = None
	def Themes(Themep):
		global Theme, back, back2, music, play_button, delet_button, back_ground, back_ground2, back_ground3, back_ground4

		Theme = Themep

		if Theme == 'gradient':
			back = back_gradient
			back2 = back2_gradient
			play_button = play_button_gradient
			delet_button = delet_button_gradient
			back_ground = back_ground_gradient
			back_ground2 = back_ground2_gradient
			back_ground3 = back_ground3_gradient
			back_ground4 = back_ground4_gradient
		if Theme == "white":
			back = back_white
			back2 = back2_white
			play_button = play_button_white
			delet_button = delet_button_white
			back_ground = back_ground_white
			back_ground2 = back_ground2_white
			back_ground3 = back_ground3_white
			back_ground4 = back_ground4_white
		if Theme == "dark":
			back = back_dark
			back2 = back2_dark
			play_button = play_button_dark
			delet_button = delet_button_dark
			back_ground = back_ground_dark
			back_ground2 = back_ground2_dark
			back_ground3 = back_ground3_dark
			back_ground4 = back_ground4_dark

		
#method for rendering all playlists
def draw_list(win):
	height = 100
	for playing in play_lists:
		if playing.y >=50 and playing.y + height <= 350:
			playing.draw_all(win)




def print_text(win, massage, x, y, font_color=None, font_type=shrift, font_size=20):
	try:
		if font_color != None:
			font_color = font_color

		elif Theme == 'gradient':
			font_color = (255,255,255)
		elif Theme == 'dark':
			font_color = (255,255,255)
		elif Theme == 'white':
			font_color = (0,0,0)


		font_type = pygame.font.Font(font_type, font_size)
		text = font_type.render(massage, True, font_color)
		win.blit(text, (x,y))
	except Exception:
		pass

#makes an input and text field and only syncs created playlists
exite_to_play = Button.rect_button(screen, 3, 10, 25,25, (0,0,0), 1)
btn_OK = Button.rect_button(screen,210, 10, 25,25,(0,0,0), 1)
def input_text(screen):
	global Theme, music_class_list, exite_to_play, btn_OK

	font = shrift
	input_box = pygame.Rect(15, 40, 220, 32)
	color_inactive = pygame.Color('lightskyblue3')
	color_active = pygame.Color('dodgerblue2')
	color = color_inactive
	active = False 
	text = ''  
	done = False
	render_text_x = 17
	render_text_x_minus = 0


	while not done:

		if Theme == 'gradient' or Theme == 'dark':
			txt_surface_color = (255,255,255)
		if Theme == 'white':
			txt_surface_color = (0,0,0)

		font_type = pygame.font.Font(font, 25)
		txt_surface = font_type.render(text, True, txt_surface_color)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
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

						if render_text_x >= 27:
							render_text_x = 27
						else:
							render_text_x += 10
					else:
						text += event.unicode

						if render_text_x + txt_surface.get_size()[0] > 200:
							render_text_x -= 25

		screen.blit(back_ground2, (0,0))

		keys = pygame.key.get_pressed()

		screen.blit(txt_surface, (render_text_x, input_box.y+5))
		if Theme == 'gradient':
			screen.blit(pygame.transform.scale(back_ground2, (15,400)), (0,0))
		if Theme == 'white':
			pygame.draw.rect(screen, (255,255,255), (0,40,15,32))
		if Theme == 'dark':
			pygame.draw.rect(screen, (41,42,41), (0,40,15,32))
        # Blit the input_box rect.
		pygame.draw.rect(screen, color, input_box, 2)

		#buttom back
		screen.blit(back, (-2,9))
		if Button.click_button_rect(exite_to_play) == True:
			done = True
			time.sleep(0.3)


		make_list_win(screen,music_list)
		print_text(screen, '+', 210, 0, font_size=50)

		#checks if the create button was pressed and checks if the name was entered
		if Button.click_button_rect(btn_OK) == True or keys[pygame.K_RETURN] and len(text) > 0 :
			if len(text) > 8:
				while len(text) > 8:
					text = text[:-1]
			name = text
			text = ''
			tracks = []

			#adds all selected tracks to the playlist
			for liste in music_class_list:
				if liste.ok == True:
					tracks.append(liste.full_name)

			#call the function to create a playlist
			make_playlist(screen,name, tracks, len(play_lists))
			music_class_list = []

			#restores all tracks to their original position
			for liste in music_class_list:
				if liste.ok == True:
					liste.ok = False

			music_class_list = []

			time.sleep(0.3)
			done = True

		pygame.display.flip()
		clock.tick(20)
    


#finds and adds all created playlists from the database
def open_playlists():
	global play_lists_y, num
	height = 90

	name_dict = os.getenv('USERPROFILE')

	try:
		with open(name_dict + '\\playlist.json', 'r') as file:
			data = json.load(file)
	except:
		data =[]

	right = False
	playlist_x = 20

	if len(data) > len(play_lists):
		for name in data:
			tracks = []
			for track in name.get('tracks'):
				tracks.append(track)

			if right == False:
				playlist_x = 20
				right = True
				if len(play_lists) % 2 == 0:
					play_lists_y += height + 10

			elif right == True:
				playlist_x = 130
				right = False
				if len(play_lists) % 2 == 0:
					play_lists_y += height + 10

			play_lists.append(PlayList(name.get('name'), playlist_x, play_lists_y, tracks, len(play_lists)))
			music_class_list = []
			num = 0


#creates a playlist and adds it to the database
def make_playlist(win,name,tracks, num) :
	global play_lists, play_lists_y

	name_dict = os.getenv('USERPROFILE')

	try:
		data = json.load(open(name_dict + "\\playlist.json"))
	except:
		data = []

	data+= [{'name' : name, "tracks" : tracks}]

	try:
		with open(name_dict + '\\playlist.json', 'w') as file:
			json.dump(data, file, indent=2, ensure_ascii=True)
	except UnicodeEncodeError:
		pass

	play_lists = []
	play_lists_y = 50
	open_playlists()


#deletes the playlist if the right mouse button was pressed
def remove_plalist(name):
	data = []
	name_dict = os.getenv('USERPROFILE')

	with open(name_dict + '\\playlist.json', 'r') as file:
	    data = json.load(file)

	for i in range(len(data)):
	    if data[i]["name"] == name:
	        data.pop(i)
	        break

	with open(name_dict + '\\playlist.json', 'w') as filee:
	    json.dump(data, filee, indent=2, ensure_ascii=False)
		

#the same class as in the main program only slightly changed
music_class_list = []
class Dict():

	def __init__(self, win, x, y, text, index_num, full_name, ok):
		global Theme
		self.x = x
		self.y = y	
		self.text = text
		self.index_num = index_num
		self.full_name = full_name
		self.ok = ok
		self.button = Button.button_text(win, '', self.x, self.y + 7, 220, 28, font_color=(255,255,255), font_size=16)
		font_type = pygame.font.Font( shrift, 16 )
		self.font = font_type.render( self.text, True, (0,0,0) )
		self.Theme = 'white'

	def music_button(self, win):
		global num_music, text_x, peremotka_on, Theme
		height = 28

		keys = pygame.key.get_pressed()

		text = str(self.index_num + 1) + ". " + self.text

		if Theme == 'gradient':
			self.font_color = (255,255,255)
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

			win.blit( self.font, (self.x,self.y + 7) )
		except UnicodeError:
			self.text = str(self.index_num + 1) + ". "
			text = str(self.index_num + 1) + ". " + self.text
			self.font = font_type.render( text, True, self.font_color )

		keys = pygame.key.get_pressed()
		pos = pygame.mouse.get_pos()
		mouse_x, mouse_y = pos[0], pos[1]
		MOUSE_CLICK = pygame.mouse.get_pressed()
	#	print(str(mouse_x) + " " + str(mouse_y))

		if mouse_x >= self.x and mouse_x <= self.x + 350 and mouse_y >= 78 and mouse_y <= 378:

			Dict.roll_mouse_wheel()

			#indicates the selected tracks
			for liste in music_class_list:
				if Button.button_text_click(liste.button) == True:
					if liste.ok == True:
						liste.ok = False
						time.sleep(0.4)
					elif liste.ok == False:
						liste.ok = True
						time.sleep(0.4)


		for liste in music_class_list:
			if liste.ok == True:
				if liste.y + height >= 78 and liste.y + height <= 378:
					pygame.draw.circle(win, (0,255,0), (liste.x - 8, liste.y + 10), 7)

	#scrolling songs
	def roll_mouse_wheel():
		keys = pygame.key.get_pressed()
		height = 28

		for i in pygame.event.get():

			if i.type == pygame.MOUSEBUTTONDOWN:

				if i.button == 4:
					for liste in music_class_list:
						liste.y += height
						if liste.index_num - 1 < 0 and liste.y > 78:
							for liste in music_class_list:
								liste.y -= height

				if i.button == 5:
					for liste in music_class_list:
						liste.y -= height
						if liste.index_num + 2 > len(music_class_list) and liste.y + height < 378:
							for liste in music_class_list:
								liste.y += height

		if keys[pygame.K_UP]:
			for liste in music_class_list:
				liste.y += height
				if liste.index_num - 1 < 0 and liste.y > 78:
					for liste in music_class_list:
						liste.y -= height
							

		if keys[pygame.K_DOWN]:
			for liste in music_class_list:
				liste.y -= height
				if liste.index_num + 2 > len(music_class_list) and liste.y + height < 378:
					for liste in music_class_list:
						liste.y += height



#the same method as in the main program, only slightly modified
num = 0
def make_list_win(win,music_list):
	global num
	height = 28
	y = 78
	if num < len(music_list):
		for liste in music_list:
			full_name = music_list[num]
			music_title = os.path.basename(music_list[num])
			music_title_print = music_title.rstrip('.mp3')

			while len(music_title_print) > 26:
				music_title_print = music_title_print[:-1]

			music_class_list.append(Dict(win,15,y, music_title_print, num, full_name, False))
			y += height
			num += 1

	
	for liste in music_class_list:
		if liste.y >= 78 and liste.y + height <= 378: 
			liste.music_button(win)


#playlist editing
redact = False
def redact_playlist(win, tracks, name):
	global num, redact, music_class_list, play_playlist, Theme
	num = 0

	keys = pygame.key.get_pressed()
	redact = True
	height = 28
	music_class_list = []

	for liste in music_class_list:
		liste.ok = False

	if play_playlist == True:
		redact = False
		play_playlist = False



	font = shrift
	input_box = pygame.Rect(15, 40, 220, 32)
	color_inactive = pygame.Color('lightskyblue3')
	color_active = pygame.Color('dodgerblue2')
	color = color_inactive
	active = False 
	text = name 
	render_text_x = 17

	#buttons
	exite_to_play = Button.rect_button(win, 220, 10, 25,25, (10,10,10),1)
	btn_remove_track = Button.rect_button(win, 35,363, 25,25, (230,0,0), 1)
	btn_add = Button.rect_button(win, 120, 363, 25, 25, (230,0,0), 1)
	btn_play = Button.rect_button(win, 200, 363, 25, 25, (230,0,0), 1)
	btn_ok = Button.rect_button(win, 30, 365, 25, 25, (230,0,0), 1)
	exite_to_add = Button.rect_button(win, 220, 10, 25,25, (10,10,10),1)

	while redact:

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

		keys = pygame.key.get_pressed()
		pos = pygame.mouse.get_pos()
		mouse_x, mouse_y = pos[0], pos[1]
		MOUSE_CLICK = pygame.mouse.get_pressed()

		win.blit(back_ground3, (0,0))


		make_list_win(win, tracks)
		print_text(win, name, 20, 20, font_size=30)

		#button to exit the loop
		win.blit(back, (217,9))
		if Button.click_button_rect(exite_to_play) == True:
			music_class_list = []
			num = 0
			for liste in music_class_list:
				liste.ok = False
			redact = False

		for liste in music_class_list:
			if mouse_y >= liste.y and mouse_y <= liste.y + height:
				if MOUSE_CLICK[0] == 1:
					liste.ok = True
					
		#button to remove selected tracks from the playlist
		win.blit(delet_button, (33,363))
		if Button.click_button_rect(btn_remove_track) == True:

			for liste in music_class_list:
				if liste.ok == True:

					for track in tracks:
						if os.path.basename(track).rstrip('.mp3') == liste.text:

							tracks.pop(tracks.index(track))
							music_class_list = []
							num = 0
							make_list_win(win, tracks)
							remove_plalist(name)
							make_playlist(win, name, tracks, len(play_lists))

			for liste in music_class_list:
				liste.ok = False
			redact = False
			time.sleep(0.3)

		#button to start the playlist
		win.blit(play_button,(200,363))
		if Button.click_button_rect(btn_play) == True:
			for playing in play_lists:
				if playing.name == name:
					playing.addd = True
				music_class_list = []
				num = 0
				redact = False

		#button to add tracks to the playlist
		print_text(win, "+", 122,356,font_size=45)
		if Button.click_button_rect(btn_add) == True:
			add = True
			num = 0
			music_class_list = []
			redact = False
			while add:

				if Theme == 'gradient' or Theme == 'dark':
					txt_surface_color = (255,255,255)
				if Theme == 'white':
					txt_surface_color = (0,0,0)

				font_type = pygame.font.Font(font, 25)
				txt_surface = font_type.render(text, True, txt_surface_color)

				win.blit(back_ground4, (0,0))
				
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
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

								if render_text_x >= 27:
									render_text_x = 27
								else:
									render_text_x += 10
							else:
								text += event.unicode

								if render_text_x + txt_surface.get_size()[0] > 200:
									render_text_x -= 25


				win.blit(txt_surface, (render_text_x, input_box.y+5))

				if Theme == 'gradient':
					win.blit(pygame.transform.scale(back_ground4, (15,400)), (0,0))
				if Theme == 'white':
					pygame.draw.rect(win, (255,255,255), (0,40,15,32))
				if Theme == 'dark':
					pygame.draw.rect(win, (41,42,41), (0,40,15,32))

				pygame.draw.rect(win, color, input_box, 2)

				make_list_win(win, music_list)

				#button to exit the loop
				win.blit(back, (218,9))
				if Button.click_button_rect(exite_to_add) == True:
					time.sleep(0.2)
					for liste in music_class_list:
						liste.ok = False
					add = False
					num = 0
					music_class_list = []
					redact = True

				#adds all selected tracks
				print_text(win, "OK", 30,370)
				if Button.click_button_rect(btn_ok) == True:
					for liste in music_class_list:
						if liste.ok == True:
							tracks.append(liste.full_name)
							#print(liste.full_name)
							liste.ok = False

					tracks = list(set(tracks))
					remove_plalist(name)
					#print(tracks)
					make_playlist(win, text, tracks, len(play_lists))

					music_class_list = []
					num = 0
					add = False
					name = text
					for liste in music_class_list:
						liste.ok = False
					time.sleep(0.3)
				redact = True

				pygame.display.update()
				clock.tick(20)


		pygame.display.update()
		clock.tick(20)
