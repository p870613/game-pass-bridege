import pygame as pg
import sys
from pygame.locals import *
from easygui import *
import random
        
#視窗初始
pg.init()
screen_size = (800, 440)
screen = pg.display.set_mode(screen_size, RESIZABLE, 32)  
pg.display.set_caption("PLAY Fun")

#背景
bg = pg.Surface(screen.get_size())
bg = bg.convert()
bg.fill((255, 255, 255))

#背景圖片
bg_img = pg.image.load('background.png').convert()

#fire
fire_img = pg.image.load('fire.png').convert()
fire_pos_right = (205, 220)
fire_pos_left = (550, 200)
fire_side = 0
fire_pos = fire_pos_right

#字體
total_cost_font = pg.font.SysFont("arial", 28)
ball_font = pg.font.SysFont("arial", 16)

#number
play_value = []
color = [(0,0,255), (0,255,255), (255,0,0), (255, 123,255)]

#ball aru
angle = [(20,20), (20, 20), (20, 20), (20, 20)]
radius = 20
width = 0

#位子
right_pos = [(20, 195), (64, 201), (114,213), (162,217)]
left_pos = [(620, 201), (670, 192), (712, 188), (758, 186)]
right_pos_queue = []
left_pos_queue = [(620, 201), (670, 192), (712, 188), (758, 186)]
right_pos_pass_bridge = [(188, 217), (194, 225)]
left_pos_pass_bridge = [(596, 209),(574, 212)]

#queue
pass_queue = []
pass_queue_index = []
pass_queue_pos = [(668, 60), (741, 60)]

#total_cost 
total_cost_text = total_cost_font.render("0", True, (0, 0, 0))

#過橋pos
bridege_button_pos_x = [294, 518]
bridege_button_pos_y = [328, 428]

#animation_bool
animation = False

min_cost = 0 #0play_value[1] +  play_value[2] + play_value[3] + 2 * play_value[0]

class ball_text:
     ball_cost_text = ball_font.render("", True, (0, 0, 0))
     ball_object = ball_cost_text.get_rect()
     text = ""
     #center = (0, 0)

     def set_value(self, num):
          self.text = str(play_value[num])
          self.ball_cost_text = ball_font.render(self.text, True, (0, 0, 0))
          self.ball_object = self.ball_cost_text.get_rect()
          self.ball_object.center = right_pos[num]
          
     def get_value(self):
          return self.text

     def change_text_pos(self, center):
          self.ball_object.center = center
     
class ball(ball_text):
     ball_surface = pg.Surface((40,40))
     ball_surface.set_alpha(100)
     rect = ball_surface.get_rect()
     speed = 0
     x = 0
     y = 0
     side = 0 # 0 -> right, 1 -> left 
     def __init__(self, background_color):
          super(ball_text, self).__init__()
          self.ball_surface.fill((255,255,255))
          self.rect = self.ball_surface.get_rect()
          self.rect.center = right_pos[background_color]
          self.x, self.y = self.rect.topleft
          self.speed = 10
          self.side = 0
          self.set_value(background_color)
          
     def paint(self, num):
          pg.draw.circle(self.ball_surface, color[num], angle[num], radius, width)

     def get_center(self):
          return self.rect.center

     def change_ball_pos(self, center):
          self.rect.center = center
          self.x, self.y = self.rect.topleft
          self.change_text_pos(center)

if(__name__ == '__main__'):     
     clock = pg.time.Clock()
     for i  in range(4):
          play_value.append(int((random.random()*100) % 100))
     play_value.sort()
     min_cost = play_value[1] +  play_value[2] + play_value[3] + 2 * play_value[0]
     
     a = [ball(0), ball(1), ball(2), ball(3)]
     run = True
     cost = 0
     while run:
          clock.tick(10)
          for item in pg.event.get():
               if item.type == pg.QUIT:
                    run = False
          if(animation == True):
               fire_x, fire_y = fire_pos
               #檢查動畫是否停止
               if(fire_side == 0):
                    fire_left_x, fire_left_y = fire_pos_left
                    if(fire_x >= fire_left_x):
                         for i in pass_queue_index:         
                              a[i].change_ball_pos(left_pos_queue[0])
                              del left_pos_queue[0]
                              a[i].side = 1
                         fire_side = 1     
                         animation = False
                         pass_queue = []
                         pass_queue_index = []
                         #過關
                         if(len(right_pos_queue) == 4):
                              if(cost <= min_cost):
                                   msgbox("比我公式厲害!? 不錯! 不錯!")
                              else:
                                   msgbox("雖然沒我厲害 不過勉強過關")
                                     
               else:
                    fire_right_x, fire_right_y = fire_pos_right
                    if(fire_x <= fire_right_x):
                         for i in pass_queue_index:         
                              a[i].change_ball_pos(right_pos_queue[0])
                              del right_pos_queue[0]
                              a[i].side = 0
                         fire_side = 0     
                         animation = False
                         pass_queue = []
                         pass_queue_index = []
               #球的移動
               if(animation == True):
                    for i in pass_queue_index:
                         if(a[i].side == 0):
                              tmp_x = a[i].get_center()[0] + a[i].speed
                              tmp_y = a[i].get_center()[1] 
                              a[i].change_ball_pos((tmp_x, tmp_y))
                         else:
                              tmp_x = a[i].get_center()[0] - a[i].speed
                              tmp_y = a[i].get_center()[1] 
                              a[i].change_ball_pos((tmp_x, tmp_y))
                    if(fire_side == 0):
                         tmp_fire_pos = fire_pos[0] + a[i].speed
                         fire_pos = (tmp_fire_pos, fire_pos[1])
                    else:
                         tmp_fire_pos = fire_pos[0] - a[i].speed
                         fire_pos = (tmp_fire_pos, fire_pos[1])
                    
          else:
               #當滑鼠按下去的時候
               if(pg.mouse.get_pressed() == (1, 0, 0)):
                    (cur_mouse_pos_x, cur_mouse_pos_y) = pg.mouse.get_pos()
                    #點球
                    for i in range (len(a)):
                         (x, y) = a[i].get_center()
                         cur_x_max = x + 20
                         cur_x_min = x - 20
                         cur_y_max = y + 20
                         cur_y_min = y - 20
                         if(cur_mouse_pos_x <= cur_x_max and cur_mouse_pos_x >= cur_x_min and cur_mouse_pos_y <= cur_y_max
                            and cur_mouse_pos_y >= cur_y_min):                              
                              #queue
                              if(len(pass_queue) == 2):
                                   if(a[i].text != pass_queue[0] and a[i].text != pass_queue[1]):
                                        del pass_queue[0]
                                        del pass_queue_index[0]
                                        pass_queue.append(a[i].text)
                                        pass_queue_index.append(i)
                              else:          
                                   pass_queue.append(a[i].text)
                                   pass_queue_index.append(i)

                              #重複
                              if(len(pass_queue) == 2):
                                   if(pass_queue[0] == pass_queue[1]):
                                        del pass_queue[0]
                                        del pass_queue_index[0]
                                   
                              #要相同的side
                              if(len(pass_queue) == 2):
                                   if(a[pass_queue_index[0]].side != a[pass_queue_index[1]].side):
                                        del pass_queue[0]
                                        del pass_queue_index[0]
                    #過橋button
                    if(cur_mouse_pos_x >= bridege_button_pos_x[0] and cur_mouse_pos_x <= bridege_button_pos_x[1]
                       and cur_mouse_pos_y >= bridege_button_pos_y[0] and cur_mouse_pos_y <= bridege_button_pos_y[1]):
                         if(fire_side == a[pass_queue_index[0]].side):
                              #改變值
                              index = 0
                              animation = True
                              for i in pass_queue_index:
                                   if(a[i].side == 0):
                                        right_pos_queue.append(a[i].rect.center)
                                        a[i].change_ball_pos(right_pos_pass_bridge[index])
                                        index = index + 1
                                   else:
                                        left_pos_queue.append(a[i].rect.center)
                                        a[i].change_ball_pos(left_pos_pass_bridge[index])
                                        index = index + 1
                              #cost
                              max = 0
                              for i in pass_queue_index:
                                   if(max < int(a[i].text)):
                                        max = int(a[i].text)
                              cost = cost + max
                                   
                         else:
                              msgbox(msg="fire必要移動的必須在同一邊", title = 'message')
               
          screen.blit(bg, (0,0))
          screen.blit(bg_img, (0, 0))
          screen.blit(fire_img, fire_pos)
          for i in range(len(a)):
               a[i].paint(i)
               screen.blit(a[i].ball_surface, a[i].rect.topleft)
               a[i].ball_cost_text = ball_font.render(a[i].text, True, (0, 0, 0))
               screen.blit(a[i].ball_cost_text, a[i].ball_object.topleft)
               

          queue_count = 0
          if(len(pass_queue) != 0):
               for i in pass_queue:
                    queue_text = total_cost_font.render(i, True, (0, 0, 0))
                    screen.blit(queue_text, pass_queue_pos[queue_count])
                    queue_count = queue_count + 1
          #change total cost
          total_cost_text = total_cost_font.render(str(cost), True, (0, 0, 0))
          screen.blit(total_cost_text, (673, 15))
          
          pg.display.update()
     print(min_cost)
     pg.quit()   


