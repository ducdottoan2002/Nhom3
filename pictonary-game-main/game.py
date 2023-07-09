import pygame
from pygame.locals import *
import ctypes
import ipaddress, server
from random import randint, random
from button import TextButton
from multiprocessing import Process
from waitingMenu import PreGame as Game
import pymongo
from profile import Profile
import os

username = "florren"
password = "florren2k2"
database = "myFirstDatabase"
cluster = pymongo.MongoClient(f"mongodb+srv://{username}:{password}@cluster0.y5mnt.mongodb.net/{database}?retryWrites=true&w=majority", connect = False)
db = cluster.insta 
cluster = db['game']
        
bgColor = (118, 188, 194)

class Home:
    idFrame = idFrame2 = 0
    
    loginMenu = True
    homeMenu = False
    hostMenu = joinMenu = launchGame = False
    bar = '|'
    
    def __init__(self):
        ctypes.windll.user32.SetProcessDPIAware()
        self.width = ctypes.windll.user32.GetSystemMetrics(0)
        self.height = ctypes.windll.user32.GetSystemMetrics(1)
        self.window = pygame.display.set_mode((self.width, self.height))#, pygame.FULLSCREEN)
        
        self.large_font = pygame.font.Font("font/Bazinga-Regular.otf", 80)
        
        self.logo1 = pygame.image.load("img/lobby/logo1.png")
        self.logo2 = pygame.image.load("img/lobby/logo2.png")
        
        self.grass1 = pygame.image.load("img/lobby/grass1.png")
        self.grass2 = pygame.image.load("img/lobby/grass2.png")
        
        self.sun = pygame.image.load("img/lobby/soleil.png")
        self.close_image = pygame.image.load("img/lobby/croix.png")
        self.back_bt = pygame.image.load("img/lobby/Back.png")
        self.cloud = pygame.image.load("img/lobby/nuage.png")
        
        self.cloud1_X = randint(-600, 1500)
        self.cloud1_G = random() / 3 + .15
        self.cloud1_Y = randint(0, 250)
        
        self.cloud2_X = randint(400, 2000)
        self.cloud2_G = -(random() / 3 + .15)
        self.cloud2_Y = randint(0, 250)
        
        self.login_button = TextButton('Login', (0, 0, 0), (int(self.width / 2), 510), self.large_font)
        self.register_button = TextButton('Create new player', (0, 0, 0), (int(self.width / 2), 680), self.large_font)
        
        self.Host_button = TextButton('Host a party', (0, 0, 0), (int(self.width / 2), 510), self.large_font)
        self.Join_button = TextButton('Join a party', (0, 0, 0), (int(self.width / 2), 680), self.large_font)
        self.IP_button = self.LAN_button = None
        
        self.is_registered = False
        self.input_Form = False
        self.warning = False
        
        self.joinWithIP = self.joinWithLAN = False
        self.IpMenu = True
        self.finish = False
        
        self.procDiffu = Process()
        self.procServer = Process()
        
        self.ip = '0.0.0.0'
        self.name = ''
        self.playerID = ''
        
        # Song in home
        pygame.mixer.music.load("music/home.mp3")
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(0.1)
        
    def checkIP(self, IP : str):
        try:          
            res = ipaddress.ip_address(IP)
            return True
        
        except:
            return False
        
    def updateDB(self):
        check = None
        user_data = self.name.split("#")
                        
        if len(user_data) != 2:
            self.warning = True
            return check
                            
        find = cluster.find_one({"name" : user_data[0], "ID" : user_data[1]})
        
        if self.is_registered == False:
            if not find:
                self.warning = True
            else:
                check = user_data
        
        else:
            if find:
                self.warning = True
                
            else:
                info = {
                    "name" : user_data[0], 
                    "ID" : user_data[1],
                    "score" : 0,
                    "game" : 0,
                    "win" : 0,
                    "lose" : 0
                    }
                
                cluster.insert_one(info)
                check = user_data
                
        return check
     
    def draw(self, pos):
        self.window.fill(bgColor)
        self.window.blit(self.logo1, self.logo1.get_rect(center=(int(self.width / 2), 100)))
        self.window.blit(self.sun, (1645, 22))
        self.window.blit(self.close_image, self.close_image.get_rect(topright=(self.width - 15, 15)))
        self.window.blit(self.back_bt, self.back_bt.get_rect(bottomleft=(25, 1020)))
        
        self.cloud1_X += self.cloud1_G
        if self.cloud1_X > 1930:
            self.cloud1_X = randint(-600, -300)
        self.window.blit(self.cloud, (int(self.cloud1_X), self.cloud1_Y))

        self.cloud2_X += self.cloud2_G
        if self.cloud2_X < -200:  
            self.cloud2_X = randint(1930, 2100)  
        self.window.blit(self.cloud, (int(self.cloud2_X), self.cloud2_Y))
    
        self.idFrame = (self.idFrame + 1) % 40 
        if self.idFrame < 20:
            self.window.blit(self.logo1, self.logo1.get_rect(center=(int(self.width / 2), 100)))
            self.window.blit(self.grass1, self.grass1.get_rect(bottomright = (self.width - 100, self.height)))
        else:
            self.window.blit(self.logo2, self.logo2.get_rect(center=(int(self.width / 2), 100)))
            self.window.blit(self.grass2, self.grass2.get_rect(bottomright = (self.width - 100, self.height)))
            
        if self.loginMenu:
            self.login_button.draw(self.window, pos)
            self.register_button.draw(self.window, pos)
            
        elif self.input_Form:
            display = self.large_font.render('Enter nickname#ID : ' + self.name + self.bar, True, (0, 0, 0))
            self.window.blit(display, (200, 530))
            
            if self.warning:
                display = self.large_font.render('Your login is invalid. Please try new one.', True, (255, 0, 0))
                self.window.blit(display, (200, 650))
        
        elif self.homeMenu:
            self.Host_button.draw(self.window, pos)
            self.Join_button.draw(self.window, pos)
            
        elif self.joinMenu:    
            if self.joinWithIP:
                textIP = self.large_font.render("Enter the IP address of the server : " + self.ip + self.bar, True, (0, 0, 0))
                self.window.blit(textIP, (200, 530))
                
            else:
                self.IP_button = TextButton('Join with IP', (0, 0, 0), (int(self.width / 2), 410), self.large_font)
                self.IP_button.draw(self.window, pos)
                
                self.LAN_button = TextButton('Join with LAN', (0, 0, 0), (int(self.width / 2), 610), self.large_font)
                self.LAN_button.draw(self.window, pos)
            
        pygame.display.update()

    def getEvent(self, pos):
        for event in pygame.event.get() :
            if event.type == pygame.QUIT or (event.type == MOUSEBUTTONDOWN and self.close_image.get_rect(topright = (self.width - 15, 15)).collidepoint(pos)):
                self.finish = True # Quit program
                
            elif event.type == MOUSEBUTTONDOWN and self.back_bt.get_rect(bottomleft = (25, 1020)).collidepoint(pos):
                self.warning = False
                
                if self.input_Form:
                    self.input_Form = False
                    self.loginMenu = True
                    self.is_registered = False
                    self.name = ""
                    
                elif self.homeMenu:
                    self.homeMenu = False
                    self.loginMenu = True
                    self.name = ""
                    
                elif self.joinMenu and self.joinWithIP:
                    self.joinWithIP = False
                    self.joinMenu = False
                    self.homeMenu = True
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: # pressed ENTER    
                    if self.input_Form and self.name.strip() != "":
                        data = self.updateDB()
                        if data is not None:
                            self.name = data[0]
                            self.playerID = data[1]
                            
                            self.warning = False
                            self.input_Form = False
                            self.homeMenu = True
                        
                    elif self.joinWithIP:
                        if self.name != '' and not self.IpMenu:
                            print('entered to Game (IP -> Game)')
                            self.launchGame = True
                            
                        elif self.IpMenu and self.checkIP(self.ip):
                            self.IpMenu = False
                        
                    elif self.joinWithLAN and self.name.strip() != '':
                        print('entered to Game (LAN -> Game) ')
                        self.launchGame = True
                        
                else:
                    if self.input_Form or not self.IpMenu:
                        if event.key == pygame.K_BACKSPACE:
                            self.name = self.name[:-1]
                            
                        elif len(self.name) < 16:
                            self.name += event.unicode 
                            
                    elif self.joinMenu and self.IpMenu:
                        if event.key == pygame.K_BACKSPACE:
                            self.ip = self.ip[:-1]
                            
                        elif len(self.ip) < 16:
                            self.ip += event.unicode
                        
            elif event.type == MOUSEBUTTONDOWN and event.button == 1: # Clicked
                if self.loginMenu:
                    if self.login_button.border_position.collidepoint(pos):
                        self.input_Form = True
                        self.loginMenu = False
                        
                    elif self.register_button.border_position.collidepoint(pos):
                        self.input_Form = True
                        self.is_registered = True
                        self.loginMenu = False
                
                elif self.homeMenu:
                    if self.Host_button.border_position.collidepoint(pos):
                        self.homeMenu = False
                        
                        self.ip = '127.0.0.1'
                        self.host = True
                        
                        # Establish self-hosted server
                        self.procDiffu = Process(target = server.connectionAgain)
                        self.procDiffu.daemon = True
                        self.procDiffu.start()
                        
                        self.procServer = Process(target = server.server)
                        self.procServer.start()
                        self.launchGame = True
                        
                        print('entered to Host ')
                        
                    elif self.Join_button.border_position.collidepoint(pos):
                        self.homeMenu = False
                        self.joinMenu = True
                        
                elif self.IpMenu:
                    if self.IP_button.border_position.collidepoint(pos):
                        self.joinWithIP = True
                        
                    elif self.LAN_button.border_position.collidepoint(pos):
                        self.launchGame = True 
    
    def run(self):
        clock = pygame.time.Clock()
        while not self.finish:
            clock.tick(80)
            pos = pygame.mouse.get_pos()
            self.draw(pos)
            self.getEvent(pos)     
            
            if self.launchGame:
                g = Game(self.name, self.playerID, self.ip.strip(), cluster, self.procDiffu, 
                         self.window, self.width, self.height)

                runGame = g.run()

                self.homeMenu = True
                self.launchGame = False
                self.joinMenu = False
                
                if self.procServer.is_alive():
                    self.procServer.terminate()
                    self.procServer.join()
                    
                    self.procDiffu.terminate()
                    self.procDiffu.join()
                    
                    self.procDiffu.daemon = False
                    
                #self.window.fill(bgColor)
                
        pygame.quit()
        
            
if __name__ == '__main__':
    pygame.font.init()
    pygame.init()
    
    g = Home()
    g.run() 