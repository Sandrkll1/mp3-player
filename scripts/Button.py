import pygame

shrift = "C:/Windows/Fonts/Calibri.ttf"

class Button():

	#method for creating a rectangular button
	def rect_button(win, x, y, width, height, color=(0,0,0), alpha=0):
		pygame.draw.rect(win, color, (x,y,width,height), alpha)
		return x, y, width, height

	#method for creating a round button
	def round_button(win, x,y,radius, color=(0,0,0), alpha=0):
		pygame.draw.circle(win, color,  (x,y), radius, alpha)
		return x, y, radius

	#checks if a rectangular button was pressed, if yes then returns True or 0
	def click_button_rect(button):
		x = button[0]
		y = button[1]
		width = button[2]
		height = button[3]

		pos = pygame.mouse.get_pos()
		mouse_x, mouse_y = pos[0], pos[1]
		MOUSE_CLICK = pygame.mouse.get_pressed()
		
		if x <= mouse_x and x + width >= mouse_x and y <= mouse_y and y + height >= mouse_y:
			if MOUSE_CLICK[0] == 1:
				return True
			if MOUSE_CLICK[2] == 1:
				return 0
			if MOUSE_CLICK[1] == 1:
				return 1

	#checks if the round button was pressed, if yes then returns True or 0
	def click_button_round(button):
		x = button[0]
		y = button[1]
		radius = button[2]

		pos = pygame.mouse.get_pos()
		mouse_x, mouse_y = pos[0], pos[1]
		MOUSE_CLICK = pygame.mouse.get_pressed()

		if mouse_x <= x + radius and mouse_x >= x - radius and mouse_y <= y + radius and mouse_y >= y - radius:
			if MOUSE_CLICK[0] == 1:
				return True 
			if MOUSE_CLICK[2] == 1:
				return 0
			if MOUSE_CLICK[1] == 1:
				return 1

	def button_text(win, text, x, y, width, height, font_color=(0,0,0), font_type=shrift, font_size=20):
		print_text(win, text, x, y, font_color, font_type, font_size)
		return x, y, width, height, text


	def button_text_click(button):
		x = button[0]
		y = button[1]
		width = button[2]
		height = button[3]

		pos = pygame.mouse.get_pos()
		mouse_x, mouse_y = pos[0], pos[1]
		MOUSE_CLICK = pygame.mouse.get_pressed()

		if mouse_y >= y and mouse_y <= y + height:
			if MOUSE_CLICK[0] == 1:
				return True
			if MOUSE_CLICK[2] == 1:
				return 0
			if MOUSE_CLICK[1] == 1:
				return 1



def print_text(win, massage, x, y, font_color=(0,0,0), font_type=shrift, font_size=20):
	try:
		font_type = pygame.font.Font(font_type, font_size)
		text = font_type.render(massage, True, font_color)
		win.blit(text, (x,y))
	except UnicodeError:
		pass
