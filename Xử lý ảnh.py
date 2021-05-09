import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import pygame
from tkinter import filedialog as fd
import tkinter as tk
import numpy as np
from PIL import Image

pygame.init()
screen = pygame.display.set_mode((1200, 700))
clock = pygame.time.Clock()
running = True
pygame.display.set_caption("Images processing")

root = tk.Tk()
a = ''
K = 1

# Colors
BACKGROUND = (214, 214, 214)
BLACK = (0,0,0)
BACKGROUND_PANEL = (249, 255, 230)
WHITE = (255,255,255)

# Fonts
font = pygame.font.SysFont('arial', 20)
font_big = pygame.font.SysFont('arial', 30)
font_huge = pygame.font.SysFont('arial', 40)
text_browse = font.render("Choose an image", True, WHITE)
text_before = font_big.render("BEFORE", True, BLACK)
text_after = font_big.render("AFTER", True, BLACK)
text_plus = font_huge.render('+', True, WHITE)
text_minus = font_huge.render('-', True, WHITE)

arrow = pygame.image.load(r"C:\Users\160 ltv\Downloads\edited-red-arrow-clip-art-317336.png")
shape_arr = arrow.get_size()
arrow = pygame.transform.scale(arrow, (int(shape_arr[0]/5), int(shape_arr[1]/5)))

img_final = []
while running == True:
	clock.tick(60)
	screen.fill(BACKGROUND)
	mouse_x, mouse_y = pygame.mouse.get_pos()
	
	pygame.draw.rect(screen, BLACK, (50, 30, 150, 50))
	screen.blit(text_browse, (60, 40))
	
	# Before
	pygame.draw.rect(screen, BLACK, (70, 130, 400, 470))
	pygame.draw.rect(screen, BACKGROUND, (75, 135, 390, 460))
	screen.blit(text_before, (210, 620))
	
	# After
	pygame.draw.rect(screen, BLACK, (730, 130, 400, 470))
	pygame.draw.rect(screen, BACKGROUND, (735, 135, 390, 460))
	screen.blit(text_after, (900, 620))
	
	# Arrow
	screen.blit(arrow, (540, 300))
	
	# K button + 
	pygame.draw.rect(screen, BLACK, (250,30,50,50)) 
	screen.blit(text_plus, (266,31)) 

	# K button -
	pygame.draw.rect(screen, BLACK, (395,30,50,50))
	screen.blit(text_minus, (415,31))

	# K value
	text_k = font_big.render("K = " + str(K), True, BLACK)
	screen.blit(text_k, (320,37))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		  
		if event.type == pygame.MOUSEBUTTONDOWN:
			if 50 < mouse_x < 200 and 30 < mouse_y < 80:
				def select_file():
					filetypes = (
						('jpeg files', '*.jpg'),
						('All files', '*.*')
					)
					global filename
					filename = fd.askopenfilename(
						title='Open a file',
						initialdir='/',
						filetypes=filetypes)
					root.mainloop()
				select_file()
				a = filename
			
			# Change K button +
			if 250 < mouse_x < 300 and 30 < mouse_y < 80:
					K = K+1
			
			# Change K button -
			if 395 < mouse_x < 445 and 30 < mouse_y < 80:
				if K > 1:
					K -= 1

			# Run button 
			if 545 < mouse_x < 655 and 300 < mouse_y < 385:
				img_read = plt.imread(r"{}".format(a))
				width = img_read.shape[0]
				height = img_read.shape[1]
				dimension = img_read.shape[2]
				img_read = img_read.reshape(width * height, dimension)
				kmeans = KMeans(n_clusters = K).fit(img_read)
				clusters = kmeans.cluster_centers_
				labels = kmeans.predict(img_read)
				img_after = np.zeros_like(img_read)

				for i in range(len(img_after)):
					img_after[i] = clusters[labels[i]]

				img_final = img_after.reshape(width, height, dimension)
	
	if a != '':
		img = pygame.image.load(r"{}".format(a))
		shape_pic = img.get_size()
		img_blit = pygame.transform.scale(img, (390, int(shape_pic[1]/shape_pic[0]*390)))
		screen.blit(img_blit, (75, 135))
	try:
		img_final = Image.fromarray(img_final, 'RGB')
		img_final.save('fixed.jpg')
  
	except:
		pass
	
	if img_final != []:
		img_final_show = pygame.image.load("fixed.jpg")
		shape_pic_final = img_final_show.get_size()
		img_final_show_blit = pygame.transform.scale(img_final_show, (390, int(shape_pic_final[1]/shape_pic_final[0]*390)))
		screen.blit(img_final_show_blit, (735, 135))


	pygame.display.flip()

pygame.quit()

