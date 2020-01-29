import pygame 
vec = pygame.math.Vector2
from Block import *



#vec = pygame.math.Vector2

class Player(pygame.sprite.Sprite):
    
    def __init__(self, x, y, platforms, width = 30, height = 50, mass = 1):
        pygame.sprite.Sprite.__init__(self)
        self.currentSprite = 0
        self.lastTicks = 0
        self.walking = False
        self.load_images()
        self.image = self.standing[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.lightRect = lightAlpha.get_rect()
        self.lightRect.center = (x,y)
        
#        self.rect.left = x-15
#        self.rect.right = x+15
#        self.rect.bottom = y-25
#        self.rect.top = y+25
        print(self.rect)
        print(self.rect.top)
        print(self.rect.bottom)
        self.width = width
        self.height = height
        self.platforms = platforms
        self.mass = mass
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.position = vec(x, y)
        self.platforming = True
        self.isJump = False
        
    def get_images(self, a, b, wid, hei):
        sprite = pygame.image.load('Assets/Walking.png').convert()
        getimage = pygame.Surface((wid,hei))
        getimage.blit(sprite,(0,0),(a,b,wid,hei))
        getimage = pygame.transform.scale(getimage,(wid, hei))
        return getimage

    def load_images(self):
        self.standing = [self.get_images(20, 20, 29, 50), self.get_images(20, 80, 29, 50)]
        for pic in self.standing:
            pic.set_colorkey((0,0,0))
        self.walkRight = [self.get_images(20,140,29,50), self.get_images(59, 20, 29, 50),self.get_images(59, 80, 29, 50),
                          self.get_images(59,140,29,50), self.get_images(98, 20, 29, 50),self.get_images(137, 20, 29, 50),
                          self.get_images(176,20,29,50), self.get_images(98, 80, 29, 50),self.get_images(98, 140, 29, 50),
                          self.get_images(137, 80, 29, 50)]
        self.walkLeft = []
        for pic in self.walkRight:
            pic.set_colorkey((0,0,0))
            self.walkLeft.append(pygame.transform.flip(pic, True, False))
        self.jumpSprite = []

    def getX(self):
        return self.rect.left
        
    def getY(self):
        return self.rect.top
        
    def jumpCheck(self):
        if not(self.isJump):
            self.isJump =True

    def jump(self):
        #jump only if velocity y = 0
        if self.isJump:
            if self.vel.y == 0:
                self.vel.y = -17
                self.isJump = False
        # self.rect.x += 1
#         hits=pygame.sprite.spritecollide(self, self.platforms, False)
#         self.rect.x -= 1
      #   if hits:
#             self.vel.y = -17

    def hitX(self):
        for platform in self.platforms:
            #hit = self.rect.colliderect(platform)
            
            if self.rect.colliderect(platform):
                #left
                if self.vel.x > 0:
                    self.position.x = platform.rect.left - (self.width/2)
                    self.vel.x = 0
                #right
                elif self.vel.x < 0:
                    self.position.x = platform.rect.right + (self.width/2)
                    self.vel.x = 0
                        
    def hitY(self):
        for platform in self.platforms:
            #hit = self.rect.colliderect(platform)
            
            if self.rect.colliderect(platform):
                #top
                if self.vel.y > 0:
                    self.position.y = platform.rect.top
                    self.vel.y = 0
                #bottom
                elif self.vel.y < 0:
                    self.position.y = platform.rect.bottom + self.height
                    self.vel.y = 0


    def update(self):
        self.motion()
        self.acc = vec(0,0.98)
        #self.hit()
        #self.acc = vec(0,0.98)
#       self.vel.x = 0
        keys = pygame.key.get_pressed()
        if self.position.y > 595:
            self.position.y = 0
        if self.position.x < 5:
            self.position.x = 5
        if self.position.x > 795:
            self.position.x = 795
        #print(self.rect.x)
        #print(self.rect.y)
        
        if keys[pygame.K_LEFT]:
            if self.position.x < 0+self.width+self.vel.x:
                self.acc.x = 0
                self.vel.x = 0
            else:
                self.acc.x = -0.9
        if keys[pygame.K_RIGHT]:
            if self.position.x > 800-self.width/2-self.vel.x:
                self.acc.x = 0
                self.vel.x = 0
            else:
                self.acc.x = 0.9

        self.acc.x += self.vel.x*(-0.1)
        self.vel += self.acc
        if abs(self.vel.x) < 0.6:
            self.vel.x = 0 
        
        self.position[0] += self.vel[0] + 0.5*self.acc[0]
        self.rect.midbottom = self.position
        
        self.hitX()
        
        self.position[1] += self.vel[1] + 0.5*self.acc[1]
        self.rect.midbottom = self.position
        
        self.hitY()
        
        self.rect.midbottom = self.position
        self.lightRect.center = self.position

    def motion(self):
        nowTicks = pygame.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False
        if self.walking:
            if nowTicks - self.lastTicks > 50:
                self.lastTicks = nowTicks
                if self.vel.x > 0:
                    self.currentSprite = (self.currentSprite+1)%len(self.walkRight)
                    self.image = self.walkRight[self.currentSprite] 
                if self.vel.x < 0:
                    self.currentSprite = (self.currentSprite+1)%len(self.walkLeft)
                    self.image = self.walkLeft[self.currentSprite]
                bottom = self.rect.bottom
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        if not self.walking and not self.isJump:
            if nowTicks - self.lastTicks > 500:
                self.lastTicks = nowTicks
                self.currentSprite = (self.currentSprite+1)% len(self.standing)
                bottom = self.rect.bottom
                self.image = self.standing[self.currentSprite]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom




'''
class Player(pygame.sprite.Sprite):
    
    def __init__(self, x, y, platforms, width = 30, height = 50, mass = 1):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30,50))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.lightRect = lightAlpha.get_rect()
        self.lightRect.center = (x,y)
        
        self.width = width
        self.height = height
        self.platforms = platforms
        self.mass = mass
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.position = vec(x, y)
        self.isJump = False
        self.hasKey = False
        pygame.mixer.init()
        
    def getX(self):
        return self.rect.left
        
    def getY(self):
        return self.rect.top
        
    def jumpCheck(self):
        if not(self.isJump):
            self.isJump =True

    def jump(self):
		#jump only if velocity y = 0
        if self.isJump:
            if self.vel.y == 0:
                self.vel.y = - 10
            else:
                self.isJump = False
    
    def update(self):
        self.acc = vec(0,0.98)
#		self.vel.x = 0
        keys = pygame.key.get_pressed()
        if self.position.y > 595:
            self.position.y = 0
        if self.position.x < 3:
            self.position.x = 3
        if self.position.x > 795:
            self.position.x = 795
        for platform in self.platforms:
            if self.rect.colliderect(platform):
                if self.isJump == False:
                    self.rect.bottom = platform.rect.top
                    self.vel.y = 0
                    self.acc.y = 0
                else:
                    #figure this out
                    print("jumping")
                    
        move_sound=pygame.mixer.Sound('Audio/WALKING_flt.ogg')
        if keys[pygame.K_LEFT]:
               
            move_sound.set_volume(.4)
            pygame.mixer.Sound.play(move_sound)

            if self.position.x < 0+self.width+self.vel.x:
                self.acc.x = 0
                self.vel.x = 0
            else:
                self.acc.x = -1
            
        if keys[pygame.K_RIGHT]:

            move_sound.set_volume(.4)
            pygame.mixer.Sound.play(move_sound)
            
            if self.position.x > 800-self.width/2-self.vel.x:
                self.acc.x = 0
                self.vel.x = 0
            else:
                self.acc.x = 1

        self.acc.x += self.vel.x*(-0.1)
        self.vel += self.acc
        self.position += self.vel + 0.5*self.acc
        self.rect.center = self.position
        self.lightRect.center = self.position
'''