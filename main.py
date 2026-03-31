import sys



class MainProof():

    def __init__(self, inputfile):
        self.knowBase = {}
        self.resolution = {}
        self.validation = None

        with open(inputfile, 'r') as file:
            for i, line in enumerate(file):
                line = line.replace('\n', '') # remove the newline character at the end of the line
                clause = line # split the line into a list of words
                #print(clause) # remove the newline character at the end of the line
                self.knowBase[i+1] = clause # this is the rule base, where i is the rule number and clause is the rule itself
        
        self.validation = self.knowBase[len(self.knowBase)] # the last line of the input file is the validation clause, which we will use to check if the resolution process is successful or not
        self.knowBase.pop(len(self.knowBase)) # remove the validation clause from the rule base, since we will use it separately to check the resolution process
        #print(self.knowBase) # print the rule base to verify that it has been read correctly
    
    def validateNegation(self):
        # this function will negate the validation clause and add it to the rule base, so that we can use it in the resolution process
        negate = self.validation.split() # split the validation clause into a list of words
        print(negate)
        for i in range(len(negate)):
            if negate[i][0] == '~': # if the word is negated, remove the negation
                negate[i] = negate[i][1:] # remove the negation
            else: # if the word is not negated, add a negation
                negate[i] = '~' + negate[i] # add a negation
            self.knowBase[len(self.knowBase)+1] = negate[i] # add the negated validation clause to the rule base, with a new rule number

    
    def kbprint(self):
        for key, value in self.knowBase.items():
            clause = ''.join(value) # join the list of words back into a string
            #print(f"{key}.{clause}" + "{" + f"{self.resolution[key]}" + "}") # print the rule number and the rule itself, without adding a newline character at the end
            print(f"{key}. {clause} " + "{}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <InputFile>")
        sys.exit(1)
    inputfile = sys.argv[1]
    
    main = MainProof(inputfile)
    main.validateNegation()
    main.kbprint()