# --- DPI Awareness for Windows (for correct scaling with display settings) ---
import sys
if sys.platform == "win32":
    import ctypes
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

import pygame
import copy
import start
from gamestate import *
from mob import *
from reward import show_reward_screen
from moviepy.editor import VideoFileClip
from sounds import *


class DropBox:
    def __init__(self, rect):
        self.rect = rect

    def is_inside(self, pos):
        return self.rect.collidepoint(pos)

class Adventurer(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet, display_width, display_height):
        super().__init__()
        self.display_width = display_width
        self.display_height = display_height
        # Use relative positioning and sizing
        self.sprite_idle_width = int(display_width * 0.104)
        self.sprite_idle_height = int(display_height * 0.23)
        self.sprite_attack_width = int(display_width * 0.21)
        self.sprite_attack_height = int(display_height * 0.3)
        self.sprite_shield_width = int(display_width * 0.195)
        self.sprite_shield_height = int(display_height * 0.23)
        self.sprite_run_width = int(display_width * 0.156)
        self.sprite_run_height = int(display_height * 0.23)
        self.death_sprite_width = int(display_width * 0.145)
        self.death_sprite_height = int(display_height * 0.24)
        self.animation_finished = False
        self.idle_num_frames = 6
        self.attack_num_frames = 8
        self.shield_num_frames = 9
        self.run_num_frames = 8
        self.death_num_frames = 14
        self.current_frame = 0
        self.idle_sprites = [sprite_sheet.subsurface((i * self.sprite_idle_width, 0, self.sprite_idle_width, self.sprite_idle_height)) for i in range(self.idle_num_frames)]
        self.attack_sprites = []
        self.shield_sprites = []
        self.run_sprites = []
        self.death_sprites = []
        self.sprites = self.idle_sprites
        self.animation_state = "Idle"
        self.animation_loop_count = 0
        self.animation_frame_count = 0
        self.image = self.sprites[0]
        self.rect = self.image.get_rect()
        # Relative position: 30% from left, 50% from top
        self.rect.topleft = (int(display_width * 0.30), int(display_height * 0.35))
        self.original_sprites = self.sprites[:]
        self.max_health = 50
        self.current_health = 50
        self.health_bar_length = int(display_width * 0.062)
        self.health_bar_height = int(display_height * 0.01)
        custom_font = "Scripts/PressStart2P-Regular.ttf"
        font_size = int(min(display_width, display_height) * 0.014)
        self.font = pygame.font.Font(custom_font, font_size)

    def update_animation(self):
        if self.animation_state == "Idle":
            self.current_frame = (self.current_frame + 1) % self.idle_num_frames
            self.image = self.idle_sprites[self.current_frame]
            self.rect.topleft = (int(self.display_width * 0.30), int(self.display_height * 0.35))
        elif self.animation_state == "Attack":
            if self.animation_frame_count < self.attack_num_frames:
                self.current_frame = (self.animation_frame_count) % self.attack_num_frames
                self.image = self.attack_sprites[self.current_frame]
                self.animation_frame_count += 1
            else:
                self.reset_animation()
        elif self.animation_state == "Shield":
            if self.animation_frame_count < self.shield_num_frames:
                self.current_frame = (self.animation_frame_count) % self.shield_num_frames
                self.image = self.shield_sprites[self.current_frame]
                self.animation_frame_count += 1
            else:
                self.reset_animation()
        elif self.animation_state == "Run":
            self.image = self.run_sprites[self.current_frame]
            self.animation_frame_count += 1
            self.rect.x += int(self.display_width * 0.018)
            self.current_frame = (self.current_frame + 1) % self.run_num_frames
            self.image = self.run_sprites[self.current_frame]
        elif self.animation_state == "Death":
            if self.animation_frame_count < self.death_num_frames:
                self.current_frame = (self.animation_frame_count) % self.death_num_frames
                self.image = self.death_sprites[self.current_frame]
                self.animation_frame_count += 1
            else:
                pygame.time.delay(200)
                self.animation_finished = "True"
                
    def attack_animation(self):
        self.animation_frame_count = 0
        new_sprite_sheet = pygame.image.load('Sprites/attack_test.png')
        new_sprite_sheet = pygame.transform.scale(new_sprite_sheet, (self.sprite_attack_width * self.attack_num_frames, self.sprite_attack_height))
        self.rect.topleft = (int(self.display_width * 0.3), int(self.display_height * 0.35))
        self.attack_sprites = [new_sprite_sheet.subsurface((i * self.sprite_attack_width, 0, self.sprite_attack_width, self.sprite_attack_height)) for i in range(self.attack_num_frames)]
        self.sprites = self.attack_sprites
        self.animation_state = "Attack"

    def shield_animation(self):
        self.animation_frame_count = 0
        new_sprite_sheet = pygame.image.load('Sprites/shield_test.png')
        new_sprite_sheet = pygame.transform.scale(new_sprite_sheet, (self.sprite_shield_width * self.shield_num_frames, self.sprite_shield_height))
        self.rect.topleft = (int(self.display_width * 0.3), int(self.display_height * 0.35))
        self.shield_sprites = [new_sprite_sheet.subsurface((i * self.sprite_shield_width, 0, self.sprite_shield_width, self.sprite_shield_height)) for i in range(self.shield_num_frames)]
        self.sprites = self.shield_sprites
        self.animation_state = "Shield"

    def reset_animation(self):
        self.animation_frame_count = 0
        self.animation_state = "Idle"
        self.sprites = self.idle_sprites

    def run_animation(self):
        self.animation_frame_count = 0
        new_sprite_sheet = pygame.image.load('Sprites/run.png')
        new_sprite_sheet = pygame.transform.scale(new_sprite_sheet, (self.sprite_run_width * self.run_num_frames, self.sprite_run_height))
        self.rect.topleft = (int(self.display_width * 0.3), int(self.display_height * 0.35))
        self.run_sprites = [new_sprite_sheet.subsurface((i * self.sprite_run_width, 0, self.sprite_run_width, self.sprite_run_height)) for i in range(self.run_num_frames)]
        self.sprites = self.run_sprites
        self.animation_state = "Run"

    def death_animation(self):
        self.animation_frame_count = 0
        new_sprite_sheet = pygame.image.load('Sprites/death.png')
        new_sprite_sheet = pygame.transform.scale(new_sprite_sheet, (self.death_sprite_width * self.death_num_frames, self.death_sprite_height))
        self.rect.topleft = (int(self.display_width * 0.3), int(self.display_height * 0.35))
        self.death_sprites = [new_sprite_sheet.subsurface((i * self.death_sprite_width, 0, self.death_sprite_width, self.death_sprite_height)) for i in range(self.death_num_frames)]
        self.sprites = self.death_sprites  
        self.animation_state = "Death"
    
    def draw_health_bar(self, surface):
        if self.animation_state == "Run" or self.animation_state == "Death":
            return
    
        # Calculate health ratio
        health_ratio = self.current_health / self.max_health
        # Ensure health ratio does not exceed 1 (maximum value)
        health_ratio = min(health_ratio, 1.0)
        # Calculate current health length
        current_health_length = int(self.health_bar_length * health_ratio)
        
        # Draw the health bar background
        bar_x = self.rect.x
        bar_y = self.rect.y - int(self.display_height * 0.04)
        pygame.draw.rect(surface, RED, (bar_x, bar_y, self.health_bar_length, self.health_bar_height))
        # Draw the current health
        pygame.draw.rect(surface, GREEN, (bar_x, bar_y, current_health_length, self.health_bar_height))
        
        # Render health text
        health_text = f"{self.current_health}/{self.max_health} HP"
        health_surface = self.font.render(health_text, True, WHITE)
        surface.blit(health_surface, (bar_x, bar_y - int(self.display_height * 0.025)))

class EnergyBar:
    def __init__(self, position, max_energy, current_energy, image_path, font):
        self.position = position
        self.max_energy = max_energy
        self.current_energy = current_energy
        self.image = pygame.image.load(image_path)
        self.font = font

    def draw(self, surface):
        # Draw the energy bar image
        surface.blit(self.image, self.position)

        # Draw the text over the energy bar
        energy_text = f"{self.current_energy}/{self.max_energy}"
        energy_text_surface = self.font.render(energy_text, True, WHITE)

        # Center the text over the energy bar
        text_x = self.position[0] + (self.image.get_width() - energy_text_surface.get_width()) // 2
        text_y = self.position[1] + (self.image.get_height() - energy_text_surface.get_height()) // 2
        surface.blit(energy_text_surface, (text_x, text_y))

    def update_energy(self, value):
        self.current_energy += value
        self.current_energy = max(0, min(self.current_energy, self.max_energy))  # Clamp energy within range 0 to max_energy

class EndTurnButton:
    def __init__(self, rect, font_path, font_size):
        self.rect = rect
        self.font = pygame.font.Font(font_path, font_size)
        self.color = RED
        self.text = "End Turn"

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        button_text = self.font.render(self.text, True, WHITE)
        button_rect = button_text.get_rect(center=self.rect.center)
        screen.blit(button_text, button_rect)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)

def display_floor_number(screen, floor_number, scale_x, scale_y, display_width, display_height):
    screen.fill(BLACK)
    custom_font = "Scripts/PressStart2P-Regular.ttf"
    font = pygame.font.Font(custom_font, int(80 * min(scale_x, scale_y)))
    text = f"Floor {floor_number}"
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(display_width // 2, display_height // 2))
    screen.blit(text_surface, text_rect)
    pygame.display.update()
    pygame.time.delay(1000)
    fade_to_black(screen)

def reset_mobs():
    global mobs_by_floor
    mobs_by_floor = {floor: [copy.copy(mob) for mob in mobs] for floor, mobs in original_mobs_by_floor.items()}

def play_video(video_path):
    clip = VideoFileClip(video_path)
    clip.preview()

def main_game(floor_number):
    pygame.init()

    # Get the current screen dimensions
    info = pygame.display.Info()
    display_width = info.current_w
    display_height = info.current_h

    # Calculate scaling factors based on reference resolution (1920x1080)
    scale_x = display_width / 1920
    scale_y = display_height / 1080

    # Create a screen that matches the current display size
    screen = pygame.display.set_mode((display_width, display_height), pygame.FULLSCREEN)
    pygame.display.set_caption('Dungeon Descent')

    # Initialize the mixer module
    bg_music.play(-1)

    display_floor_number(screen, floor_number, scale_x, scale_y, display_width, display_height)

    # Load and scale background image
    background_image = pygame.image.load('Sprites/main-bg.png').convert()
    background_image = pygame.transform.scale(background_image, (display_width, display_height))
    screen.blit(background_image, (0, 0))

    # Load and scale energy bar image
    energy_bar_image = pygame.image.load('Sprites/energy.png')
    energy_bar_image = pygame.transform.scale(energy_bar_image, 
        (int(energy_bar_image.get_width() * scale_x), 
         int(energy_bar_image.get_height() * scale_y)))

    custom_font = "Scripts/PressStart2P-Regular.ttf"
    font = pygame.font.Font(custom_font, int(46 * min(scale_x, scale_y)))

    adventurer_sprite_sheet = pygame.image.load('Sprites/idle.png')

    adventurer = Adventurer(adventurer_sprite_sheet, display_width, display_height)

    energy_bar = EnergyBar(
        (int(80 * scale_x), int(display_height - energy_bar_image.get_height())), 
        3, 3, 'Sprites/energy.png', font)

    all_sprites = pygame.sprite.Group()
    
    # Scale dropbox dimensions
    dropbox_rect = pygame.Rect(
        int(50 * scale_x), 
        int(50 * scale_y), 
        int(1820 * scale_x), 
        int(500 * scale_y))
    dropbox = DropBox(dropbox_rect)

    for mob in mobs_by_floor[floor_number]:
        all_sprites.add(mob)

    cards = []

    debug_font = pygame.font.Font("Scripts/PressStart2P-Regular.ttf", int(45 * min(scale_x, scale_y)))

    game_state = GameState(cards, dropbox, adventurer, mobs_by_floor[floor_number], debug_font, energy_bar, all_sprites)
    game_state.refill_cards()
    
    # Scale end turn button
    end_turn_button = EndTurnButton(
        pygame.Rect(
            int(1670 * scale_x), 
            int(1000 * scale_y), 
            int(180 * scale_x), 
            int(50 * scale_y)), 
        custom_font, 
        int(20 * min(scale_x, scale_y)))

    clock = pygame.time.Clock()

    # Scale retry button
    retry_button_rect = pygame.Rect(
        int((display_width // 2 - 100) * scale_x), 
        int((display_height // 2 - 25) * scale_y), 
        int(200 * scale_x), 
        int(50 * scale_y))
    retry_font = pygame.font.Font(custom_font, int(30 * min(scale_x, scale_y)))
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if end_turn_button.is_clicked(event):
                game_state.end_adventurer_turn()
            game_state.handle_event(event, screen)  # Pass screen to handle_event

            if game_state.turn == "Adventurer" and adventurer.animation_state == "Idle" and not game_state.mobs:
                adventurer.run_animation()  # Move this line inside the condition

            if game_state.game_over:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if retry_button_rect.collidepoint(event.pos):
                        mobs_by_floor.update({floor: [copy.copy(mob) for mob in mobs] for floor, mobs in original_mobs_by_floor.items()})
                        start.main_menu()
                        reset_mobs()

        if adventurer.rect.x >= display_width - 120 and adventurer.animation_state == "Run":
            pygame.mixer.music.fadeout(1000)  # Fade out the music over 1 second
            fade_to_black(screen)
            if floor_number == 10:
                play_video("Video/end_scene.mp4")  # Replace with your video path
                pygame.quit()
                sys.exit()
            show_reward_screen(floor_number, card_types, game_state)
            pygame.time.delay(300)
            floor_number += 1
            main_game(floor_number)

        adventurer.update_animation()
        all_sprites.update()

        screen.fill((0, 0, 0))
        screen.blit(background_image, (0, 0))

        screen.blit(adventurer.image, adventurer.rect.topleft)

        font = pygame.font.Font(None, int(36 * min(scale_x, scale_y)))
        for mob in mobs_by_floor[floor_number]:
            mob.draw(screen, font)
            mob.draw_health_bar(screen)

        all_sprites.draw(screen)

        energy_bar.draw(screen)

        adventurer.draw_health_bar(screen)

        if game_state.state == "Info" and game_state.clicked_card:
            screen.blit(game_state.clicked_card.image, game_state.clicked_card.rect.topleft)

        game_state.draw_debug_info(screen)
        game_state.draw_message(screen)

        end_turn_button.draw(screen)

        if game_state.game_over and adventurer.animation_finished == "True":
            overlay = pygame.Surface((display_width, display_height))
            overlay.fill(RED)
            screen.blit(overlay, (0, 0))
            bg_music.stop()
            # "You Died!" text
            you_died_font = pygame.font.Font(custom_font, int(80 * min(scale_x, scale_y)))
            you_died_text = you_died_font.render("You Died!", True, WHITE)
            you_died_rect = you_died_text.get_rect(center=(display_width // 2, display_height // 2 - int(200 * scale_y)))
            screen.blit(you_died_text, you_died_rect)

            # Retry button
            retry_text = retry_font.render("Retry", True, WHITE)
            retry_rect = retry_text.get_rect(center=retry_button_rect.center)
            pygame.draw.rect(screen, BLACK, retry_button_rect)
            screen.blit(retry_text, retry_rect)

        pygame.display.update()
        clock.tick(10)

if __name__ == "__main__":
    floor_number = 1# Initial floor number
    main_game(floor_number)
