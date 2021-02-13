# -*- coding: utf-8 -*-

import re

class lexer:
    def __init__(self, s):
        self.data = s
        self.tokens = list()
        self.line = 1
        
        self.patterns = list()
        
        self.data = re.sub(r'%[^\n]+', '', self.data)
        
        # self.patterns.append(('ignore', r'\s+|%[^\n]+\n'))
        self.patterns.append(('ignore', r'\s+'))
        self.patterns.append(('keyword-forw', r'[Ff][Oo][Rr][Ww]\s+'))
        self.patterns.append(('keyword-back', r'[Bb][Aa][Cc][Kk]\s+'))
        self.patterns.append(('keyword-up', r'[Uu][Pp](\s+)?'))
        self.patterns.append(('keyword-down', r'[Dd][Oo][Ww][Nn](\s+)?'))
        self.patterns.append(('keyword-left', r'[Ll][Ee][Ff][Tt]\s+'))
        self.patterns.append(('keyword-right', r'[Rr][Ii][Gg][Hh][Tt]\s+'))
        self.patterns.append(('keyword-color', r'[Cc][Oo][Ll][Oo][Rr]\s+'))
        self.patterns.append(('keyword-rep', r'[Rr][Ee][Pp]\s+'))
        self.patterns.append(('color-hex', r'#[a-fA-F0-9]{6}(\s+)?'))
        self.patterns.append(('quote', r'"(\s+)?'))
        self.patterns.append(('end-statement', r'\.(\s+)?'))
        self.patterns.append(('positive-integer', r'[1-9](\d+)?(\s+)?'))
    
    def linenum(self):
        return self.line

    def next(self):
        if len(self.data) == 0:
            return False
        for name, regex in self.patterns:
            match = re.match(regex, self.data)
            if match != None:
                self.line += match.group(0).count("\n")
                self.data = self.data[len(match.group(0)):]
                self.tokens.append(match.group(0))
                if name == 'ignore':
                    return self.next()
                return (name, match.group(0))
        return False    

    def has_next(self):
        if self.next() == False:
                return False
        self.put_back()
        return True

    def put_back(self):
        if len(self.tokens) == 0:
            return False
        
        tok = self.tokens.pop()
        
        self.line -= tok.count("\n")
        self.data = tok + self.data
        
        return True
    
    def pos(self):
        return len(self.tokens)

    def rewind(self, pos):
        for i in range(0, self.pos() - pos):
            self.put_back()

    def at_end(self):
        if len(self.data) == 0:
            return True
        return False
