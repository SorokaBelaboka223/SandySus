import pygame
import pygame_menu
import pygame_widgets
from pygame_widgets.button import Button
import story
import map_map
from pynput import keyboard
import random
from pygame.locals import *
import webbrowser

pygame.init()

fps = pygame.time.Clock()

width = 1600
height = 900

player_name = "Игрок"
profession = 1
health = 100
mana_points = 20
day = 1
attack_type = "srd"

hide_ui = True
battle_ui = False

enemy_mob = 1

text_index = 0
story_index = 0
map_index = 0
map_menu = False

base_map_border = (map_map.map1[0][1])

# НЕ РАБОТАЕТТТ
story_text_test_file = open("code/story/TestChapter.json","r+")
story_text_test = story_text_test_file.readlines()

print(story_text_test)

game = False

first = pygame.display.set_mode((width,height))

map_img = [pygame.image.load("media/icons/map_base.png"),pygame.image.load("media/icons/map_block.png"),pygame.image.load("media/icons/map_player.png")]
inv_img = pygame.image.load("media/icons/inventory.png")
opt_img = pygame.image.load("media/icons/options.png")
backrooms = [pygame.image.load("media/background/ur_room.png"),pygame.image.load("media/background/black_room.png"),pygame.image.load("media/background/forest_1.png"),pygame.image.load("media/background/forest_gate.png")]
enemies_img = [pygame.image.load("media/chars/enemies/ork.png")]
npc_img = [pygame.image.load("media\chars/nps/aqua.png"),pygame.image.load("media\chars/nps/quard.png")]

main_story = story.chapters[story_index]
main_map = 0
print(main_story)
main_story_img = backrooms[0]

font1 = pygame.font.match_font('arial')
font = pygame.font.SysFont('Arial', 40)

def draw_text(surf, text, size, x, y):
    global main_story
    global width
    font = pygame.font.Font(font1, size)
    text_surface = font.render(text, True, (255,255,255))
    
    if "Богиня:" in main_story[text_index]:
        text_surface = font.render(text, True, (24,145,0))
        first.blit(npc_img[0],(width-700,100))
        
    if "Стражник:" in main_story[text_index]:
        text_surface = font.render(text, True, (255,0,0))
        first.blit(npc_img[1],(width-700,100))
        
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def Map_gen():
    global first
    global map_img
    for j in range(0,int(map_map.map1[int(main_map)][2])):
        for i in range(0,map_map.map1[main_map][1]):
            map = int(map_map.map1[main_map][0][j*6+i])
            if map == 1:
                first.blit(map_img[1],(100+i*200,j * 200))
            else:
                first.blit(map_img[0],(100+i*200,j * 200))
            print(map)

def Atk_Select():
    global atk_sel
    atk_sel = pygame_menu.Menu("Выбери",width , height)
    atk_sel.add.button("Ударить мечом",Set_Sword,)
    atk_sel.add.button("Выстрелить луком",Set_Bow)
    atk_sel.add.button("Использовать магию",Set_Mage)
    atk_sel.mainloop(first)

def on_release(key):
    print("Key released: {0}".format(key))
    if key == keyboard.Key.esc:
        # Stop listener
        return True

def Map_Go(map):
    global main_map
    global map_menu
    global Game_Menu
    main_map = map
    map_menu = True
    Game_Menu = False

def Next():
    global text_index
    global main_story
    global map_index
    text_index += 1

    try:
        main_story[text_index]
        
    except IndexError:
        text_index = 0
        
    if "changebackground" in main_story[text_index]:
        cache = main_story[text_index][-1]
        print(cache)
        Change_Img(cache)
        Next()
        
    if "chapter" in main_story[text_index]:
        cache = main_story[text_index][-1]
        text_index = 0
        Change_Chapter(cache)
        Next()
        
    if "NewGame" in main_story[text_index]:
        New_Game()
        Next()
        
    if "StartGame" in main_story[text_index]:
        Start_New()
        Next()
    
    if "battle" in main_story[text_index]:
         Start_Battle()
         
    if "map" in main_story[text_index]:
        cache = main_story[text_index][-1]
        map_index = cache
        Map_Go(int(cache))
        
def Open_Options():
    options = pygame_menu.Menu("", width, height, theme=pygame_menu.themes.THEME_ORANGE)
    options.add.label("Настройки", font_size = 60, font_color=(158, 54, 37))
    options.add.vertical_margin(40)
    options.add.label("Громкость:", font_size = 40, font_color=(158, 54, 37))
    options.add.range_slider("Музыка",100,(0,100),10,Set_v, font_color=(0,0,0))
    options.add.range_slider("Эффекты",100,(0,100),10,Set_vx, font_color=(0,0,0))
    options.add.vertical_margin(20)
    options.add.label("Общее:", font_size = 40, font_color=(158, 54, 37))
    options.add.dropselect("Трек  -",[("Chainsaw Man Op1",1),("The a la menthe",2),("Erica(German)",3),("OMGF - Hello",4),("PigStep(Minecraft)",5),("Мы стреляем по...",6),("Russian athem",7),("Xenogenesis",8),("Safe and Sound",9),("Wither Storm Ost",10)],
                            onchange=set_music, font_color=(0,0,0),placeholder="Chainsaw Man Op1",default=0,placeholder_add_to_selection_box=False,selection_box_border_width=(1))
    options.add.dropselect("Тема  -", [("Оригинал",1),("Pvz NEW", 2),("jojo",3),("GDash",4),("Minecraft",5)],
                            onchange=lambda: print("yahe"), font_color=(0,0,0),placeholder="Chainsaw Man Op1",default=0,placeholder_add_to_selection_box=False)
    options.add.button("Полный экран", fulscr, font_color=(0,0,0),cursor=SYSTEM_CURSOR_ARROW)
    options.add.button("Сбросить рекорд", reset_top, font_color=(0,0,0))
    options.add.vertical_margin(20)
    options.add.label("Другое:", font_size = 40, font_color=(158, 54, 37))
    options.add.url("https://www.youtube.com/watch?v=dQw4w9WgXcQ","О нас")
    options.add.button("Changelog",lambda: print("yahe"))
    options.add.vertical_margin(40)
    options.add.button("Закрыть", lambda: options.disable(), selection_color=(255,0,0), font_color=(144,2,2))
    options.mainloop(first)

button_Main_Text = Button(
    # Mandatory Parameters
    first,  # Surface to place button on
    width/2-150,  # X-coordinate of top left corner
    height -50-150,  # Y-coordinate of top left corner
    900,  # Width
    150,  # Height

    # Optional Parameters
    text='Дальше',  # Text to display
    fontSize=50,  # Size of font
    margin=20,  # Minimum distance between text/image and edge of button
    inactiveColour=(200, 50, 0),  # Colour of button when not being interacted with
    hoverColour=(150, 0, 0),  # Colour of button when being hovered over
    pressedColour=(220, 70, 20),  # Colour of button when being clicked
    radius=20,  # Radius of border corners (leave empty for not curved)
    onClick=Next  # Function to call when clicked on
)

button_Inv = Button(
    # Mandatory Parameters
    first,  # Surface to place button on
    width/2-325,  # X-coordinate of top left corner
    height -50-150,  # Y-coordinate of top left corner
    150,  # Width
    150,  # Height

    # Optional Parameters
    text='',  # Text to display
    fontSize=50,  # Size of font
    margin=20,  # Minimum distance between text/image and edge of button
    inactiveColour=(200, 50, 0),  # Colour of button when not being interacted with
    hoverColour=(150, 0, 0),  # Colour of button when being hovered over
    pressedColour=(220, 70, 20),  # Colour of button when being clicked
    radius=60,  # Radius of border corners (leave empty for not curved)
    onClick=lambda: print("click")  # Function to call when clicked on
)
button_Inv.image = inv_img

button_Opt = Button(
    # Mandatory Parameters
    first,  # Surface to place button on
    width/2-325 - 175,  # X-coordinate of top left corner
    height -50-150,  # Y-coordinate of top left corner
    150,  # Width
    150,  # Height


    # Optional Parameters
    text='',  # Text to display
    fontSize=50,  # Size of font
    margin=20,  # Minimum distance between text/image and edge of button
    inactiveColour=(200, 50, 0),  # Colour of button when not being interacted with
    hoverColour=(150, 0, 0),  # Colour of button when being hovered over
    pressedColour=(220, 70, 20),  # Colour of button when being clicked
    radius=60,  # Radius of border corners (leave empty for not curved)
    onClick=Open_Options  # Function to call when clicked on
)
button_Opt.image = opt_img

button_Atk = Button(
    # Mandatory Parameters
    first,  # Surface to place button on
    width/2-325 - 175,  # X-coordinate of top left corner
    height -50-150,  # Y-coordinate of top left corner
    150,  # Width
    150,  # Height


    # Optional Parameters
    text='Атака',  # Text to display
    fontSize=50,  # Size of font
    margin=20,  # Minimum distance between text/image and edge of button
    inactiveColour=(200, 50, 0),  # Colour of button when not being interacted with
    hoverColour=(150, 0, 0),  # Colour of button when being hovered over
    pressedColour=(220, 70, 20),  # Colour of button when being clicked
    radius=60,  # Radius of border corners (leave empty for not curved)
    onClick=Atk_Select  # Function to call when clicked on
)

button_Def = Button(
    # Mandatory Parameters
    first,  # Surface to place button on
    width/2-325,  # X-coordinate of top left corner
    height -50-150,  # Y-coordinate of top left corner
    150,  # Width
    150,  # Height

    # Optional Parameters
    text='Защита',  # Text to display
    fontSize=50,  # Size of font
    margin=20,  # Minimum distance between text/image and edge of button
    inactiveColour=(200, 50, 0),  # Colour of button when not being interacted with
    hoverColour=(150, 0, 0),  # Colour of button when being hovered over
    pressedColour=(220, 70, 20),  # Colour of button when being clicked
    radius=60,  # Radius of border corners (leave empty for not curved)
    onClick=lambda: print("click")  # Function to call when clicked on
)

button_Skip = Button(
    # Mandatory Parameters
    first,  # Surface to place button on
    width/2-150,  # X-coordinate of top left corner
    height -50-150,  # Y-coordinate of top left corner
    900,  # Width
    150,  # Height

    # Optional Parameters
    text='Пропустить',  # Text to display
    fontSize=50,  # Size of font
    margin=20,  # Minimum distance between text/image and edge of button
    inactiveColour=(200, 50, 0),  # Colour of button when not being interacted with
    hoverColour=(150, 0, 0),  # Colour of button when being hovered over
    pressedColour=(220, 70, 20),  # Colour of button when being clicked
    radius=20,  # Radius of border corners (leave empty for not curved)
    onClick=Next  # Function to call when clicked on
)

def Victory():
    global battle_ui
    global hide_ui
    battle_ui = False
    hide_ui = False
    First_Menu.disable()
    button_Atk.disable()
    button_Def.disable()
    button_Skip.disable()
    First_Menu.disable_render()
    button_Atk.hide()
    button_Def.hide()
    button_Skip.hide()

    Next()

class Enemy():
    def __init__(self,h,a):
        self.health = h
        self.attack = a
        self.image = enemies_img[0]
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        
    def Attack(self):
        p1.health-= self.attack
    def update(self):
        if self.health <= 0:
            Victory()
        first.blit(self.image, (height - self.rect.x,self.rect.y))


ork = Enemy(random.randint(20, 60),random.randint(10,20))    
            
class Map():
    def __init__(self,mapmap):
        global map_index
        global main_map
        if mapmap == 1:
            self.image = pygame.image.load("media/icons/map_block.png")
        elif mapmap == 2:
            self.image = pygame.image.load("media/icons/map_base.png")
    def update(self,x,y):
        first.blit(self.image,(x,y))
    
class Player():
    def __init__(self):
        global player_name
        global profession
        global height
        global mana_points
        self.health = health
        self.mana = mana_points
        self.name = player_name
        self.profession = profession
        self.cords = [0,1]
        print(self.name, self.profession)
        
        if self.profession == 1:
            self.swordskill = 2
            self.swordskillxp = 0
            self.swordskillxpmax = 140
            print(self.swordskill)
        else:
            self.swordskill = 0
            self.swordskillxp = 0
            self.swordskillxpmax = 100
            print(self.swordskill)
        
        if self.profession == 2:
            self.bowskill = 2
            self.bowskillxp = 0
            self.bowskillxpmax = 140
            print(self.bowskill)
        else:
            self.bowskill = 0
            self.bowskillxp = 0
            self.bowskillxpmax = 100
            print(self.bowskill)
        
        if self.profession == 3:
            self.mageskill = 2
            self.mageskillxp = 0
            self.mageskillxpmax = 140
            self.mana = 30
            print(self.mageskill)
        else:
            self.mageskill = 0
            self.mageskillxp = 0
            self.mageskillxpmax = 100
            print(self.mageskill)
        
        if self.profession == 4:
            self.durskill = 2
            self.durskillxp = 0
            self.durskillxpmax = 140
            self.swordskill = 1
            self.swordskillxp = 0
            self.swordskillxpmax = 120
            self.health = 140
            print(self.durskill)
        else:
            self.durskill = 0
            self.durskillxp = 0
            self.durskillxpmax = 100
            print(self.durskill)
        
    def lvlupcheck(self):
        if self.swordskillxp >= self.swordskillxpmax:
            self.swordskill += 1
            self.swordskillxp -= self.swordskillxpmax
            self.swordskillxpmax += 20
            
        if self.bowskillxp >= self.bowskillxpmax:
            self.bowskill += 1
            self.bowskillxp -= self.bowskillxpmax
            self.bowskillxpmax += 20
            
        if self.mageskillxp >= self.mageskillxpmax:
            self.mageskill += 1
            self.mageskillxp -= self.mageskillxpmax
            self.mageskillxpmax += 20
            self.mana += 5

        if self.durskillxp >= self.durskillxpmax:
            self.durskill += 1
            self.durskillxp -= self.durskillxpmax
            self.durskillxpmax += 20
            self.health += 20
    def Atk(self, type, mob):
        if type == "srd":
            mob.health -=  10 * self.swordskill
            self.swordskillxp += 20
            
        if type == "bow":
            mob.health -=  10 * self.bowskill
            self.bowskillxp += 20

        if type == "mag":
            mob.health -=  10 * self.mageskill
            self.mageskillxp += 20

def set_resolution(name, id):
    global width
    global height
    
    ph = name[0]
    
    res = ph[0].split("/")
    
    width = int(res[0])
    height = int(res[1])
    
def complete():
    global first
    # resolutionselector.disable()
    first = pygame.display.set_mode((width,height))
themeM = pygame_menu.Theme(title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_NONE)

# resolutionselector = pygame_menu.Menu("", 700, 200,theme = themeM)
# resolutionselector.add.dropselect("Screescreen resolution:",[("1600/900",1),("1920/1080",4)],0, onchange=set_resolution,placeholder_add_to_selection_box=False)
# #resolutionselector.add.dropselect("Language: ",[("Engilsh",1),("Русский", 2)],0,placeholder_add_to_selection_box=False, onchange=Language)
# resolutionselector.add.button("Select", complete)
# resolutionselector.mainloop(first)

pygame.display.set_caption("GAMESS")

def New_Persone():
    global p1

    p1 = Player()

def Set_Sword():
    global attack_type
    attack_type = "srd"
    New_Step(attack_type,enemy_mob)

def Set_Bow():
    global attack_type
    attack_type = "bow"
    New_Step(attack_type,enemy_mob)
    
def Set_Mage():
    global attack_type
    attack_type = "mag"
    New_Step(attack_type,enemy_mob)
    
def set_music(name, p):
    pygame.mixer.music.load("music/song"+str(p)+".mp3")
    pygame.mixer.music.play(-1)
        
def set_difficulty(name, id):
    global speed
    speed = id * 2
    if id >= 2:
         speed - 6

def Set_v(id):
     negr = id / 100
     pygame.mixer.music.set_volume(negr)

def Set_vx(id):
     negr = id / 100

def reset_top():
     global top
     top = 0

def Set_Profession(name,id):
    global profession
    profession = id
    
def Set_Name(name):
    global player_name
    player_name = name

def Start_New():
    global hide_ui
    hide_ui = False
    Change_Img(2)

def Start_Battle():
    global enemy_mob
    global hide_ui
    global battle_ui
    p1.health = 100 + 20*p1.durskill
    hide_ui = True
    battle_ui = True
    enemy_mob = Enemy(random.randint(20, 60),random.randint(10,20)) 
    First_Menu.enable()
    button_Atk.enable()
    button_Def.enable()
    button_Skip.enable()
    button_Atk.show()
    button_Def.show()
    button_Skip.show()


def Change_Chapter(i):
    global story_index
    global main_story
    story_index = int(i)
    main_story = story.chapters[story_index]

def Change_Img(i):
    global background_rect
    global main_story_img
    main_story_img = backrooms[int(i)]
    background = pygame.transform.scale(main_story_img, (width, height))
    background_rect = background.get_rect()

def fulscr():
     pygame.display.toggle_fullscreen()
def StartGame():
    New_Persone()
    # Change_Img(0)
    Selection_Menu.disable()

def New_Step(p,Enemy):
    global atk_sel
    Enemy.Attack()
    p1.Atk(p,Enemy)
    atk_sel.disable()

def New_Game():
    global First_Menu
    global Selection_Menu
    First_Menu.disable()
    Selection_Menu = pygame_menu.Menu("Настройка персонажа",width , height)
    Selection_Menu.add.text_input("Имя: ","Игрок",onchange=Set_Name)
    Selection_Menu.add.dropselect("Профессия",[("Мечник", 1),("Лучник", 2),("Маг", 3),("Выживальщик", 4)],placeholder="Выбери свою",onchange=Set_Profession)
    Selection_Menu.add.toggle_switch("Пол:",state_text=("Мужской","Женский"),width = 200)
    Selection_Menu.add.button("Продолжить",StartGame)
    Selection_Menu.mainloop(first)

def Close_First_Menu():
    Change_Img(0)
    First_Menu.disable()
    button_Atk.disable()
    button_Def.disable()
    button_Skip.disable()
    First_Menu.disable_render()
    button_Atk.hide()
    button_Def.hide()
    button_Skip.hide()

def First_Menu_Load():
    global First_Menu
    First_Menu = pygame_menu.Menu("GAMESS VALPHA 0,05",width,height)
    First_Menu.add.button("Новая Игра",Close_First_Menu)
    First_Menu.add.button("Продолжить")
    First_Menu.add.button("Выйти")
    First_Menu.mainloop(first)

def onlytest(i):
    global background_rect
    global main_story_img
    main_story_img = backrooms[int(i)]
    background = pygame.transform.scale(main_story_img, (width, height))
    background_rect = background.get_rect()

First_Menu_Load()
Next()


Game_Menu = True
ali = True

while ali:
    events = pygame.event.get()
    gkey = pygame.key.get_pressed()
    
    if Game_Menu:
        first.blit(main_story_img, background_rect)
        
        if battle_ui:
            enemy_mob.update()
            draw_text(first,"hp: "+str(enemy_mob.health),20,height / 2, 200)
            draw_text(first,"hp: "+str(p1.health),20,100,height - 200)
            draw_text(first,"mana: "+str(p1.mana),20,100,height - 150)
            button_Atk.draw()
            button_Def.draw()
            button_Skip.draw()
            
        else:
            if hide_ui:
                pass
            
            else:
                draw_text(first,player_name,20,100,height - 200)
                draw_text(first,"День"+str(day),20,100,height - 150)
                button_Opt.draw()
                button_Inv.draw()
            draw_text(first,main_story[text_index],20,width /2,height /2 + 200)
            button_Main_Text.draw()
    elif map_menu:
        Map_gen()
        
    pygame.display.flip()
    pygame_widgets.update(events)
    
    fps.tick(60)
    
    if gkey[K_ESCAPE]:
        ali = False

pygame.quit()