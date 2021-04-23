import pygame, sys, random

pygame.init()

screen = pygame.display.set_mode((512,512))
pygame.display.set_caption("FishtheDeep")

background = pygame.image.load('Data/menubackground.png')

font = pygame.font.SysFont("times new roman", 28)
box_color = pygame.Color('dodgerblue1')

def draw_text(text, font, color, surface, x,y):
	textbox = font.render(text, 1, color)
	textrect = textbox.get_rect(center = (x,y))
	surface.blit(textbox, textrect)

click = False
clock = pygame.time.Clock()

pygame.mixer.music.load('Data/MidiSe.mid')
pygame.mixer.music.play(-1)
swim_sound = pygame.mixer.Sound('Data/1plop.mp3')

logo = pygame.image.load('Data/logo.png')
logo_rect_topleft = logo.get_rect(topleft = (10,10))
logo_rect_topright = logo.get_rect(topright = ( 502, 10))



def main_menu():
	while True:
		screen.blit(background, (0,0))
		draw_text('MENU', font, (0,0,255), screen, 256, 110)
		mouse_x, mouse_y = pygame.mouse.get_pos()

		button_1 = pygame.Rect(156, 136, 200, 50)
		button_2 = pygame.Rect(156, 211, 200, 50)
		button_3 = pygame.Rect(156, 286, 200, 50)
		button_4 = pygame.Rect(156, 361, 200, 50)

		pygame.draw.rect(screen, box_color, button_1)
		draw_text('CHƠI GAME', font, (0,255,0), screen, 256,161)
		pygame.draw.rect(screen, box_color, button_2)
		draw_text('HƯỚNG DẪN', font, (0,255,0), screen, 256, 236)
		pygame.draw.rect(screen, box_color, button_3)
		draw_text('THÔNG TIN', font, (0,255,0), screen, 256, 311)
		pygame.draw.rect(screen, box_color, button_4)
		draw_text('THOÁT GAME', font ,(0,255,0), screen, 256, 386)
		click = False

		screen.blit(logo, logo_rect_topleft)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True

		if button_1.collidepoint((mouse_x,mouse_y)):
			if click:
				swim_sound.play()
				game()
		if button_2.collidepoint((mouse_x,mouse_y)):
			if click:
				swim_sound.play()
				guide()
		if button_3.collidepoint((mouse_x,mouse_y)):
			if click:
				swim_sound.play()
				about()
		if button_4.collidepoint((mouse_x, mouse_y)):
			if click:
				pygame.quit()
				sys.exit()

		pygame.display.update()
		clock.tick(120)
def game():
	background = pygame.image.load('Data/colorbackground.png') 
	gameover = pygame.image.load('Data/PRESSSPACE.png')
	gameover_rect = gameover.get_rect(center = (256,256))

	#wave
	wave = pygame.image.load('Data/wave.png').convert_alpha()
	flip_wave = pygame.transform.flip(wave, False, True)
	wave_x = 0
	wave_x_2 = 0

	def draw_wave():
		screen.blit(wave,(wave_x,410))
		screen.blit(wave,(wave_x + 512,410))
		screen.blit(wave,(wave_x_2,420))
		screen.blit(wave,(wave_x_2 + 512, 420))

		screen.blit(flip_wave,(wave_x, 15))
		screen.blit(flip_wave,(wave_x + 512, 15)) 
		screen.blit(flip_wave,(wave_x_2, 0))
		screen.blit(flip_wave,(wave_x_2 + 512, 0))

	#Fish
	fish = pygame.image.load('Data/fish.png').convert_alpha()
	fish_rect = fish.get_rect(center = (50, 266))

	gravity = 0.25
	fish_movement = 0

	def  rotate_fish(pfish):
		new_fish = pygame.transform.rotozoom(fish,-fish_movement*2, 1)
		return new_fish

	#heart
	heart = pygame.image.load('Data/heart.png')
	heart_rect = heart.get_rect(center = (540, 256))
	heart_list = []
	heart_height = [150, 180, 210, 240, 270, 300, 400]
	timer = pygame.USEREVENT
	pygame.time.set_timer(timer, 900)

	def create_heart():
		random_height = random.choice(heart_height)
		new_heart = heart.get_rect(center = (540, random_height))
		return new_heart

	def heart_move(heartlist):
		for pheart in heartlist:
			pheart.centerx -= 2
		return heartlist

	def draw_heart(heartlist):
		for pheart in heartlist:
			screen.blit(heart, pheart)

	gameloop = True

	def check_collision(heartlist):
		for pheart in heartlist:
			if fish_rect.colliderect(pheart) == True:
				return False

		if fish_rect.top <= 30 or fish_rect.bottom >= 482:
			return False
		return True

	blue = (0,0,255)
	white = (255,255,255)
	black = (0,0,0)
	Score_0_color = pygame.Color('lightskyblue3')
	Game_name_color = pygame.Color('dodgerblue1')

	game_name = font.render('FishtheDeep', True, Game_name_color, None)
	game_name_rect = game_name.get_rect()
	game_name_rect.bottomleft = ( 10, 502)

	score = 0
	best_score = 0
	game_score = font.render("Điểm: {}".format(score), True, black, None)
	game_score_rect = game_score.get_rect()
	game_score_rect.topleft = (10,10)

	def update_score(score, best_score):
		if score >= best_score:
			return score
		else:
			return best_score


	while True:
		mouse_x, mouse_y = pygame.mouse.get_pos()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					fish_movement = 0
					fish_movement -= 6
					swim_sound = pygame.mixer.Sound('Data/1plop.mp3')
					swim_sound.play()
				if event.key == pygame.K_SPACE and gameloop == False:
					gameloop = True
					heart_list.clear()
					score = 0
					game_score = font.render("Điểm: {}".format(score), True, Score_0_color, None)
					fish_rect.center = (50, 266)
					key_music = -1
			if event.type == timer:
				heart_list.append(create_heart())
			if event.type == pygame.MOUSEBUTTONDOWN:
				click = True

		screen.blit(background, (0,0))

		#wave
		wave_x -= 1
		wave_x_2 -= 2
		draw_wave()
		if wave_x == -512:
			wave_x = 0
		if wave_x_2 == - 512:
			wave_x_2 = 0

		gameloop = check_collision(heart_list)
		if gameloop:		
			#fish
			fish_movement += gravity
			rotated_fish = rotate_fish(fish)
			fish_rect.centery += fish_movement
			screen.blit(rotated_fish, fish_rect)

			#heart
			heart_list = heart_move(heart_list)
			draw_heart(heart_list)
			for pheart in heart_list:
				if pheart.left  == 30:
					score += 1
					game_score = font.render("Điểm: {}".format(score), True, black, None)

			screen.blit(game_score, game_score_rect)
		else:
			best_score = update_score(score, best_score)
			screen.blit(gameover, gameover_rect)
			draw_text('Điểm cao nhất: ' + str(best_score), font, (255,255,0), screen, 256, 30)
			draw_text('Điểm của bạn: ' + str(score), font, (255,255,0), screen, 256, 60)
			screen.blit(logo, logo_rect_topright)
			button_1 = pygame.Rect(5,10, 105, 40)
			pygame.draw.rect(screen, box_color, button_1)
			draw_text('Quay lại', font, (0,255,0), screen, 55,30)
			if button_1.collidepoint((mouse_x, mouse_y)):
				if click:
					swim_sound = pygame.mixer.Sound('Data/1plop.mp3')

					swim_sound.play()
					main_menu()
		click = False

		screen.blit(game_name, game_name_rect)
		pygame.display.update()
		clock.tick(120)
def guide():
	while True:
		screen.blit(background, (0,0))
		screen.blit(logo, logo_rect_topright)

		mouse_x, mouse_y = pygame.mouse.get_pos()
		button_1 = pygame.Rect(5,10, 105, 40)
		if button_1.collidepoint((mouse_x,mouse_y)):
			if click:
				swim_sound.play()
				main_menu()
		click = False

		draw_text('LUẬT CHƠI', font, box_color, screen, 256,120)
		draw_text('', font, box_color, screen, 256, 150)
		draw_text('Sau khi vào game nhấn SPACE', font, box_color, screen, 256,180)
		draw_text('để né các thính là các trái tim', font, box_color, screen, 256,210)
		draw_text('để giành nhiều điểm nhất', font, box_color, screen, 256,240)
		draw_text('Nên nhớ: Cá không thể bơi quá xa vùng biển', font, box_color, screen, 256,270)
		draw_text('', font, box_color, screen, 256, 300)
		draw_text('CHÚC CÁC BẠN MAY MẮN', font, box_color, screen, 256,330)
		draw_text('VÀ GIÀNH THẬT NHIỀU ĐIỂM', font, box_color, screen, 256,360)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				click = True
		pygame.draw.rect(screen, box_color, button_1)
		draw_text('Quay lại', font, (0,255,0), screen, 55,30)

		pygame.display.update()
		clock.tick(120)
def about():
	while True:
		screen.blit(background, (0,0))
		screen.blit(logo, logo_rect_topright)

		mouse_x, mouse_y = pygame.mouse.get_pos()
		button_1 = pygame.Rect(5,10, 105, 40)
		if button_1.collidepoint((mouse_x,mouse_y)):
			if click:
				swim_sound.play()
				main_menu()
		click = False
		draw_text('TÁC GIẢ', font,box_color, screen, 256,120)
		draw_text('Cao Tấn Đức', font, box_color, screen, 256,150)
		draw_text('MSSV: 20120270', font, box_color, screen, 256,180)
		draw_text('', font, box_color, screen, 256, 210)		
		draw_text('NHÓM', font, box_color, screen, 256,240)
		draw_text('Lục Đại Điêu', font, box_color, screen, 256,270)
		draw_text('', font, box_color, screen, 256, 300)
		draw_text('ÂM THANH', font, box_color, screen, 256,330)
		draw_text('Phạm Quốc Vương', font, box_color, screen, 256,360)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				click = True
		pygame.draw.rect(screen, box_color, button_1)
		draw_text('Quay lại', font, (0,255,0), screen, 55,30)

		pygame.display.update()
		clock.tick(120)

main_menu()