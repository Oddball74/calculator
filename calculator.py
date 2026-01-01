import operator
import os, sys
#Using this gentlemen's answer https://stackoverflow.com/questions/13055884/parsing-math-expression-in-python-and-solving-to-find-an-answer/13056137#13056137
required_plugins=["nlp_core"]

def __init__(self):
   for plugin in self.loaded_plugins[:]:
       if plugin["name"] == __name__:
           path = plugin["path"]
           break
   self.load_template_file(os.path.join(path,"calculator_templates.json"))
   pass

def text2int(textnum, numwords={}):
    outputs = []
    if not numwords:
      units = [
        "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
        "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
        "sixteen", "seventeen", "eighteen", "nineteen",
      ]

      tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

      scales = ["hundred", "thousand", "million", "billion", "trillion"]

      numwords["and"] = (1, 0)
      for idx, word in enumerate(units):    numwords[word] = (1, idx)
      for idx, word in enumerate(tens):     numwords[word] = (1, idx * 10)
      for idx, word in enumerate(scales):   numwords[word] = (10 ** (idx * 3 or 2), 0)

    current = result = 0
    for word in textnum.split():
        if word not in numwords:
            if result+current != 0:
                outputs.append(str(result+current))
            outputs.append(word)
            current = result = 0
            #raise Exception("Illegal word: " + word)
            continue
        scale, increment = numwords[word]
        current = current * scale + increment
        if scale > 100:
            result += current
            current = 0
    if result+current != 0:
        outputs.append(str(result+current))
    return outputs

def parse(x):
    operators = set('+-*/')
    op_out = []    #This holds the operators that are found in the string (left to right)
    num_out = []   #this holds the non-operators that are found in the string (left to right)
    buff = []
    for c in x:  #examine 1 character at a time
        if c in operators:  
            #found an operator.  Everything we've accumulated in `buff` is 
            #a single "number". Join it together and put it in `num_out`.
            num_out.append(''.join(buff))
            buff = []
            op_out.append(c)
        else:
            #not an operator.  Just accumulate this character in buff.
            buff.append(c)
    num_out.append(''.join(buff))
    return num_out,op_out

def my_eval(nums,ops):

    nums = list(nums)
    ops = list(ops)
    operator_order = ('*/','+-')  #precedence from left to right.  operators at same index have same precendece.
                                  #map operators to functions.
    op_dict = {'*':operator.mul,
               '/':operator.truediv,
               '+':operator.add,
               '-':operator.sub}
    Value = None
    for op in operator_order:                   #Loop over precedence levels
        while any(o in ops for o in op):        #Operator with this precedence level exists
            idx,oo = next((i,o) for i,o in enumerate(ops) if o in op) #Next operator with this precedence         
            ops.pop(idx)                        #remove this operator from the operator list
            values = map(float,nums[idx:idx+2]) #here I just assume float for everything
            value = op_dict[oo](*values)
            nums[idx:idx+2] = [value]           #clear out those indices
    return nums[0]

def calculate_equation(self,equation):
    #first replace any kind of text by its number
    equation = ''.join(text2int(equation)).replace(' ','')
    self.output_text(f'Refined your question in: "{equation}"')
    output = my_eval(*parse(equation))
    self.output_text(f'The answer is: "{output}"')
    a=1

