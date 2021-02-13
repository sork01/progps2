import sys
import re

class lexer:

    def __init__(self, s):
        self.data = s
        self.tokens = list()
        self.program()
        
    def next():
        pass
        
    def program(self):
        self.statements()
        while self.statements() != False:
            pass

    def statements(self):
        if self.forw_statement() or self.back_statement() or self.empty_state():
            return True
        return False

    def forw_statement(self):
        if self.data.startswith("FORW"):
            pos = self.data.find(" ")
            self.data = self.data[pos + 1:]
            digit = self.data[:1]
            self.tokens.append(["FORW", digit])
            self.data = self.data[1:]
            self.end_statement()
            return True
        return False


    
    def back_statement(self):
        if self.data.startswith("BACK"):
            pos = self.data.find(" ")
            self.data = self.data[pos + 1:]
            digit = self.data[:1]
            self.tokens.append(["BACK", digit])
            self.data = self.data[1:]
            self.end_statement()
            return True
        return False
        
    def end_statement(self):
        if self.data.startswith("."):            
            self.data = self.data[1:]
            print self.data
            
    def empty_state(self):
        if self.data.startswith(" "):
            print re.match(r'[a-z][1-9]', self.data)
    
x = lexer("FORW 5. BACK 1. FORW 8.")
print x.tokens