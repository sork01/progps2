# -*- coding: utf-8 -*-

import sys

class parser:
    def __init__(self, lexer):
        self.tokens = lexer
        self.parsetree = list()
        self.line_reached = 1
        
        self.treeptr = list()
        self.treeptr.append(self.parsetree)
    
    def parsetree_append(self, thing):
        self.treeptr[-1].append(thing)
    
    def treestack_push(self, x):
        self.treeptr.append(x)
    
    def treestack_pop(self):
        self.treeptr.pop()
    
    def parse(self):
        # reset lexer?
        try:
            self.program()
        except:
            return self.errorbail()
        
        return self.parsetree
    
    def errorbail(self):
        print('Syntaxfel på rad ' + str(self.line_reached))
        return False
    
    def backtrack(self):
        if self.tokens.linenum() > self.line_reached:
            self.line_reached = self.tokens.linenum()
    
    def program(self):
        if not self.statement():
            return self.errorbail()
        
        while self.statement():
            pass
        
        if not self.tokens.at_end():
            return self.errorbail()
            
            # while self.tokens.has_next():
                # print(self.tokens.next())
            
            # return False
    
    def statement(self):
        if self.repable_stmt() or self.rep_stmt():
            return True
        else:
            return False
    
    def repable_stmt(self):
        if self.forw_stmt() or self.back_stmt() or self.left_stmt() or self.right_stmt() or self.up_stmt() or self.down_stmt() or self.color_stmt():
            return True
        else:
            return False
    
    def expect(self, stuff):
        count = 1
        result = list()
        
        for s in stuff:
            tok = self.tokens.next()
            
            if not tok:
                count -= 1
            
            if not tok or tok[0] != s:
                # överger möjligheten till backtracking
                # raise Exception()
                
                self.backtrack()
                
                for i in range(0, count):
                    self.tokens.put_back()
                
                return False
            else:
                result.append(tok)
                count += 1
        
        return result
    
    def forw_stmt(self):
        return self.one_arg_stmt('keyword-forw', 'positive-integer', 'forward')
    
    def back_stmt(self):
        return self.one_arg_stmt('keyword-back', 'positive-integer', 'back')
    
    def left_stmt(self):
        return self.one_arg_stmt('keyword-left', 'positive-integer', 'left')
    
    def right_stmt(self):
        return self.one_arg_stmt('keyword-right', 'positive-integer', 'right')
    
    def one_arg_stmt(self, kw, arg, pt):
        stuff = self.expect([kw, arg, 'end-statement'])
        
        if not stuff:
            return False
        else:
            self.parsetree_append((pt, stuff[1][1]))
            return True
    
    def up_stmt(self):
        stuff = self.expect(['keyword-up', 'end-statement'])
        
        if not stuff:
            return False
        else:
            self.parsetree_append(('up'))
            return True
    
    def down_stmt(self):
        stuff = self.expect(['keyword-down', 'end-statement'])
        
        if not stuff:
            return False
        else:
            self.parsetree_append(('down'))
            return True
    
    def color_stmt(self):
        return self.one_arg_stmt('keyword-color', 'color-hex', 'color')
    
    def rep_stmt(self):
        pre = self.tokens.pos()
        
        stuff = self.expect(['keyword-rep', 'positive-integer'])
        
        if not stuff:
            return False
        
        contents = list()
        self.treestack_push(contents)
        
        quoted = True
        
        if not self.tokens.has_next():
            # överge backtracking :(
            # raise Exception()
            self.backtrack()
            self.treestack_pop()
            self.tokens.rewind(pre)
            return False
        
        if self.tokens.next()[0] != 'quote':
            quoted = False
            self.tokens.put_back()
        
        if not self.statement():
            # överge backtracking :(
            # raise Exception()
            self.backtrack()
            self.treestack_pop()
            self.tokens.rewind(pre)
            return False
        
        if quoted:
            while self.statement():
                pass
            
            if not self.tokens.has_next() or self.tokens.next()[0] != 'quote':
                # överge backtracking :(
                # raise Exception()
                self.backtrack()
                self.treestack_pop()
                self.tokens.rewind(pre)
                return False
        
        self.treestack_pop()
        self.parsetree_append(('repeat', stuff[1][1], contents))
        
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

