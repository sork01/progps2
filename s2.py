# -*- coding: utf-8 -*-
# Mikael Forsberg <miforsb@kth.se>
# Robin Gunning <rgunning@kth.se>
# Skapad 2015-11-12
# Version 2015-11-17

# import pprint
import sys
import re
import math

# sys.setrecursionlimit(10000)

class lexer:
    def __init__(self, data):
        self.data = data
        # self.kwpatterns = list()
        # self.patterns = list()
        
        # self.kwpatterns.append(('keyword-forw', r'[Ff][Oo][Rr][Ww]'))
        # self.kwpatterns.append(('keyword-back', r'[Bb][Aa][Cc][Kk]'))
        # self.kwpatterns.append(('keyword-up', r'[Uu][Pp]'))
        # self.kwpatterns.append(('keyword-down', r'[Dd][Oo][Ww][Nn]'))
        # self.kwpatterns.append(('keyword-left', r'[Ll][Ee][Ff][Tt]'))
        # self.kwpatterns.append(('keyword-right', r'[Rr][Ii][Gg][Hh][Tt]'))
        # self.kwpatterns.append(('keyword-color', r'[Cc][Oo][Ll][Oo][Rr]'))
        # self.kwpatterns.append(('keyword-rep', r'[Rr][Ee][Pp]'))
        # self.kwpatterns.append(('notwhitespace', r'[^\s]+'))
        # self.patterns.append(('color-hex', r'#[a-fA-F0-9]{6}'))
        # self.patterns.append(('quote', r'"'))
        # self.patterns.append(('end-statement', r'\.'))
        # self.patterns.append(('positive-integer', r'[1-9](\d+)?'))
        # self.patterns.append(('comment', r'%[^\n]*'))
        # self.patterns.append(('whitespace', r'\s+'))
        # self.patterns.append(('notwhitespace', r'[^\s]+'))
    
    def next(self):
        if len(self.data) == 0:
            return False
        
        if self.data[0] == '.':
            self.data = self.data[1:]
            return ('end-statement', '.')
        elif self.data[0] == '"':
            self.data = self.data[1:]
            return ('quote', '"')
        elif self.data[0:3].upper() == 'REP':
            self.data = self.data[3:]
            return ('keyword-rep', 'REP')
        elif self.data[0:4].upper() == 'FORW':
            self.data = self.data[4:]
            return ('keyword-forw', 'FORW')
        elif self.data[0:4].upper() == 'BACK':
            self.data = self.data[4:]
            return ('keyword-back', 'BACK')
        elif self.data[0:2].upper() == 'UP':
            self.data = self.data[2:]
            return ('keyword-up', 'UP')
        elif self.data[0:4].upper() == 'DOWN':
            self.data = self.data[4:]
            return ('keyword-down', 'DOWN')
        elif self.data[0:4].upper() == 'LEFT':
            self.data = self.data[4:]
            return ('keyword-left', 'LEFT')
        elif self.data[0:5].upper() == 'RIGHT':
            self.data = self.data[5:]
            return ('keyword-right', 'RIGHT')
        elif self.data[0:5].upper() == 'COLOR':
            self.data = self.data[5:]
            return ('keyword-color', 'COLOR')
        
        match = re.match(r'#[a-fA-F0-9]{6}', self.data)
        if match != None:
            self.data = self.data[len(match.group(0)):]
            return ('color-hex', match.group(0))
        
        match = re.match(r'[1-9](\d+)?', self.data)
        if match != None:
            self.data = self.data[len(match.group(0)):]
            return ('positive-integer', match.group(0))
        
        match = re.match(r'%[^\n]*', self.data)
        if match != None:
            self.data = self.data[len(match.group(0)):]
            return ('comment', match.group(0))
        
        match = re.match(r'\s+', self.data)
        if match != None:
            self.data = self.data[len(match.group(0)):]
            return ('whitespace', match.group(0))
        
        match = re.match(r'[^\s]+', self.data)
        if match != None:
            self.data = self.data[len(match.group(0)):]
            return ('notwhitespace', match.group(0))
        
        return False
    
    def has_next(self):
        if len(self.data) == 0:
            return False
        
        if self.data[0] == '.':
            return True
        elif self.data[0] == '"':
            return True
        elif self.data[0:3].upper() == 'REP':
            return True
        elif self.data[0:4].upper() == 'FORW':
            return True
        elif self.data[0:4].upper() == 'BACK':
            return True
        elif self.data[0:2].upper() == 'UP':
            return True
        elif self.data[0:4].upper() == 'DOWN':
            return True
        elif self.data[0:4].upper() == 'LEFT':
            return True
        elif self.data[0:5].upper() == 'RIGHT':
            return True
        elif self.data[0:5].upper() == 'COLOR':
            return True
        
        match = re.match(r'#[a-fA-F0-9]{6}', self.data)
        if match != None:
            return True
        
        match = re.match(r'[1-9](\d+)?', self.data)
        if match != None:
            return True
        
        match = re.match(r'%[^\n]*', self.data)
        if match != None:
            return True
        
        match = re.match(r'\s+', self.data)
        if match != None:
            return True
        
        match = re.match(r'[^\s]+', self.data)
        if match != None:
            return True
        
        return False
    
    def put_back(self, str):
        self.data = str + self.data
        return True
    
    def at_end(self):
        if len(self.data) == 0:
            return True
        
        return False

class parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.processed = list()
    
    def next_token(self, req):
        if not self.lexer.has_next():
            return False
        
        toks = list()
        self.processed.append(toks)
        
        while True:
            tok = self.lexer.next()
            
            if tok == False:
                return False
            
            # print('take "' + tok[1] + '"')
            toks.append(tok)
            
            if tok[0] in req:
                return tok
            elif tok[0] == 'comment' or tok[0] == 'whitespace':
                continue
            else:
                # self.put_back()
                return False
    
    def put_back(self):
        toks = self.processed.pop()
        
        while len(toks) > 0:
            tok = toks.pop()[1]
            # print('put back "' + tok + '"')
            self.lexer.put_back(tok)
    
    def parse_error(self):
        line = 1
        fulltext = ''
        
        for tokset in self.processed:
            for tok in tokset:
                fulltext += tok[1]
                
                if tok[0] != 'comment' and tok[0] != 'whitespace':
                    line = fulltext.count("\n") + 1
        
        print('Syntaxfel på rad ' + str(line))
        # print('<<<' + fulltext + '>>>')
        return False
    
    def parse(self):
        states = list()
        states.append('program')
        
        parsetree = list()
        treeptr = list()
        treeptr.append(parsetree)
        
        map = dict()
        map[('statement', 'keyword-forw')] = 'forw-stmt'
        map[('statement', 'keyword-back')] = 'back-stmt'
        map[('statement', 'keyword-left')] = 'left-stmt'
        map[('statement', 'keyword-right')] = 'right-stmt'
        map[('statement', 'keyword-up')] = 'up-stmt'
        map[('statement', 'keyword-down')] = 'down-stmt'
        map[('statement', 'keyword-color')] = 'color-stmt'
        map[('statement', 'keyword-rep')] = 'rep-stmt'
        
        while True:
            state = states.pop()
            # print(state)
            if state == 'program':
                states.append('program-more-stmt')
                states.append('statement')
            elif state == 'program-more-stmt':
                if not self.next_token(['keyword-forw', 'keyword-back', 'keyword-left', 'keyword-right',
                        'keyword-up', 'keyword-down', 'keyword-color', 'keyword-rep']):
                    self.put_back()
                    states.append('done')
                else:
                    self.put_back()
                    states.append('program-more-stmt')
                    states.append('statement')
            elif state == 'statement':
                tok = self.next_token(['keyword-forw', 'keyword-back', 'keyword-left', 'keyword-right',
                    'keyword-up', 'keyword-down', 'keyword-color', 'keyword-rep'])
                
                if not tok:
                    return self.parse_error()
                
                # self.put_back()
                states.append(map[('statement', tok[0])])
            elif state == 'forw-stmt':
                # if not self.next_token(['keyword-forw']):
                    # return self.parse_error()
                if not self.next_token(['whitespace']):
                    return self.parse_error()
                
                tok = self.next_token(['positive-integer'])
                if not tok:
                    return self.parse_error()
                
                if not self.next_token(['end-statement']):
                    return self.parse_error()
                
                treeptr[-1].append(('forward', int(tok[1])))
            elif state == 'back-stmt':
                # if not self.next_token(['keyword-back']):
                    # return self.parse_error()
                if not self.next_token(['whitespace']):
                    return self.parse_error()
                
                tok = self.next_token(['positive-integer'])
                if not tok:
                    return self.parse_error()
                
                if not self.next_token(['end-statement']):
                    return self.parse_error()
                
                treeptr[-1].append(('back', int(tok[1])))
            elif state == 'left-stmt':
                # if not self.next_token(['keyword-left']):
                    # return self.parse_error()
                if not self.next_token(['whitespace']):
                    return self.parse_error()
                
                tok = self.next_token(['positive-integer'])
                if not tok:
                    return self.parse_error()
                
                if not self.next_token(['end-statement']):
                    return self.parse_error()
                
                treeptr[-1].append(('left', int(tok[1])))
            elif state == 'right-stmt':
                # if not self.next_token(['keyword-right']):
                    # return self.parse_error()
                if not self.next_token(['whitespace']):
                    return self.parse_error()
                
                tok = self.next_token(['positive-integer'])
                if not tok:
                    return self.parse_error()
                
                if not self.next_token(['end-statement']):
                    return self.parse_error()
                
                treeptr[-1].append(('right', int(tok[1])))
            elif state == 'color-stmt':
                # if not self.next_token(['keyword-color']):
                    # return self.parse_error()
                if not self.next_token(['whitespace']):
                    return self.parse_error()
                
                tok = self.next_token(['color-hex'])
                if not tok:
                    return self.parse_error()
                
                if not self.next_token(['end-statement']):
                    return self.parse_error()
                
                treeptr[-1].append(('color', tok[1]))
            elif state == 'down-stmt':
                # if not self.next_token(['keyword-down']):
                    # return self.parse_error()
                if not self.next_token(['end-statement']):
                    return self.parse_error()
                
                treeptr[-1].append('down')
            elif state == 'up-stmt':
                # if not self.next_token(['keyword-up']):
                    # return self.parse_error()
                if not self.next_token(['end-statement']):
                    return self.parse_error()
                
                treeptr[-1].append('up')
            elif state == 'rep-stmt':
                # if not self.next_token(['keyword-rep']):
                    # return self.parse_error()
                if not self.next_token(['whitespace']):
                    return self.parse_error()
                
                tok = self.next_token(['positive-integer'])
                if not tok:
                    return self.parse_error()
                
                contents = list()
                treeptr[-1].append(('repeat', int(tok[1]), contents)) # for non-flattening
                treeptr.append(contents)
                
                if not self.next_token(['whitespace']):
                    return self.parse_error()
                
                quoted = True
                
                if not self.next_token(['quote']):
                    self.put_back()
                    quoted = False
                
                if quoted:
                    states.append('rep-stmt-more-stmt')
                    states.append('statement')
                else:
                    states.append('rep-stmt-end')
                    states.append('statement')
            elif state == 'rep-stmt-more-stmt':
                if not self.next_token(['quote']):
                    self.put_back()
                    states.append('rep-stmt-more-stmt')
                    states.append('statement')
                else:
                    self.put_back()
                    states.append('rep-stmt-end-quoted')
            elif state == 'rep-stmt-end':
                # contents = treeptr.pop() # for flattening
                # treeptr[-1] += contents[0] * contents[1:] # for flattening
                treeptr.pop() # for non-flattening
            elif state == 'rep-stmt-end-quoted':
                if not self.next_token(['quote']):
                    return self.parse_error()
                
                #contents = treeptr.pop() # for flattening
                #treeptr[-1] += contents[0] * contents[1:] # for flattening
                treeptr.pop()
            elif state == 'done':
                # pp = pprint.PrettyPrinter(indent=2)
                # pp.pprint(parsetree)
                # quit()
                while self.next_token(['whitespace', 'comment']):
                    pass
                
                if not self.lexer.at_end():
                    return self.parse_error()
                else:
                    return parsetree
            else:
                print('unhandled: ' + state)
                print(parsetree)
                quit()

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
        quit()
        if parsetree != False:
            self.execute(parsetree)
    
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
    C = compiler()
    # C.compile(sys.stdin.read())
    C.compile(open('samples/leonardo-03.in').read())
    C.show()
