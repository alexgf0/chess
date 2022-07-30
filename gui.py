import pygame as pg
from pygame.locals import *

WHITE = (255, 255, 255)
GREY = (90, 90, 90)



class Chess_gui:
    def __init__(self, board):
        pg.init()
        self.screen = pg.display.set_mode((1280, 920))
        self.font = pg.font.SysFont(None, 50)
        pg.display.set_caption("Chess")
        self.clock = pg.time.Clock()
        self.white_paths = ["./pieces_imgs/white_king.png", "./pieces_imgs/white_queen.png", "./pieces_imgs/white_rook.png", "./pieces_imgs/white_bishop.png",
                    "./pieces_imgs/white_knight.png", "./pieces_imgs/white_pawn.png"]
        self.black_paths = ["./pieces_imgs/black_king.png", "./pieces_imgs/black_queen.png", "./pieces_imgs/black_rook.png", "./pieces_imgs/black_bishop.png",
                    "./pieces_imgs/black_knight.png", "./pieces_imgs/black_pawn.png"]
        self.draw_board(board, (-1, -1))


    def get_img(self, path):
        img = pg.image.load(path)
        img = pg.transform.scale(img, (100,100))
        return img


    def checkCell(self, x, y):
        pos_x = 0
        pos_y = 0
        if (x>1050 or x<250):
            pos_x = -1
        else:
            x -= 250 
            pos_x = x//100
        if (y<50 or y>850):
            pos_y = -1
        else:
            y -= 50
            pos_y = y // 100

        return (pos_x, pos_y)


    def get_pixels(self, pos):
        pos_x, pos_y = pos
        x, y = 250, 50
        x += pos_x * 100
        y += pos_y * 100
        return (x, y)


    def clicked_a_piece(self, board, pos):
        col, row = pos
        if board[row][col] != " ":
            return True
        return False


    def draw_piece(self, piece_tag, pos):
        #get the path and draw the img
        if piece_tag.isupper():
            paths = self.white_paths
        else:
            paths = self.black_paths

        index = -1
        if piece_tag.lower() == "k":
            index = 0
        elif piece_tag.lower() == "q":
            index = 1
        elif piece_tag.lower() == "r":
            index = 2 
        elif piece_tag.lower() == "b":
            index = 3
        elif piece_tag.lower() == "n":
            index = 4
        elif piece_tag.lower() == "p":
            index = 5
        else:
            return #empty square

        img = self.get_img(paths[index])
        rect = img.get_rect()
        x, y = self.get_pixels(pos)
        rect = rect.move([x, y])

        self.screen.blit(img, rect)


    def draw_board(self, board, selected):
        self.screen.fill(WHITE)
        pg.draw.rect(self.screen, GREY, (250, 50, 800, 800)) 
        x,y = 251, 51 #initial board pixel positions

        #draw the board
        for i in range(8):
            if(i==7):
                x -=1
            y = 51 if i%2 == 0 else 151 #starting y
            for j in range(4):
                if(j==3):
                    y -=1
                pg.draw.rect(self.screen, WHITE, (x, y, 99, 99))
                y += 200
            x+= 100

        if selected != (-1, -1): #paint the selected square
           x, y = self.get_pixels(selected)
           pg.draw.rect(self.screen, (51,102,204), (x,y,100,100)) 

        #draw letters
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        for ind in range(len(letters)):
            img = self.font.render(letters[ind], True, (0,0,0))
            self.screen.blit(img, (295 + 99*ind, 865))
        nums = ['1', '2', '3', '4', '5', '6', '7', '8'] 
        for ind in range(len(nums)):
            img = self.font.render(nums[ind], True, (0,0,0))
            self.screen.blit(img, (1080, 95 + 99*ind))

        # draw the pieces
        for row in range(len(board)):
            for col in range(len(board[row])):
                if board[row][col] != " ":
                    self.draw_piece(board[row][col], (col, row))
        pg.display.update()


    def refresh_board(self, board):
        self.draw_board(board, (-1,-1))


    def draw_promotion_selector(self, color, board):
        piece = " "
        if color == "white":
            paths = self.white_paths
        elif color == "black":
            paths = self.black_paths

        pg.draw.rect(self.screen, (0,0,0), (69, 248, 103, 403))
        
        imgs = []
        rects = []
        for i in range(4):
            pg.draw.rect(self.screen, (255,255,255), (71, 250+100*i, 99, 99))
            imgs.append(self.get_img(paths[i+1]))
            r = imgs[i].get_rect()
            rects.append(r.move([71, 250+100*i]))
            self.screen.blit(imgs[i], rects[i])
        
        pg.display.update()
        loop = True
        while loop: 
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    return (-1,-1, -1,-1)
                if event.type == MOUSEBUTTONDOWN:
                    (x, y) = pg.mouse.get_pos()
                    if x > 70 and x < 170:
                        if y > 250 and y < 350:
                            piece = "Q"
                        elif y > 350 and y < 450:
                            piece = "R"
                        elif y > 450 and y < 550:
                            piece = "B"
                        elif y > 550 and y < 650:
                            piece = "N"
                    loop = False
        
        self.draw_board(board, (-1,-1)) 
        pg.display.update()

        if color == "black":
            return piece.lower()

        return piece 


    def promotion_selector(self, old_pos, new_pos, board):
        if new_pos[1] == 0:
            if board[old_pos[1]][old_pos[0]] == "P":
                return self.draw_promotion_selector("white", board)
        elif new_pos[1] == 7:
            if board[old_pos[1]][old_pos[0]] == "p":
                    return self.draw_promotion_selector("black", board)
        return " "


    def get_input(self, board):
        running, selected = True, False
        pos = (-1, -1)

        while running:
            self.clock.tick(60)
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    return(-1,-1,-1,-1)
                if event.type == MOUSEBUTTONDOWN:
                    (x, y) = pg.mouse.get_pos()
                    (col, row) = self.checkCell(x, y)

                    if row != -1 and col != -1:
                        if selected:
                            piece = self.promotion_selector(pos, (col, row), board)  
                            if piece != " ": 
                                return (pos[1], pos[0], row, col, piece)
                            return (pos[1], pos[0], row, col)
                        else:
                            x_c, y_c = self.checkCell(x, y)
                            if self.clicked_a_piece(board, (x_c,y_c)):
                                selected = True
                                pos = self.checkCell(x, y)
                        self.draw_board(board, pos)
                    pg.display.update()

