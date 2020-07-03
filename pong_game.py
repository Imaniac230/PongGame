#!/usr/bin/env python3

##imports
import PongObjects as po
from PongObjects import pygame as pg
from PongObjects import numpy as np


def main():
    ##variable definitions
    class GameFlags:
        pass

    GameFlags.cheats_on = False
    GameFlags.keep_last_missed_location = False
    GameFlags.show_mouse = True
    GameFlags.hard_core = True
    GameFlags.minimum_frame_time = 0 #mili seconds
    GameFlags.fps_update_rate = 30 #frames

    game_music = "sounds/game_music.wav"
    music_volume = 0.07
    
    sound_volume = 0.05
    wall_hit_sound = "sounds/wall_hit.wav"
    paddle_hit_sound = "sounds/paddle_hit.wav"

    display_resolution_height = 1080 #pixels
    display_physical_height = 0.184 #meters
    
    window_width = 1280 #pixels
    window_height = 720 #pixels
    background_color = pg.Color("cyan")
    top_area_height = 35 #pixels
    pixel_size = display_physical_height/display_resolution_height #meters

    fps_font = "arial"
    fps_size = 15 #pixels
    fps_color = pg.Color("black")
    fps_position = (0, top_area_height//10)

    score_font = "arial"
    score_size = 20 #pixels
    score_color = pg.Color("brown")
    score_position = (window_width//3, top_area_height//10)

    velocity_font = "arial"
    velocity_size = 20 #pixels
    velocity_color = pg.Color("black")
    velocity_position = (window_width//10, top_area_height//10)

    title_font = "arial"
    title_size = 50 #pixels
    title_color = pg.Color("magenta")
    title_position = (window_width//5, window_height//4)
    title_text = "CLICK LEFT MOUSE TO START"

    gameover_font = title_font
    gameover_size = title_size #pixels
    gameover_color = title_color
    gameover_position = (window_width//30, window_height//4)
    gameover_text = "GAME OVER! CLICK LEFT MOUSE TO RESTART"

    hint_paddle_font = "arial"
    hint_paddle_size = 13 #pixels
    hint_paddle_color = pg.Color("black")
    hint_paddle_position = (window_width//2 + window_width//4, 0)
    hint_paddle_text = "Hint: Hold RIGHT mouse to unlock paddle."

    hint_ball_font = hint_paddle_font
    hint_ball_size = hint_paddle_size #pixels
    hint_ball_color = hint_paddle_color
    hint_ball_position = (hint_paddle_position[0], top_area_height//2)
    hint_ball_text = "Hint: Click MIDDLE mouse to reset ball."

    border_width = 20 #pixels
    border_color = pg.Color("red")
    
    ball_color = pg.Color("black")
    ball_radius = round(border_width*1.0)
    ball_velocity = 500 #pixels/second
    ball_mass = 100
    
    paddle_color = pg.Color("blue")
    paddle_width = round(ball_radius*1.0)
    paddle_length_factor = 0.2 #percent of arena height
    paddle_mass = ball_mass/10
    

    ##define game objects
    class GameObjects:
        pass

    GameObjects.paddle_sound = po.Sound(paddle_hit_sound, sound_volume)
    GameObjects.wall_sound = po.Sound(wall_hit_sound, sound_volume)
    
    GameObjects.screen_0 = po.Screen(window_width, window_height, background_color, stats_area=(0, top_area_height, 0, 0), pixel=pixel_size)
    GameObjects.border_0 = po.Border(GameObjects.screen_0, border_width, border_color)
    
    GameObjects.paddle_0 = po.Paddle(GameObjects.screen_0, GameObjects.border_0, width=paddle_width, length_factor=paddle_length_factor, color=paddle_color, mass=paddle_mass)
    GameObjects.ball_0 = po.Ball(GameObjects.screen_0, GameObjects.border_0, r=ball_radius, v=ball_velocity, color=ball_color, mass=ball_mass)
    
    GameObjects.title = po.Text(GameObjects.screen_0, title_position[0], title_position[1], title_text, title_color, title_font, title_size)
    GameObjects.hint_paddle = po.Text(GameObjects.screen_0, hint_paddle_position[0], hint_paddle_position[1], hint_paddle_text, hint_paddle_color, hint_paddle_font, hint_paddle_size)
    GameObjects.hint_ball = po.Text(GameObjects.screen_0, hint_ball_position[0], hint_ball_position[1], hint_ball_text, hint_ball_color, hint_ball_font, hint_ball_size)
    
    GameObjects.fps = po.Text(GameObjects.screen_0, fps_position[0], fps_position[1], color=fps_color, font=fps_font, font_size=fps_size)
    GameObjects.gameover = po.Text(GameObjects.screen_0, gameover_position[0], gameover_position[1], gameover_text, gameover_color, gameover_font, gameover_size)
    GameObjects.score = po.Text(GameObjects.screen_0, score_position[0], score_position[1], color=score_color, font=score_font, font_size=score_size)
    GameObjects.velocity = po.Text(GameObjects.screen_0, velocity_position[0], velocity_position[1], color=velocity_color, font=velocity_font, font_size=velocity_size)


    ##define objects with only their default values
    #GameObjects.paddle_sound = po.Sound(paddle_hit_sound)
    #GameObjects.wall_sound = po.Sound(wall_hit_sound)
    #
    #GameObjects.screen_0 = po.Screen()
    #GameObjects.border_0 = po.Border(GameObjects.screen_0)
    #
    #GameObjects.paddle_0 = po.Paddle(GameObjects.screen_0, GameObjects.border_0)
    #GameObjects.ball_0 = po.Ball(GameObjects.screen_0, GameObjects.border_0)
    #
    #GameObjects.title = po.Text(GameObjects.screen_0)
    #GameObjects.hint_paddle = po.Text(GameObjects.screen_0)
    #GameObjects.hint_ball = po.Text(GameObjects.screen_0)
    #
    #GameObjects.fps = po.Text(GameObjects.screen_0)
    #GameObjects.gameover = po.Text(GameObjects.screen_0)
    #GameObjects.score = po.Text(GameObjects.screen_0)
    #GameObjects.velocity = po.Text(GameObjects.screen_0)

    if (GameFlags.cheats_on):
        GameFlags.cheats_on = GameObjects.ball_0.toggle_cheats()
    if (GameFlags.hard_core):
        GameFlags.hard_core = GameObjects.ball_0.toggle_mode()
   

    ##initial screen setup    
    GameObjects.border_0.draw()
    GameObjects.ball_0.draw()
    GameObjects.paddle_0.draw()
    
    GameObjects.title.draw()
    pg.display.flip()
    GameObjects.hint_paddle.draw()
    GameObjects.hint_ball.draw()

    pg.mouse.set_visible(GameFlags.show_mouse)


    ##music setup
    pg.mixer.music.load(game_music)
    pg.mixer.music.set_volume(music_volume)
    

    ##display title screen
    if (title_screen(GameObjects)):
        return 1
   

    ##game loop
    pg.mixer.music.play(-1)
    game_loop(GameObjects, GameFlags)


def reset_ball(ball, screen, border, velocity):
    ball.draw(screen.color)
    ball = po.Ball(screen, border, r=ball.radius, v=velocity, color=ball.color, mass=ball.mass)
    ball.draw()
    return ball


def draw_stats(stats, text):
    stats.clear()
    stats.update(text)
    stats.draw()
    return stats


def title_screen(game_objects):
    while True:
        event = pg.event.poll()
        if (event.type == pg.QUIT):
            pg.quit()
            return 1
        if (pg.mouse.get_pressed()[0]):
            game_objects.title.clear()
            return 0


def game_loop(game_objects, game_flags):
    #clock = pg.time.Clock()
    ball_reset = False
    #initial loop time
    t = 1
    #initial loop count
    frame_count = 0
    #initial fps
    current_fps = 0

    initial_velocity = game_objects.ball_0.velocity

    event = pg.event.poll()
    while (event.type != pg.QUIT):
        start = pg.time.get_ticks()
        #clock.tick(300)

        #TODO: add some proper screen resize handling
        #if (event.type == pg.VIDEORESIZE):
        #    game_objects.screen_0.get_surface().blit(pg.transform.scale(game_objects.screen_0.get_surface(), event.dict['size']), (0, 0))
        #    pg.display.flip()
        #elif (event.type == pg.VIDEOEXPOSE):
        #    #game_objects.screen_0.get_surface().fill((0, 0, 0))
        #    game_objects.screen_0.get_surface().blit(pg.transform.scale(game_objects.screen_0.get_surface(), game_objects.screen_0.get_surface().get_size()), (0, 0))
        #    game_objects.ball_0.draw(game_objects.screen_0.color)
        #    game_objects.paddle_0.draw(game_objects.screen_0.color)
        #    game_objects.border_0.draw(game_objects.screen_0.color)
        #    game_objects.ball_0.draw()
        #    game_objects.paddle_0.draw()
        #    game_objects.border_0.draw()
        #    pg.display.flip()

        if (game_flags.keep_last_missed_location):
            ball_out_of_screen = game_objects.screen_0.get_arena_start()[0] + game_objects.screen_0.get_width()
        else:
            ball_out_of_screen = game_objects.screen_0.get_arena_start()[0] + game_objects.screen_0.get_width() + game_objects.ball_0.radius

        if (pg.mouse.get_pressed()[1] and not ball_reset and (game_objects.ball_0.get_position()[0] < ball_out_of_screen)):
            game_objects.ball_0 = reset_ball(game_objects.ball_0, game_objects.screen_0, game_objects.border_0, initial_velocity)
            ball_reset = True

        #ball resets only once per click
        if (ball_reset and not pg.mouse.get_pressed()[1]):
            ball_reset = False

        if (game_objects.ball_0.get_position()[0] >= ball_out_of_screen):
            game_objects.gameover.draw()
            if (pg.mouse.get_pressed()[0]):
                game_objects.gameover.clear()
                game_objects.ball_0 = reset_ball(game_objects.ball_0, game_objects.screen_0, game_objects.border_0, initial_velocity)
       
        pg.display.flip()

        if (pg.mouse.get_pressed()[2]):
            game_objects.paddle_0.update_2D(t/1000)
        else:
            game_objects.paddle_0.update(t/1000)

        #draw ball only when inside arena
        if (game_objects.ball_0.get_position()[0] < ball_out_of_screen):
            game_objects.ball_0.update(game_objects.paddle_0, t/1000, game_objects.wall_sound, game_objects.paddle_sound)

        text = "Retries: " + str(game_objects.ball_0.total_balls - 1) + " Hits: " + str(game_objects.ball_0.get_hits())
        game_objects.score = draw_stats(game_objects.score, text)

        if (game_flags.hard_core):
            text = "Ball velocity: " + str(np.around(game_objects.ball_0.velocity*game_objects.screen_0.pixel*100, 3)) + " cm/s"
            draw_stats(game_objects.velocity, text)
    
        pg.time.wait(game_flags.minimum_frame_time)

        t = pg.time.get_ticks() - start
        if (t > 0):
            frame_count += 1
            if (frame_count >= game_flags.fps_update_rate):
                frame_count = 0
                current_fps = round(1000/t)
                text = str(current_fps) + " FPS"
                game_objects.fps = draw_stats(game_objects.fps, text)

        event = pg.event.poll()
        
     
    pg.quit()
    return 0


if __name__ == "__main__":
    main()