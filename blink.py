import sys, operator as operators

class blink:
    def __init__(self):
        self.vars = {}
        self.file = sys.argv[1]
        self.ops = {

                '*':operators.mul,'-':operators.sub,'+':operators.add, '/':operators.div, '=':operators.eq, '>':operators.gt, '<':operators.lt, '>=':operators.ge, '<=':operators.le, '!=':operators.ne}

        self.para = {}
    def start(self):
        with open(self.file, 'r') as file:
            self.tokenize(file.read())

    def tokenize(self, code):
        self.parse(code.replace("\n", '').replace("[", ' [ ').replace("]", ' ] ').replace("(", ' ( ').replace(")"," ) ").split())

    def parse(self, tokens):
        pointer = 0
        length = len(tokens) - 1
        while length != pointer:
            toke = tokens[pointer]
            if toke == "{":
                tokens.remove("{")
                while tokens[pointer] != "}":
                    out = []
                    if tokens[pointer] == '[':
                        pointer += 1
                        while tokens[pointer] != ']':
                            if tokens[pointer] == '(':
                                what = []
                                while tokens[pointer] != ")":
                                    if tokens[pointer] == '(':
                                        pointer += 1
                                        continue
                                    what.append(tokens[pointer])
                                    pointer += 1
                                self.para[pointer] = what
                            else:
                                out.append(tokens[pointer])
                                pointer += 1
                        self.evaluate(out)
                        continue
                    pointer += 1
                continue
            pointer += 1
    
    def evaluate(self, out):
        first = out[0]
        if 'assign' == first:
            var = out[1]
            val = out[2]
            if '@' in val:
                try:
                    val = val.replace("@", '')
                    self.vars[var] = self.vars[val]
                except:
                    print "Variable Error:", ' '.join(out)
                    exit()
            else:
                try:
                    val = int(val)
                    self.vars[var] = val
                except:
                    if isinstance(val, str):
                        self.vars[var] = ' '.join(out[2:])
            
        if 'say' == first:
            val = out[1]
            if '@' in val:
                try:
                    val = self.vars[val.replace("@", '')]
                    print val
                except:
                    print 'Variable Error:',' '.join(out)
                    exit()
            else:
                try:
                    print int(val)
                except:
                    print str(' '.join(out[1:]))
        
        if 'math' == first:
            var = out[1]
            first = out[2]
            op = out[3]
            second = out[4]
            
            if '@' in first:
                try:
                    first = self.vars[first.replace("@", '')]
                except:
                    print "Variable Error:", ' '.join(out)
            else:
                try:
                    first = int(first)
                except:
                    print "Math Error:", ' '.join(out)
            if '@' in second:
                try:
                    second = self.vars[second.replace("@", '')]
                except:
                    print "Variable Error:", ' '.join(out)
            else:
                try:
                    second = int(second)
                except:
                    print "Math Error:", ' '.join(out) 
            self.vars[var] = self.ops[op](first, second)

        if 'if' == first:
            first = out[1]
            op = out[2]
            second = out[3]
            if '@' in first:
                try:
                    first = self.vars[first.replace("@", '')]
                except:
                    print "Variable Error:", ' '.join(out)
            if "@" in second:
                try:
                    second = self.vars[second.replace("@", '')]
                except:
                    print "Variable Error:", ' '.join(out)
            try:
                first = int(first)
            except:
                pass
            try:
                second = int(second)
            except:
                pass
            boolean = self.ops[op](first, second)
            if boolean:
                nums = []
                for x in self.para:
                    self.evaluate(self.para[x])
                for x in self.para:
                    nums.append(x)
                for x in nums:
                    del self.para[x]

        if 'while' == first:
            first = out[1]
            op = out[2]
            second = out[3]
            consq = out[4:]
            if '@' in first:
                try:
                    first = self.vars[first.replace("@", '')]
                except:
                    print "Variable Error:", ' '.join(out)
            if "@" in second:
                try:
                    second = self.vars[second.replace("@", '')]
                except:
                    print "Variable Error:", ' '.join(out)
            try:
                first = int(first)
            except:
                pass
            try:
                second = int(second)
            except:
                pass
            boolean = self.ops[op](first, second)
            if boolean:
                while True:
                    if '@' in out[1]:
                        first = self.vars[out[1].strip("@")]
                    if '@' in out[3]:
                        second = self.vars[out[3].strip("@")]
                    boolean = self.ops[op](first, second)
                    if boolean:
                        for x in self.para:
                            self.evaluate(self.para[x])
                    else:
                        break

if __name__ == "__main__":
    try:
        blink().start()
    except IndexError:
        pass
