# -*- coding: utf-8 -*-
# Mikael Forsberg <miforsb@kth.se>
# Robin Gunning <rgunning@kth.se>
# Skapad 2015-11-12

import traceback
import sys
import re
import math

class lexer:
    def __init__(self, s):
        self.data = s
        self.patterns = list()
        
        #self.data = re.sub(r'%[^\n]+', '', self.data)
        
        self.patterns.append(('keyword-forw', r'[Ff][Oo][Rr][Ww]'))
        self.patterns.append(('keyword-back', r'[Bb][Aa][Cc][Kk]'))
        self.patterns.append(('keyword-up', r'[Uu][Pp]'))
        self.patterns.append(('keyword-down', r'[Dd][Oo][Ww][Nn]'))
        self.patterns.append(('keyword-left', r'[Ll][Ee][Ff][Tt]'))
        self.patterns.append(('keyword-right', r'[Rr][Ii][Gg][Hh][Tt]'))
        self.patterns.append(('keyword-color', r'[Cc][Oo][Ll][Oo][Rr]'))
        self.patterns.append(('keyword-rep', r'[Rr][Ee][Pp]'))
        self.patterns.append(('color-hex', r'#[a-fA-F0-9]{6}'))
        self.patterns.append(('quote', r'"'))
        self.patterns.append(('end-statement', r'\.'))
        self.patterns.append(('positive-integer', r'[1-9](\d+)?'))
        self.patterns.append(('comment', r'%[^\n]*'))
        self.patterns.append(('whitespace', r'\s+'))

    def next(self):
        if len(self.data) == 0:
            return False
        for name, regex in self.patterns:
            match = re.match(regex, self.data)
            if match != None:
                self.data = self.data[len(match.group(0)):]
                return (name, match.group(0))
        
        return False    

    def has_next(self):
        tok = self.next()
        
        if tok == False:
            return False
        
        self.put_back(tok[1])
        return True

    def put_back(self, str):
        self.data = str + self.data
        return True
    
    def at_end(self):
        if len(self.data) == 0:
            return True
        
        return False

class parser:
    def __init__(self, lexer):
        self.tokens = list()
        
        while lexer.has_next():
            self.tokens.append(lexer.next())
        
        self.lexer_reached_end = lexer.at_end()
        self.tokens.reverse()
        self.parsetree = list()
        self.line_reached = 1
        self.line_seen = 1
        self.parse_error = False
        
        self.treeptr = list()
        self.treeptr.append(self.parsetree)

    def parsetree_append(self, thing):
        self.treeptr[-1].append(thing)

    def treestack_push(self, x):
        self.treeptr.append(x)

    def treestack_pop(self):
        self.treeptr.pop()

    def next_token(self, req):
        while True:
            if len(self.tokens) == 0:
                return False
            
            tok = self.tokens.pop()
            
            if tok[0] == req:
                self.line_seen += tok[1].count("\n")
                
                if self.line_seen > self.line_reached:
                    self.line_reached = self.line_seen
                
                return tok
            elif tok[0] == 'comment' or tok[0] == 'whitespace':
                self.line_seen += tok[1].count("\n")
            else:
                if self.line_seen > self.line_reached:
                    self.line_reached = self.line_seen
                
                self.tokens.append(tok)
                return False
    
    def parse(self):
        if not self.program():
            print('Syntaxfel på rad ' + str(self.line_reached))
            return False
        else:
            return self.parsetree
    
    def raise_parse_error(self):
        self.parse_error = True
        return False
    
    def program(self):
        if not self.statement():
            return False
        
        while self.statement():
            pass
        
        while self.next_token('whitespace') or self.next_token('comment'):
            pass
        
        if self.parse_error or len(self.tokens) != 0 or not self.lexer_reached_end:
            #print(self.tokens)
            return False
        
        return True
    
    def statement(self):
        if self.parse_error:
            return False
        
        if self.repable_stmt() or self.rep_stmt():
            return True
        else:
            return False
    
    def repable_stmt(self):
        if self.parse_error:
            return False
        
        if self.forw_stmt() or self.back_stmt() or self.left_stmt() or self.right_stmt() or self.up_stmt() or self.down_stmt() or self.color_stmt():
            return True
        else:
            return False
    
    def forw_stmt(self):
        return self.one_arg_stmt('keyword-forw', 'positive-integer', 'forward')
    
    def back_stmt(self):
        return self.one_arg_stmt('keyword-back', 'positive-integer', 'back')
    
    def left_stmt(self):
        return self.one_arg_stmt('keyword-left', 'positive-integer', 'left')
    
    def right_stmt(self):
        return self.one_arg_stmt('keyword-right', 'positive-integer', 'right')
    
    def one_arg_stmt(self, kw, arg, pt):
        if self.parse_error:
            return False
        
        if not self.next_token(kw):
            return False
        
        if not self.next_token('whitespace'):
            return self.raise_parse_error()
        
        tok = self.next_token(arg)
        if not tok:
            return self.raise_parse_error()
        
        if not self.next_token('end-statement'):
            return self.raise_parse_error()
        
        self.parsetree_append((pt, tok[1]))
        return True
    
    def up_stmt(self):
        pos = len(self.tokens)
        
        if not self.next_token('keyword-up'):
            return False
        
        if not self.next_token('end-statement'):
            return self.raise_parse_error()
        
        self.parsetree_append(('up'))
        return True
    
    def down_stmt(self):
        pos = len(self.tokens)
        
        if not self.next_token('keyword-down'):
            return False
        
        if not self.next_token('end-statement'):
            return self.raise_parse_error()
        
        self.parsetree_append(('down'))
        return True
    
    def color_stmt(self):
        return self.one_arg_stmt('keyword-color', 'color-hex', 'color')
    
    def rep_stmt(self):
        while True:
            if not self.next_token('keyword-rep'):
                return False
            
            numreps = self.next_token('positive-integer')
            if not numreps:
                return self.raise_parse_error()
            
            if not self.next_token('whitespace'):
                return self.raise_parse_error()
            
            self.treestack_push(list())
            
            quoted = True
            
            if not self.next_token('quote'):
                quoted = False
            
            tok = self.next_token('keyword-rep')
            if tok != False:
                self.tokens.append(tok)
                continue
            
            if not self.statement():
                return self.raise_parse_error()
            
            if quoted:
                while True:
                    if not self.statement():
                        if not self.next_token('quote'):
                            return self.raise_parse_error()
                        else:
                            break
            
            contents = self.treestack_pop()
            self.parsetree_append(('repeat', numreps[1], contents))
            
            return True
    
    def prettyprint(self, tree, depth):
        for val in tree:
            if type(val) == str:
                print('  '*depth + val)
            elif type(val) == tuple:
                sys.stdout.write('  '*depth)
                for tval in val:
                    if type(tval) == str:
                        sys.stdout.write(tval + ' ')
                    elif type(tval) == list:
                        sys.stdout.write("\n")
                        self.prettyprint(tval, depth+1)
                
                sys.stdout.write("\n")

class compiler:
    def __init__(self):
        self.pen_down = False
        self.color = '#0000FF'
        self.x = 0
        self.y = 0
        self.angle = 0
        self.lines = list()
    
    def compile(self, program):
        if re.match(r'^\s*$', program):
            print('')
            quit()
        
        L = lexer(program)
        P = parser(L)
        
        parsetree = P.parse()
        
        if parsetree != False:
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

if __name__ == '__main__':
    com = compiler()
    #com.compile(sys.stdin.read()
    com.compile(open('samples/leonardo-02.in').read())
    com.show()
