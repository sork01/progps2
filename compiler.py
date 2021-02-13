import lexer
import parser
import math
import sys

class compiler:
    def __init__(self):
        self.pen_down = False
        self.color = '#0000FF'
        self.x = 0
        self.y = 0
        self.angle = 0
        self.lines = list()
    
    def compile(self, program):
        L = lexer.lexer(program)
        P = parser.parser(L)
        P.parse()
        self.execute(P.parsetree)
    
    def execute(self, parsetree):
        for instr in parsetree:
            if instr == 'down':
                self.pen_down = True
            if instr == 'up':
                self.pen_down = False
            if instr[0] == 'left':
                self.angle = self.angle + int(instr[1]) * math.pi / 180.0
            if instr[0] == 'right':
                self.angle = self.angle - int(instr[1]) * math.pi / 180.0
            if instr[0] == 'forward':
                oldx = self.x
                oldy = self.y
                self.x = self.x + int(instr[1]) * math.cos(self.angle)
                self.y = self.y + int(instr[1]) * math.sin(self.angle)
                
                if self.pen_down:
                    self.lines.append((self.color, oldx, oldy, self.x, self.y))
            if instr[0] == 'back':
                oldx = self.x
                oldy = self.y
                self.x = self.x - int(instr[1]) * math.cos(self.angle)
                self.y = self.y - int(instr[1]) * math.sin(self.angle)
                
                if self.pen_down:
                    self.lines.append((self.color, oldx, oldy, self.x, self.y))
            if instr[0] == 'color':
                self.color = instr[1]
            if instr[0] == 'repeat':
                for i in range(0, int(instr[1])):
                    self.execute(instr[2])
    
    def show(self):
        for line in self.lines:
            print('%s %.4f %.4f %.4f %.4f' % line)

program = sys.stdin.read()

C = compiler()
C.compile(program)
C.show()
