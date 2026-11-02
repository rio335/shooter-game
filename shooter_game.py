import pygame
pygame.init()
import random

#bagian variable global
lebar_scene = 400
tinggi_scene = 400
judul_scene = "penjaga antariksa"
gambar_belakang = "galaxy.jpg"
gambar_pemain = "rocket.png"
gambar_musuh = "ufo.png"
gambar_peluru = "bullet.png"
gambar_rintangan = "asteroid.png"
suara_tembak = "miaw.mp3"
suara_belakang = "rap.mp3"
GAME_RUN = True
GAME_FINISH = Falsepip
poin = 0
adoh = 0
jumlah_tembakan = 0
waktu_reload = 10

#bagian scene
scene = pygame.display.set_mode((lebar_scene, tinggi_scene))
scene.fill((0,0,0))
pygame.display.set_caption(judul_scene)
belakang = pygame.transform.scale(
    pygame.image.load(gambar_belakang), (lebar_scene, tinggi_scene)
)
fps = pygame.time.Clock()

#bagian musik
pygame.mixer.init()
pygame.mixer.music.load(suara_belakang)
pygame.mixer.music.set_volume(0.7)
pygame.mixer.music.play()
piw = pygame.mixer.Sound(suara_tembak)



###bagian tulisan
###bagian tulisan
pygame.font.init()
font1 = pygame.font.SysFont("impact", 40)
tulisan_score = font1.render("POIN:"+str(poin), True, (0,0,0))
tulisan_missed = font1.render("ADOH:"+str(adoh), True, (0,0,0))
menang = font1.render("WAH JAGO", True, (0,255,0))
kalah = font1.render("TRY AGAIN", True, (255,0,0))

### bagian class
class GameSprite(pygame.sprite.Sprite):
    def __init__(self, gambar, x, y, lebar, tinggi, kecepatan):
        super().__init__()
        self.lebar = lebar
        self.tinggi = tinggi
        self.gambar = pygame.transform.scale(
            pygame.image.load(gambar), (self.lebar, self.tinggi)
        )
        self.kecepatan = kecepatan
        self.rect = self.gambar.get_rect()
        self.rect.x = x
        self.rect.y = y
    def tampil(self):
        scene.blit(self.gambar, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def bergerak(self):
        tombol = pygame.key.get_pressed()
        if tombol[pygame.K_a] and self.rect.x>0: #kekiri
            self.rect.x -= self.kecepatan
        elif tombol[pygame.K_d] and self.rect.x<lebar_scene-self.lebar: #kekanan
            self.rect.x += self.kecepatan
    def tembak(self):
        peluru = Bullet(gambar=gambar_peluru, x=self.rect.centerx,
                        y=self.rect.top, lebar=20, tinggi=40,
                        kecepatan=5)
        grup_peluru.add(peluru)





class Enemy(GameSprite):
    def bergerak(self):
        self.rect.y += self.kecepatan
        global adoh
        if self.rect.y > tinggi_scene:
            self.rect.y = random.randint(-300, -100)
            self.rect.x = random.randint(50, lebar_scene-100)
            adoh += 1 

grup_peluru = pygame.sprite.Group()


class Bullet(GameSprite):
    def bergerak(self):
        self.rect.y -= self.kecepatan #kea atas
        if self.rect.y < -100:
            self.kill()

class Rintangan(GameSprite):
    def bergerak(self):
        self.rect.y += self.kecepatan

        if self.rect.y > tinggi_scene:
            self.rect.y = random.randint(-300, -100)
            self.rect.x = random.randint(50, lebar_scene-100)
          


###bagian sprite
pemain = Player(gambar=gambar_pemain, x=10, y=tinggi_scene-100, lebar=50, tinggi=50, kecepatan=10)

grup_musuh = pygame.sprite.Group()
jumlah_musuh = 5
for jumlah in range(jumlah_musuh):
    musuh = Enemy(gambar=gambar_musuh, x=random.randint(50,300), y=-100,
                    lebar=50, tinggi=50, kecepatan=2)
    grup_musuh.add(musuh)

grup_rintangan = pygame.sprite.Group()
jumlah_rintangan = 3
for jumlah in range(jumlah_rintangan):
    rintangan = Enemy(gambar=gambar_rintangan, x=random.randint(50,300), y=-100,
                    lebar=50, tinggi=50, kecepatan=2)
    grup_rintangan.add(rintangan)

#bagian game loop
while GAME_RUN:
    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GAME_RUN = False
        if event.type ==pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if jumlah_tembakan >= 5 and waktu_reload >= 0:
                    waktu_reload -= 1
                elif jumlah_tembakan >= 5 and waktu_reload <= 0:
                    jumlah_tembakan = 0
                    waktu_reload = 10
                elif jumlah_tembakan <= 5 and waktu_reload >= 10:
                    piw.play()
                    pemain.tembak()

    if GAME_FINISH == False:
        scene.blit(belakang, (0,0))
        tulisan_score = font1.render("POIN:"+str(poin), True, (255, 255, 255))
        tulisan_missed = font1.render("ADOH:"+str(adoh), True, (255, 255, 255))
        scene.blit(tulisan_score, (10, 10))
        scene.blit(tulisan_missed, (190, 10))

        pemain.tampil()
        for rintangan in grup_rintangan:
            rintangan.tampil()
            rintangan.bergerak()
        for musuh in grup_musuh:
            musuh.tampil()
            musuh.bergerak()
        for peluru in grup_peluru:
            peluru.tampil()
            peluru.bergerak()

        pemain.bergerak()
        if (pygame.sprite.spritecollide(pemain, grup_musuh, False) or adoh >= 10):
            scene.blit(kalah, (50, 50))
        if (pygame.sprite.spritecollide(pemain, grup_musuh, True) or poin >= 25):
            scene.blit(menang, (125, 180))
            GAME_FINISH = True
        if pygame.sprite.groupcollide(grup_peluru, grup_musuh, True, True):
            poin += 1
            #djuhd
            musuh = Enemy(gambar=gambar_musuh, x=random.randint(50,300), y=-100,
                          lebar=50, tinggi=50, kecepatan=2)
            grup_musuh.add(musuh)
        if pygame.sprite.groupcollide(grup_peluru, grup_rintangan, True, True):
            pass

    fps.tick(60)
    pygame.display.update()



