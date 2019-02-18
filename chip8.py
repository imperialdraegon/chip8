import numpy
import pygame
from time import sleep
from cpu import CPU

class Chip8:

    def __init__(self):
        self.memory = [0x00] * 4096
        self.memory_start = 0x200
        self.V = [0x00] * 16
        self.PC = self.memory_start
        self.SP = 0x00
        self.stack = [0x0000] * 16
        self.I = 0x00
        self.delay_timer = 0
        self.sound_timer = 0
        self.CPU = CPU(self)
        self.clock_speed = 1/600 #In hertz

        self.cur_key = None
        self.paused = False

        pygame.init()

        self.screen_width = 64
        self.screen_height = 32
        self.scale_factor = 10
        self.display = pygame.display.set_mode((self.screen_width * self.scale_factor, self.screen_height * self.scale_factor))
        self.screen = [[0]*self.screen_width for x in range(self.screen_height)]

        self.font_set = [
            0xF0, 0x90, 0x90, 0x90, 0xF0,
            0x20, 0x60, 0x20, 0x20, 0x70,
            0xF0, 0x10, 0xF0, 0x80, 0xF0,
            0xF0, 0x10, 0xF0, 0x10, 0xF0,  # 3
            0x90, 0x90, 0xF0, 0x10, 0x10,
            0xF0, 0x80, 0xF0, 0x10, 0xF0,
            0xF0, 0x80, 0xF0, 0x90, 0xF0,  # 6
            0xF0, 0x10, 0x20, 0x40, 0x40,
            0xF0, 0x90, 0xF0, 0x90, 0xF0,
            0xF0, 0x90, 0xF0, 0x10, 0xF0,  # 9
            0xF0, 0x90, 0xF0, 0x90, 0x90,
            0xE0, 0x90, 0xE0, 0x90, 0xE0,
            0xF0, 0x80, 0x80, 0x80, 0xF0,  # C
            0xE0, 0x90, 0x90, 0x90, 0xE0,
            0xF0, 0x80, 0xF0, 0x80, 0xF0,
            0xF0, 0x80, 0xF0, 0x80, 0x80,  # F
        ]

        self.init("../roms/TANK")

    def load_rom_to_memory(self, path):
        code = open(path, "rb").read()
        mem_counter = 0
        for x in code:
            self.memory[mem_counter + self.memory_start] = x
            mem_counter += 1

    def init(self, path):
        self.load_rom_to_memory(path)
        self.memory[0:len(self.font_set)] = self.font_set
        self.cycle()
        self.start()


    def cycle(self):
        opcode = (self.memory[self.PC] << 8) | self.memory[self.PC + 1]
        self.CPU.execute(opcode)
        self.update_screen()
        self.PC += 2

    def start(self):
        done = False
        count = 0

        while not done:
            if not self.paused:
                self.cycle()
                if count % 10 == 0:
                    self.update_timers()
            sleep(self.clock_speed)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
            pygame.display.flip()

    def clear_screen(self):
        for y in range(len(self.screen)):
            for x in range(len(self.screen[y])):
                self.screen[y][x] = 0

    def update_screen(self):
        for y in range(len(self.screen)):
            for x in range(len(self.screen[y])):
                val = self.screen[y][x]
                if val == 1:
                    pygame.draw.rect(self.display, (255, 255, 255), (x * 10, y * 10, self.scale_factor, self.scale_factor))
                elif val == 0:
                    pygame.draw.rect(self.display, (0, 0, 0), (x * 10, y * 10, self.scale_factor, self.scale_factor))

    def update_timers(self):
        if self.delay_timer > 0:
            self.delay_timer += -1
        if self.sound_timer > 0:
            self.sound_timer += -1










