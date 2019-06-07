import pygame, math, random, time, sys
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()
screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
pygame.mouse.set_visible(False)
pygame.display.set_caption("Howdy Pressing")
icon = pygame.image.load("Icon.png")
pygame.display.set_icon(icon)
environment_image = pygame.image.load("Environment.png")
sun_image = pygame.image.load("Sun.png")
player_sprite = pygame.image.load("CowboyFire.png")
enemy_sprite = pygame.image.load("CowboyFireAlt.png")
player_death = pygame.image.load("CowboyDie.png")
enemy_death = pygame.image.load("CowboyDieAlt.png")
title_screen = pygame.image.load("TitleScreen.png")
title_image = pygame.image.load("Title.png")
win_screen = pygame.image.load("WinScreen.png")
lose_screen = pygame.image.load("LoseScreen.png")
cloud1_image = pygame.image.load("ACloud1.png")
cloud2_image = pygame.image.load("Cloud2.png")
cloud3_image = pygame.image.load("Cloud3.png")
return_hint_image = pygame.image.load("ReturnHint.png")
space_hint_image = pygame.image.load("SpaceHint.png")
game_state = 0
clock = pygame.time.Clock()
cloud_layers = list()
pygame.mixer.music.load("WildWestMusic.mp3")
gunshot_sound = pygame.mixer.Sound("Gunshot.wav")
def clear_stack():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
def check_exit():
    current_keys = pygame.key.get_pressed()
    if current_keys[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()
class Fighter:
    def __init__(self, image, rect, n_sprites, sprite_delay, orientation, fire_frame, death_image, n_death):
        self.image = image
        self.rect = rect
        self.sprite_state = 0
        self.frame_counter = 0
        self.dead = False
        self.fire_frame = fire_frame
        self.n_sprites = n_sprites
        self.sprite_delay = sprite_delay
        self.death_image = death_image
        self.n_death = n_death
        self.orientation = orientation
        self.fired = False
        self.finished = False
        if self.orientation == "vertical":
            self.sprite_height = self.image.get_height() / self.n_sprites
            self.sprite_width = self.image.get_width()
            self.death_sprite_height = self.death_image.get_height() / self.n_death
            self.death_sprite_width = self.death_image.get_width()
        elif self.orientation == "horizontal":
            self.sprite_height = self.image.get_height()
            self.sprite_width = self.image.get_width() / self.n_sprites
            self.death_sprite_height = self.death_image.get_height()
            self.death_sprite_width = self.death_image.get_width() / self.n_death
    def draw(self):
        if self.dead == False:
            if self.orientation == "vertical":
                sprite_rect = pygame.Rect(0, (self.sprite_height * self.sprite_state), self.sprite_width, self.sprite_height)
            elif self.orientation == "horizontal":
                sprite_rect = pygame.Rect((self.sprite_width * self.sprite_state), 0, self.sprite_width, self.sprite_height)
            screen.blit(self.image, self.rect, sprite_rect)
        else:
            if self.orientation == "vertical":
                sprite_rect = pygame.Rect(0, (self.death_sprite_height * self.sprite_state), self.death_sprite_width, self.death_sprite_height)
            elif self.orientation == "horizontal":
                sprite_rect = pygame.Rect((self.death_sprite_width * self.sprite_state), 0, self.death_sprite_width, self.death_sprite_height)
            screen.blit(self.death_image, self.rect, sprite_rect)
    def die(self):
        if self.finished == False:
            self.frame_counter += 1
            if self.frame_counter % 2 == 0:
                self.sprite_state += 1
            if self.sprite_state + 1 >= self.n_death:
                self.finished = True
class EnemyFighter(Fighter):
    def setup_round(self):
        self.anim_start_frame = random.randint(20, 100)
        self.frame_counter = 0
        self.sprite_state = 0
    def check_fire(self):
        if self.fired == False:
            if self.frame_counter == self.anim_start_frame:
                self.fired = True
    def update(self):
        if self.dead == False:
            self.frame_counter += 1
            if self.fired == True:
                if (self.frame_counter - self.anim_start_frame) % self.sprite_delay == 0:
                    self.sprite_state += 1
                if self.sprite_state == self.fire_frame:
                    if player_fighter.dead == False:
                        pygame.mixer.Sound.play(gunshot_sound)
                        player_fighter.dead = True
                        lose_sign.rect.topleft = lose_sign.pos2
                        lose_sign.direction = 1
                        lose_sign.frame_counter = 0
                        lose_sign.moving = True
                        player_fighter.sprite_state = 0
                        player_fighter.frame_counter = 0
                if self.sprite_state + 1 >= self.n_sprites:
                    self.fired = False
                    self.sprite_state = 0
        else:
            self.die()
class PlayerFighter(Fighter):
    def check_fire(self):
        if self.fired == False:
            if enemy_fighter.dead == False:
                current_keys = pygame.key.get_pressed()
                if current_keys[pygame.K_SPACE]:
                    self.fired = True
                    self.trigger_frame = self.frame_counter
    def update(self):
        if self.dead == False:
            self.frame_counter += 1
            if self.fired == True:
                if (self.frame_counter - self.trigger_frame) % self.sprite_delay == 0:
                    self.sprite_state += 1
                if self.sprite_state == self.fire_frame:
                    pygame.mixer.Sound.play(gunshot_sound)
                    if enemy_fighter.fired == True:
                        enemy_fighter.dead = True
                        win_sign.rect.topleft = win_sign.pos2
                        win_sign.direction = 1
                        win_sign.frame_counter = 0
                        win_sign.moving = True
                        enemy_fighter.sprite_state = 0
                        enemy_fighter.frame_counter = 0
                    else:
                        self.dead = True
                        lose_sign.rect.topleft = lose_sign.pos2
                        lose_sign.direction = 1
                        lose_sign.frame_counter = 0
                        lose_sign.moving = True
                if self.sprite_state + 1 >= self.n_sprites:
                    self.fired = False
                    self.sprite_state = 0
        else:
            self.die()
class CloudLayer:
    def __init__(self, speed, cloud_image, start):
        self.speed = speed
        self.cloud_image = cloud_image
        self.x = start
        self.y = random.randint(10, 500)
    def update(self):
        self.x += self.speed
        if self.x >= screen.get_width():
            self.x = -1 * self.cloud_image.get_width()
    def draw(self):
        screen.blit(self.cloud_image, (self.x, self.y))
class ButtonHint:
    def __init__(self, image, rect):
        self.image = image
        self.rect = rect
        self.frame_counter = 0
        self.sprite_state = 0
    def draw(self):
        self.sprite_rect = pygame.Rect(
            (self.sprite_state * (self.image.get_width() / 2), 0),
            (self.image.get_width() / 2, self.image.get_height())
            )
        screen.blit(self.image, self.rect, self.sprite_rect)
    def update(self):
        if self.frame_counter % 5 == 0:
            if self.sprite_state == 0:
                self.sprite_state = 1
            elif self.sprite_state == 1:
                self.sprite_state = 0
        self.frame_counter += 1
class Sign:
    def __init__(self, rect, image, pos1, pos2, frames):
        self.image = image
        self.pos1 = pos1
        self.pos2 = pos2
        self.frames = frames
        x_diff = self.pos2[0] - self.pos1[0]
        y_diff = self.pos2[1] - self.pos1[1]
        self.step = [x_diff / self.frames, y_diff / self.frames]
        self.frame_counter = 0
        self.direction = 2
        self.moving = False
        self.rect = rect
    def transition(self):
        if self.moving == True:
            if self.direction == 2:
                self.rect.move_ip(self.step)
            elif self.direction == 1:
                self.rect.move_ip(self.step[0] * -1, self.step[1] * -1)
            self.frame_counter += 1
            if self.frame_counter == self.frames:
                self.moving = False
    def draw(self):
        screen.blit(self.image, self.rect)
title_sign_rect = pygame.Rect(
    (screen.get_width() / 2 - title_image.get_width() / 2, 0),
    (title_image.get_width(), title_image.get_height())
    )
title_sign = Sign(title_sign_rect, title_image, [screen.get_width() / 2 - title_image.get_width() / 2, 0], [screen.get_width() / 2 - title_image.get_width() / 2, -1 * title_image.get_height()], 20)
win_sign_rect = pygame.Rect(
    [screen.get_width() / 2 - win_screen.get_width() / 2, -1 * win_screen.get_height()],
    (win_screen.get_width(), win_screen.get_height())
    )
win_sign = Sign(win_sign_rect, win_screen, [screen.get_width() / 2 - win_screen.get_width() / 2, 0], [screen.get_width() / 2 - win_screen.get_width() / 2, -1 * win_screen.get_height()], 20)
win_sign.direction = 1
lose_sign_rect = pygame.Rect(
    [screen.get_width() / 2 - lose_screen.get_width() / 2, -1 * lose_screen.get_height()],
    (lose_screen.get_width(), lose_screen.get_height())
    )
lose_sign = Sign(lose_sign_rect, lose_screen, [screen.get_width() / 2 - lose_screen.get_width() / 2, 0], [screen.get_width() / 2 - lose_screen.get_width() / 2, -1 * lose_screen.get_height()], 20)
lose_sign.direction = 1
cloud1 = CloudLayer(random.randint(1, 5), cloud1_image, random.randint(0, screen.get_width()))
cloud2 = CloudLayer(random.randint(1, 5), cloud2_image, random.randint(0, screen.get_width()))
cloud3 = CloudLayer(random.randint(1, 5), cloud3_image, random.randint(0, screen.get_width()))
cloud_layers.append(cloud1)
cloud_layers.append(cloud2)
cloud_layers.append(cloud3)
enemy_fighter_rect = pygame.Rect(((screen.get_width() - 500) - player_sprite.get_width() / 2, 500), (enemy_sprite.get_width(), enemy_sprite.get_height()))
enemy_fighter = EnemyFighter(enemy_sprite, enemy_fighter_rect, 7, 3, "vertical", 3, enemy_death, 7)
enemy_fighter.setup_round()
player_fighter_rect = pygame.Rect((500 - player_sprite.get_width() / 2, 500), (player_sprite.get_width(), player_sprite.get_height()))
player_fighter = PlayerFighter(player_sprite, player_fighter_rect, 7, 1, "vertical", 3, player_death, 7)
return_rect = pygame.Rect(
    (screen.get_width() / 2 - return_hint_image.get_width() / 4, screen.get_height() - return_hint_image.get_height() - 50),
    (return_hint_image.get_width(), return_hint_image.get_height())
    )
return_button_hint = ButtonHint(return_hint_image, return_rect)
space_rect = pygame.Rect(
    (player_fighter.rect.centerx - space_hint_image.get_width() / 4, player_fighter.rect.y - space_hint_image.get_height()),
    (space_hint_image.get_width(), space_hint_image.get_height())
    )
space_button_hint = ButtonHint(space_hint_image, space_rect)
def update():
    global game_state
    if game_state == 0:
        return_button_hint.update()
        current_keys = pygame.key.get_pressed()
        if current_keys[pygame.K_RETURN]:
            title_sign.moving = True
            game_state = 1
    if game_state == 1:
        enemy_fighter.check_fire()
        enemy_fighter.update()
        player_fighter.check_fire()
        player_fighter.update()
        title_sign.transition()
        win_sign.transition()
        lose_sign.transition()
        if enemy_fighter.fired == True and enemy_fighter.dead == False:
            space_button_hint.update()
        if player_fighter.finished == True or enemy_fighter.finished == True:
            return_button_hint.update()
            current_keys = pygame.key.get_pressed()
            if current_keys[pygame.K_RETURN]:
                if win_sign.frame_counter == win_sign.frames:
                    win_sign.rect.topleft = win_sign.pos1
                    win_sign.direction = 2
                    win_sign.frame_counter = 0
                    win_sign.moving = True
                if lose_sign.frame_counter == lose_sign.frames:
                    lose_sign.rect.topleft = lose_sign.pos1
                    lose_sign.direction = 2
                    lose_sign.frame_counter = 0
                    lose_sign.moving = True
                player_fighter.dead = False
                player_fighter.finished = False
                player_fighter.sprite_state = 0
                player_fighter.frame_counter = 0
                player_fighter.fired = 0
                enemy_fighter.dead = False
                enemy_fighter.finished = False
                enemy_fighter.sprite_state = 0
                enemy_fighter.frame_counter = 0
                enemy_fighter.fired = 0
                enemy_fighter.start_anim_frame = random.randint(20, 500)
    for current_cloud_layer in cloud_layers:
        current_cloud_layer.update()
def draw():
    global game_state
    if game_state == 0:
        screen.blit(sun_image, (0, 0))
        for current_cloud_layer in cloud_layers:
            current_cloud_layer.draw()
        screen.blit(environment_image, (0, 0))
        title_sign.draw()
        enemy_fighter.draw()
        player_fighter.draw()
        return_button_hint.draw()
    if game_state == 1:
        screen.blit(sun_image, (0, 0))
        for current_cloud_layer in cloud_layers:
            current_cloud_layer.draw()
        screen.blit(environment_image, (0, 0))
        title_sign.draw()
        enemy_fighter.draw()
        player_fighter.draw()
        if enemy_fighter.fired == True and enemy_fighter.dead == False:
            space_button_hint.draw()
        if player_fighter.finished == True or enemy_fighter.finished == True:
            return_button_hint.draw()
        win_sign.draw()
        lose_sign.draw()
pygame.mixer.music.play(-1)
while True:
    clear_stack()
    check_exit()
    update()
    draw()
    pygame.display.flip()
    clock.tick(20)