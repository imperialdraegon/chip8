import random

class CPU:

    def __init__(self, chip8):
        self.chip8 = chip8

    def execute(self, opcode):
        nnn = opcode & 0x0FFF
        x = (opcode & 0x0F00) >> 8
        y = (opcode & 0x00F0) >> 4
        kk = opcode & 0x00FF
        first = opcode & 0xF000
        last = opcode & 0x000F
        if opcode == 0x00E0:
            self.op_00E0()
        elif opcode == 0x00EE:
            self.op_00EE()
        elif first == 0x1000:
            self.op_1XXX(nnn)
        elif first == 0x2000:
            self.op_2XXX(nnn)
        elif first == 0x3000:
            self.op_3XXX(x, kk)
        elif first == 0x4000:
            self.op_4XXX(x, kk)
        elif first == 0x5000:
            self.op_5XXX(x, y)
        elif first == 0x6000:
            self.op_6XXX(x, kk)
        elif first == 0x7000:
            self.op_7XXX(x, kk)
        elif first == 0x8000:
            if last == 0:
                self.op_8XX0(x, y)
            if last == 1:
                self.op_8XX1(x, y)
            if last == 2:
                self.op_8XX2(x, y)
            if last == 3:
                self.op_8XX3(x, y)
            if last == 4:
                self.op_8XX4(x, y)
            if last == 5:
                self.op_8XX5(x, y)
            if last == 6:
                self.op_8XX6(x, y)
            if last == 7:
                self.op_8XX7(x, y)
            if last == 0xE:
                self.op_8XXE(x, y)
        elif first == 0x9000:
            self.op_9XX0(x, y)
        elif first == 0xA000:
            self.op_AXXX(nnn)
        elif first == 0xB000:
            self.op_BXXX(nnn)
        elif first == 0xC000:
            self.op_CXXX(x, kk)
        elif first == 0xD000:
            self.op_DXXX(x, y, last)
        elif first == 0xE000:
            if kk == 0x9E:
                self.op_EX9E(x)
            if kk == 0xA1:
                self.op_EXA1(x)
        elif first == 0xF000:
            if kk == 0x07:
                self.op_FX07(x)
            if kk == 0x0A:
                self.op_FX0A(x)
            if kk == 0x15:
                self.op_FX15(x)
            if kk == 0x18:
                self.op_FX18(x)
            if kk == 0x1E:
                self.op_FX1E(x)
            if kk == 0x29:
                self.op_FX29(x)
            if kk == 0x33:
                self.op_FX33(x)
            if kk == 0x55:
                self.op_FX55(x)
            if kk == 0x65:
                self.op_FX65(x)


    def op_00E0(self):
        self.chip8.clear_screen()

    def op_00EE(self):
        self.chip8.PC = self.chip8.stack[self.chip8.SP]
        self.chip8.SP += -1

    def op_1XXX(self, nnn):
        self.chip8.PC = nnn
        self.chip8.PC += -2

    def op_2XXX(self, nnn):
        self.chip8.SP += 1
        self.chip8.stack[self.chip8.SP] = self.chip8.PC
        self.chip8.PC = nnn
        self.chip8.PC += -2

    def op_3XXX(self, x, kk):
        if self.chip8.V[x] == kk:
            self.chip8.PC += 2

    def op_4XXX(self, x, kk):
        if self.chip8.V[x] != kk:
            self.chip8.PC += 2

    def op_5XXX(self, x, y):
        if self.chip8.V[x] == self.chip8.V[y]:
            self.chip8.PC += 2

    def op_6XXX(self, x, kk):
        self.chip8.V[x] = kk

    def op_7XXX(self, x, kk):
        self.chip8.V[x] = (self.chip8.V[x] + kk) & 0xFF

    def op_8XX0(self, x, y):
        self.chip8.V[x] = self.chip8.V[y]

    def op_8XX1(self, x, y):
        self.chip8.V[x] = self.chip8.V[x] | self.chip8.V[y]

    def op_8XX2(self, x, y):
        self.chip8.V[x] = self.chip8.V[x] & self.chip8.V[y]

    def op_8XX3(self, x, y):
        self.chip8.V[x] = self.chip8.V[x] ^ self.chip8.V[y]

    def op_8XX4(self, x, y):
        sum = self.chip8.V[x] + self.chip8.V[y]
        if sum > 255:
            self.chip8.V[15] = 1
        else:
            self.chip8.V[15] = 0
        self.chip8.V[x] = sum | 0xFF

    def op_8XX5(self, x, y):
        vx = self.chip8.V[x]
        vy = self.chip8.V[y]
        if vx > vy:
            self.chip8.V[15] = 1
        else:
            self.chip8.V[15] = 0
        self.chip8.V[x] = (self.chip8.V[x] - self.chip8.V[y]) & 0xFF

    def op_8XX6(self, x, y):
        lsb = int(bin(self.chip8.V[x])[0]) & 1
        if lsb == 1:
            self.chip8.V[15] = 1
        else:
            self.chip8.V[15] = 0
        self.chip8.V[x] = self.chip8.V[x] / 2

    def op_8XX7(self, x, y):
        vx = self.chip8.V[x]
        vy = self.chip8.V[y]
        if vy > vx:
            self.chip8.V[15] = 1
        else:
            self.chip8.V[15] = 0
        self.chip8.V[x] = (self.chip8.V[y] - self.chip8.V[x]) & 0xFF

    def op_8XXE(self, x, y):
        pass

    def op_9XX0(self, x, y):
        if self.chip8.V[x] != self.chip8.V[y]:
            self.chip8.PC += 2

    def op_AXXX(self, nnn):
        self.chip8.I = nnn

    def op_BXXX(self, nnn):
        self.chip8.PC += nnn + self.chip8.V[0]

    def op_CXXX(self, x, kk):
        self.chip8.V[x] = random.randint(0x0, 0xFF) & kk

    def op_DXXX(self, x, y, n):
        x_coord = self.chip8.V[x]
        y_coord = self.chip8.V[y]
        self.chip8.V[15] = 0
        for address in range(n):
            pixel = format(self.chip8.memory[self.chip8.I + address], "08b")
            for i in range(8):
                prev = self.chip8.screen[(y_coord + address) % self.chip8.screen_height][(x_coord + i) % self.chip8.screen_width]
                if prev ^ int(pixel[i]) == 0:
                    self.chip8.V[15] = 1
                self.chip8.screen[(y_coord + address) % self.chip8.screen_height][(x_coord + i) % self.chip8.screen_width] = prev ^ int(pixel[i])
    def op_EX9E(self, x):
        pass

    def op_EXA1(self, x):
        pass

    def op_FX07(self, x):
        self.chip8.V[x] = self.chip8.delay_timer

    def op_FX0A(self, x):
        self.chip8.sound_timer = self.chip8.V[x]

    def op_FX15(self, x):
        self.chip8.delay_timer = self.chip8.V[x]

    def op_FX18(self, x):
        pass

    def op_FX1E(self, x):
        self.chip8.I += self.chip8.V[x]

    def op_FX29(self, x):
        self.chip8.I = 5 * x

    def op_FX33(self, x):
        self.chip8.memory[self.chip8.I] = (self.chip8.V[x] / 100) % 10
        self.chip8.memory[self.chip8.I + 1] = (self.chip8.V[x] / 10) % 10
        self.chip8.memory[self.chip8.I + 2] = (self.chip8.V[x]) % 10

    def op_FX55(self, x):
        for x in range(0, x):
            self.chip8.memory[self.chip8.I + x] = self.chip8.V[x]

    def op_FX65(self, x):
        for x in range(0, x):
            self.chip8.V[x] = self.chip8.memory[self.chip8.I + x]
