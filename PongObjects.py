#!/usr/bin/env python3

import pygame
import numpy

##object class definitions
class Ball:

    total_balls = 0
    active_balls = 0
    __paddle_hits = 0

    cheats_on = False
    hard_core = False

    seed_initialized = False
    seed = 0
   
    default_color = pygame.Color("white")
    default_radius = 20
    default_velocity = 200
    default_mass = 1
    
    def __init__(self, screen, border, x=None, y=None, r=default_radius, v=default_velocity, angle=None, color=default_color, mass=default_mass):
        if (x is None):
            x = screen.get_width()/2
        if (y is None):
            y = screen.get_height()/2
        if (angle is None):
            if (not Ball.seed_initialized):
                Ball.seed = numpy.random.default_rng()
                Ball.seed_initialized = True
            
            angle = Ball.seed.normal()
        
        self.__screen = screen
        self.__border = border
        self.__x = x
        self.__y = y
        self.radius = r
        self.velocity = v
        self.velocity_angle = angle
        self.color = color
        self.mass = mass
        Ball.total_balls += 1
        Ball.active_balls += 1

    def draw(self, color=None):
        if (color is None):
            color = self.color

        pygame.draw.circle(self.__screen.get_surface(), color, [int(numpy.ceil(self.__x)), int(numpy.ceil(self.__y))], self.radius)

    def get_position(self):
        return self.__x, self.__y

    def get_hits(self):
        return self.__paddle_hits

    def update(self, paddle, t=1, wall_sound=None, paddle_sound=None):
        screen_width, screen_height = self.__screen.get_size()
        zero_width, zero_height = self.__screen.get_arena_start()
        
        dx = self.velocity*numpy.cos(self.velocity_angle)*t
        dy = self.velocity*numpy.sin(self.velocity_angle)*t
        
        new_x = self.__x + dx
        new_y = self.__y + dy

        if (new_x <= (zero_width + self.__border.width + self.radius)):
            if (wall_sound is not None):
                wall_sound.play()
            self.velocity_angle = numpy.pi - self.velocity_angle
            dx = -dx
        elif (new_y <= (zero_height + self.__border.width + self.radius) or new_y >= (zero_height + screen_height - self.__border.width - self.radius)):
            if (wall_sound is not None):
                wall_sound.play()
            self.velocity_angle = -self.velocity_angle
            dy = -dy
        else:
            y_relative = self.__y - self.__border.width
            new_y_relative = new_y - self.__border.width
            paddle_y = zero_height + paddle.get_y()

            x_relative = self.__x - self.__border.width
            new_x_relative = new_x - self.__border.width
            paddle_x = zero_width + paddle.get_x()

            was_within_paddle_height = (y_relative + self.radius) >= paddle_y and (y_relative - self.radius) <= (paddle_y + paddle.length)
            was_within_paddle_width = (x_relative + self.radius) >= paddle_x  and (x_relative - self.radius) <= (paddle_x + paddle.width)
            is_within_paddle_height = (new_y_relative + self.radius) >= paddle_y and (new_y_relative - self.radius) <= (paddle_y + paddle.length)
            is_within_paddle_width = (new_x_relative + self.radius) >= paddle_x  and (new_x_relative - self.radius) <= (paddle_x + paddle.width)

            vertical_hit = not was_within_paddle_height and was_within_paddle_width
            horizontal_hit = was_within_paddle_height and not was_within_paddle_width

            if (is_within_paddle_height and is_within_paddle_width):
                if (paddle_sound is not None):
                    paddle_sound.play()
                if (self.hard_core):
                    #might be more realistic
                    v_y = (self.mass*self.velocity*numpy.sin(self.velocity_angle) + paddle.mass*paddle.velocity_y)/self.mass
                    v_x = (self.mass*self.velocity*numpy.cos(self.velocity_angle) + paddle.mass*paddle.velocity_x)/self.mass
                    self.velocity = numpy.sqrt(numpy.power(v_x, 2) + numpy.power(v_y, 2))
                    self.velocity_angle = numpy.arctan2(v_y, v_x)
                    if (horizontal_hit):
                        self.velocity_angle = numpy.pi - self.velocity_angle
                        dx = -dx
                    if (vertical_hit):
                        self.velocity_angle = -self.velocity_angle
                        dy = -dy
                else:
                    #dumb solution
                    if (horizontal_hit):
                        self.velocity_angle = numpy.pi - self.velocity_angle + paddle.velocity_y*numpy.cos(self.velocity_angle)
                        dx = -dx
                    if (vertical_hit):
                        self.velocity_angle = -self.velocity_angle
                        dy = -dy

                if ((new_x_relative + dx + self.radius) <= paddle_x):
                    Ball.__paddle_hits += 1
                if ((new_x_relative + dx - self.radius) >= (paddle_x + paddle.width)):
                    Ball.__paddle_hits -= 1

            elif(self.cheats_on and new_x >= (zero_width + screen_width - self.__border.width - self.radius)):
                if (paddle_sound is not None):
                    paddle_sound.play()
                if (self.hard_core):
                    #might be more realistic
                    if ((new_y_relative + self.radius) >= paddle_y and (new_y_relative - self.radius) <= (paddle_y + paddle.length)):
                        v_y = (self.mass*self.velocity*numpy.sin(self.velocity_angle) + paddle.mass*paddle.velocity_y)/self.mass
                        v_x = (self.mass*self.velocity*numpy.cos(self.velocity_angle) + paddle.mass*paddle.velocity_x)/self.mass
                        self.velocity = numpy.sqrt(numpy.power(v_x, 2) + numpy.power(v_y, 2))
                        self.velocity_angle = numpy.arctan2(v_y, v_x)
                    self.velocity_angle = numpy.pi - self.velocity_angle
                    dx = -dx
                else:
                    #dumb solution
                    if ((new_y_relative + self.radius) >= paddle_y and (new_y_relative - self.radius) <= (paddle_y + paddle.length)):
                        self.velocity_angle = numpy.pi - self.velocity_angle + paddle.velocity_y*numpy.cos(self.velocity_angle)
                    else:
                        self.velocity_angle = numpy.pi - self.velocity_angle
                    dx = -dx

            self.draw(self.__screen.color)
            self.__x += dx
            self.__y += dy
            self.draw()

    def toggle_cheats(self):
        Ball.cheats_on = not Ball.cheats_on
        return self.cheats_on

    def toggle_mode(self):
        Ball.hard_core = not Ball.hard_core
        return self.hard_core

    def __del__(self):
        Ball.active_balls -= 1


class Paddle:

    total_paddles = 0
    active_paddles = 0

    default_color = pygame.Color("white")
    default_width = 20
    default_length_factor = 0.3
    default_mass = 1

    def __init__(self, screen, border, y=0, width=default_width, length_factor=default_length_factor, color=default_color, mass=default_mass):
        self.__screen = screen
        self.__border = border
        self.__y = y
        self.__x = screen.get_arena_start()[0] + screen.get_width() - width - border.width
        self.width = width
        self.length_factor = length_factor
        self.length = round((screen.get_height() - 2*border.width)*length_factor)
        self.color = color
        self.velocity_y = 0
        self.velocity_x = 0
        self.mass = mass
        Paddle.total_paddles += 1
        Paddle.active_paddles += 1
    
    def draw(self, color=None):
        if (color is None):
            color = self.color

        screen_width, screen_height = self.__screen.get_size()
        zero_width, zero_height = self.__screen.get_arena_start()

        paddle_rect = pygame.Rect(zero_width + screen_width - self.width, zero_height + self.__border.width + self.__y, self.width, self.length)

        pygame.draw.rect(self.__screen.get_surface(), color, paddle_rect)

    def get_y(self):
        return self.__y

    def get_x(self):
        return self.__x

    def update(self, t=1):
        if (t == 0):
            t = 1

        zero_width, zero_height = self.__screen.get_arena_start()
        new_y = pygame.mouse.get_pos()[1]
        new_y = new_y - self.__border.width - self.length/2 - zero_height

        if (new_y > (self.__screen.get_height() - 2*self.__border.width - self.length)):
            new_y = self.__screen.get_height() - 2*self.__border.width - self.length
        if (new_y < 0):
            new_y = 0

        self.velocity_y = (new_y - self.__y)/t
        self.velocity_x = 0
        
        self.draw_2D(self.__screen.color)
        self.draw(self.__screen.color)
        self.__y = new_y
        self.__x = self.__screen.get_width() - self.width - self.__border.width
        self.draw()

    def update_ai(self, new_y):
        if (t == 0):
            t = 1

        zero_width, zero_height = self.__screen.get_arena_start()
        new_y = new_y - self.__border.width - self.length/2 - zero_height

        if (new_y > (self.__screen.get_height() - 2*self.__border.width - self.length)):
            new_y = self.__screen.get_height() - 2*self.__border.width - self.length
        if (new_y < 0):
            new_y = 0

        self.velocity_y = (new_y - self.__y)/t
        self.velocity_x = 0
        
        self.draw_2D(self.__screen.color)
        self.draw(self.__screen.color)
        self.__y = new_y
        self.__x = self.__screen.get_width() - self.width - self.__border.width
        self.draw()

    def draw_2D(self, color=None):
        if (color is None):
            color = self.color

        screen_width, screen_height = self.__screen.get_size()
        zero_width, zero_height = self.__screen.get_arena_start()

        paddle_rect = pygame.Rect(zero_width + self.__border.width + self.__x, zero_height + self.__border.width + self.__y, self.width, self.length)

        pygame.draw.rect(self.__screen.get_surface(), color, paddle_rect)
        
    def update_2D(self, t=1):
        if (t == 0):
            t = 1

        zero_width, zero_height = self.__screen.get_arena_start()
        new_x, new_y = pygame.mouse.get_pos()
        new_y = new_y - self.__border.width - self.length/2 - zero_height
        new_x = new_x - self.__border.width - self.width/2 - zero_width

        if (new_y > (self.__screen.get_height() - 2*self.__border.width - self.length)):
            new_y = self.__screen.get_height() - 2*self.__border.width - self.length
        if (new_y < 0):
            new_y = 0
        if (new_x > (self.__screen.get_width() - self.__border.width - self.width)):
            new_x = self.__screen.get_width() - self.__border.width - self.width
        if (new_x < 0):
            new_x = 0

        self.velocity_y = (new_y - self.__y)/t
        self.velocity_x = (new_x - self.__x)/t
        
        self.draw(self.__screen.color)
        self.draw_2D(self.__screen.color)
        self.__y = new_y
        self.__x = new_x
        self.draw_2D()

    def __del__(self):
        Paddle.active_paddles -= 1


class Border:

    total_borders = 0
    active_borders = 0

    default_width = 20
    default_color = pygame.Color("white")
    
    def __init__(self, screen, width=default_width, color=default_color):
        self.__screen = screen
        self.width = width
        self.color = color
        Border.total_borders += 1
        Border.active_borders += 1

    def draw(self, color=None):
        if (color is None):
            color = self.color

        zero_width, zero_height = self.__screen.get_arena_start()

        top_wall = pygame.Rect(zero_width, zero_height, self.__screen.get_width(), self.width)
        bottom_wall = pygame.Rect(zero_width, zero_height + self.__screen.get_height() - self.width, self.__screen.get_width(), self.width)
        left_wall = pygame.Rect(zero_width, zero_height + self.width, self.width, self.__screen.get_height() - 2*self.width)

        pygame.draw.rect(self.__screen.get_surface(), color, top_wall)
        pygame.draw.rect(self.__screen.get_surface(), color, bottom_wall)
        pygame.draw.rect(self.__screen.get_surface(), color, left_wall)

    def __del__(self):
        Border.active_borders -= 1


class Screen:

    total_screens = 0
    active_screens = 0

    modules_initialized = False

    default_width = 800
    default_height = 600
    default_color = pygame.Color("black")
    default_pixel_size = 0.000274

    default_stats_area = (0, 0, 0, 0)

    def __init__(self, width=default_width, height=default_height, color=default_color, stats_area=default_stats_area, pixel=default_pixel_size):
        if (not Screen.modules_initialized):
            pygame.init()
            Screen.modules_initialized = True

        self.__screen = pygame.display.set_mode(size=(width, height), flags=pygame.RESIZABLE)
        self.__stats_area = stats_area
        self.__arena_start = (stats_area[0], stats_area[1])
        self.color = color
        self.pixel = pixel
        Screen.total_screens += 1
        Screen.active_screens += 1

        self.__screen.fill(color)

    def get_width(self):
        return (self.__screen.get_width() - self.__stats_area[0] - self.__stats_area[2])

    def get_height(self):
        return (self.__screen.get_height() - self.__stats_area[1] - self.__stats_area[3])

    def get_size(self):
        width, height = self.__screen.get_size()
        return (width - self.__stats_area[0] - self.__stats_area[2], height - self.__stats_area[1] - self.__stats_area[3])

    def get_surface(self):
        return self.__screen

    def get_arena_start(self):
        return self.__arena_start

    def __del__(self):
        Screen.active_screens -= 1


class Text:
    
    total_texts = 0
    active_texts = 0

    fonts_initialized = False

    default_color = pygame.Color("white")
    default_font = "arial"
    default_font_size = 15

    def __init__(self, screen, x=0, y=0, content="", color=default_color, font=default_font, font_size=default_font_size):
        if (not Text.fonts_initialized):
            pygame.font.init()
            Text.fonts_initialized = True
        
        self.__screen = screen
        self.__x = x
        self.__y = y
        self.__content = content
        self.color = color
        self.font = pygame.font.SysFont(font, font_size)
        self.size = self.font.size(content)
        Text.total_texts += 1
        Text.active_texts += 1

    def update(self, new_content):
        self.__content = new_content
        self.size = self.font.size(self.__content)

    def draw(self, x=None, y=None):
        if (x is not None):
            self.__x = x
        if (y is not None):
            self.__y = y

        content_area = pygame.Rect(self.__x, self.__y, self.size[0], self.size[1])
        pygame.draw.rect(self.__screen.get_surface(), self.__screen.color, content_area)
        textsurface = self.font.render(self.__content, True, self.color)
        self.__screen.get_surface().blit(textsurface, (self.__x, self.__y))

    def clear(self):
        content_area = pygame.Rect(self.__x, self.__y, self.size[0], self.size[1])
        pygame.draw.rect(self.__screen.get_surface(), self.__screen.color, content_area)

    def __del__(self):
        Text.active_texts -= 1


class Sound:

    total_sounds = 0
    active_sounds = 0

    initialized = False

    default_volume = 1.0
    default_buffer_size = 512
    default_channels = 1


    def __init__(self, sound_file, volume=default_volume, channel_number=default_channels, buffer_size=default_buffer_size):
        if (not Sound.initialized):
            pygame.mixer.init(channels=channel_number, buffer=buffer_size)
            Sound.initialized = True

        self.file = sound_file
        self.volume = volume

        self.sound = pygame.mixer.Sound(sound_file)
        self.sound.set_volume(volume)

    def play(self):
        channel = pygame.mixer.find_channel(True)
        #channel.set_volume(self.volume)
        channel.play(self.sound)

    def __del__(self):
        Sound.active_sounds -= 1