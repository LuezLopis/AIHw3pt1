import sys



class MainProof():

    def __init__(self, inputfile):
        self.knowBase = {}
        self.resolution = {}
        self.contradiction = None
        self.validation = None
        self.splitcache = {}  # Add cache dictionary
        self.clausesets = {}  # Cache sets for redundancy check

       
        with open(inputfile, 'r') as file:
            for i, line in enumerate(file):
                line = line.replace('\n', '') # remove the newline character at the end of the line
                clause = line # split the line into a list of words
                #print(clause) # remove the newline character at the end of the line
                self.knowBase[i+1] = clause # this is the rule base, where i is the rule number and clause is the rule itself
        
        self.validation = self.knowBase[len(self.knowBase)] # the last line of the input file is the validation clause, which we will use to check if the resolution process is successful or not
        self.knowBase.pop(len(self.knowBase)) # remove the validation clause from the rule base, since we will use it separately to check the resolution process
        #print(self.knowBase) # print the rule base to verify that it has been read correctly
    
    
    def getSplit(self, clause):
        """Get split clause with caching"""
        if clause not in self.splitcache:
            self.splitcache[clause] = clause.split()
        return self.splitcache[clause]


    def validateNegation(self):
        # this function will negate the validation clause and add it to the rule base, so that we can use it in the resolution process
        negates = self.validation.split() # split the validation clause into a list of words
        #print(negates)
        if len(negates) == 1: # if the validation clause is a single negated word, remove the negation and add it to the rule base
            negate = negates[0] # remove the negation
            if negate[0] == '~': # if the word is negated, remove the negation
                negate = negate[1:] # remove the negation
            else: # if the word is not negated, add a negation
                negate = '~' + negate # add a negation
            self.knowBase[len(self.knowBase)+1] = negate # add the negated validation clause to the rule base, with a new rule number
        else:
            for i in range(len(negates)):
                if negates[i][0] == '~': # if the word is negated, remove the negation
                    negates[i] = negates[i][1:] # remove the negation
                else: # if the word is not negated, add a negation
                    negates[i] = '~' + negates[i] # add a negation
                self.knowBase[len(self.knowBase)+1] = negates[i] # add the negated validation clause to the rule base, with a new rule number

    
    def kbprint(self, ans):
        #print(self.resolution)
        for key, value in self.knowBase.items():
            clause = ''.join(value) # join the list of words back into a string
            #print(f"{key}.{clause}" + "{" + f"{self.resolution[key]}" + "}") # print the rule number and the rule itself, without adding a newline character at the end
            if key in self.resolution:
                i, j= self.resolution[key]
                print(f"{key}. {clause} " + "{"+ f"{i}, {j}" +"}")
            else:
                print(f"{key}. {clause} " + "{ }")
        if ans:
            i, j = self.contradiction
            print(f"{key+1}" + ". Contradiction {" + f"{i}, {j}" + "}\nValid")
        else:
            print(f"{key+1}. No contradiction\nInvalid")

    def getClauseSet(self, clause): # increase efficiency of redundancy check by caching sets of clause parts
        if clause not in self.clausesets:
            parts = self.getSplit(clause)
            self.clausesets[clause] = frozenset(parts)
        return self.clausesets[clause]

    def redundancyCheck(self, clause):
        """Check if clause is subsumed by any existing clause"""

        clauseParts = self.getClauseSet(clause) # get the clause as a frozenset for faster comparison
        
        for existingClause in self.knowBase.values():
            existingClauseParts = self.getClauseSet(existingClause) # get the existing clause as a frozenset for faster comparison
        
            if clauseParts == existingClauseParts: # check if the new clause is a subset of an existing clause
                #print(f"Clause {clause} is the same as {existingClause}, skipping...")
                return True # if it is, then it is redundant and we can skip it

        return False
          
    def mirrorliteralCheck(self, clause):
        if not clause:
            return False
        
        parts = self.getSplit(clause)
        pos_set = set()
        neg_set = set()
        
        for lit in parts:
            if lit.startswith('~'):
                neg_set.add(lit[1:])
            else:
                pos_set.add(lit)
        
        # Check if any literal appears both positively and negatively
        return bool(pos_set & neg_set)        


    def resolutionProcess(self, parentClause1, ruleNum1, clauseParts2, ruleNum2):
        
        #resolventFound = False
        set1 = set(parentClause1)
        set2 = set(clauseParts2)
    
        # Quick check: if no complementary literals possible
        # This is faster than nested loops for large clauses
        for lit in set1:
            neg = lit[1:] if lit.startswith('~') else '~' + lit
            if neg in set2:
                # Found possible resolution, proceed with detailed check
                break
        else:
            return 2  # No possible resolution



        for i, part in enumerate(parentClause1):
            #print(f"Checking C1 {part} of {parentClause1}")
            for j, part2 in enumerate(clauseParts2):
                #print(f"Checking C2 {part2} of {clauseParts2}")
                if part == '~' + part2 or '~' + part == part2: # check if the parts are negations of each other
                    
                    #print(f"Found resolvent between {part} and {part2} in {parentClause1} and {clauseParts2}")

                    #resolventFound = True
                    newClause = [] # create a new clause by removing the negated parts from both clauses and combining the remaining parts
                    
                    for k, p in enumerate(parentClause1):
                        if i != k:
                            #print(f"Adding {p} from {parentClause1} to new clause") # print the part that we are adding to the new clause to verify that it is correct
                            newClause.append(p) # add the remaining parts of the first clause to the new clause  
                    for k, p in enumerate(clauseParts2):
                        if j != k:
                            #print(f"Adding {p} from {clauseParts2} to new clause") # print the part that we are adding to the new clause to verify that it is correct
                            newClause.append(p) # add the remaining parts of the second clause to the new clause
                     # print the new clause to verify that it has been created correctly
                    
                    couple = (ruleNum1, ruleNum2)
                    newClause = sorted(list(set(newClause))) # remove duplicates from the new clause
                    newClauseStr = ' '.join(newClause) if newClause else ''
                    # join the list of words back into a string
                    
                    #check if the clause exist in a differnt order in the rule base, if it does, then we can skip it and move on to the next resolution step, since we have already derived this clause before 

                    #print(f"New Clause {newClause} from {parentClause1} and {clauseParts2}")
                    #print(f"Resolving {ruleNum1} and {ruleNum2} to get {newClauseStr}") # print the resolution step to verify that it is correct
                    
                    if self.mirrorliteralCheck(newClauseStr): # check if the new clause has a mirror literal, if it does, then we can skip it and move on to the next resolution step
                        #print(f"Clause {newClauseStr} has a mirror literal, skipping...")
                        continue

                    if not newClauseStr: # if the new clause is empty, it means that we have derived a contradiction, which means that the original validation clause is true
                        #print("The validation clause is true.")
                        self.contradiction = couple # store the parent clauses that were resolved to create the contradiction, so that we can print them later
                        return 1
                    
                    if not self.redundancyCheck(newClauseStr): # check if the new clause is redundant, if it is not, then we can add it to the rule base and continue with the resolution process
                        if newClauseStr not in self.knowBase.values(): # if the new clause is not already in the rule base, add it to the rule base with a new rule number
                            #print(f"Adding new clause {newClauseStr} to the rule base") # print the new clause that we are adding to the rule base to verify that it is correct
                            self.knowBase[len(self.knowBase)+1] = newClauseStr # add the new clause to the rule base, with a new rule number
                            self.resolution[len(self.knowBase)] = couple # add the new clause to the resolution dictionary, with a new rule number and the parent clauses that were resolved to create it
                            return 0 # if the new clause is already in the rule base, return False, which means that we have already derived this clause before, so we can skip it and move on to the next resolution step   
                else:
                    #print(f"No resolvent between {part} and {part2} in {parentClause1} and {clauseParts2}")
                    pass
        return 2  # if we have gone through all the parts of both clauses and have not found any negations of each other, return 3, which means that we cannot resolve these two clauses, so we can skip it and move on to the next resolution step


    def mainProcess(self):
        size = len(self.knowBase)+1
        i = 1

        while i < size:
            #print(f"Processing clause {i}...") # print the clause that we are processing to verify that it is correct
            for j in range(1, i):
                #print(f"Resolving {i} and {j}...") # print the clauses that we are resolving to verify that it is correct
                clause1 = self.knowBase[i] # get the first clause from the rule base
                clause2 = self.knowBase[j] # get the second clause from the rule base
                clauseParts1 = self.getSplit(clause1)
                clauseParts2 = self.getSplit(clause2) # split the second clause into a list of words

                ans = self.resolutionProcess(clauseParts1, i, clauseParts2, j) # call the resolution process function to resolve the two clauses and check if we have derived a contradiction or not
                if ans == 1: # if we have derived a contradiction, return True, which means that the original validation clause is true
                    return True
                elif ans == 0: # if we have derived a new clause, add it to the rule base and update the size of the rule base, so that we can continue to resolve new clauses with the existing clauses in the rule base
                    size = len(self.knowBase)+1
                    
            i+=1
        return False # if we have resolved all possible pairs of clauses and have not derived a contradiction, return False, which means that the original validation clause is false


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <InputFile>")
        sys.exit(1)
    inputfile = sys.argv[1]
    
    main = MainProof(inputfile)
    main.validateNegation()
    ans = main.mainProcess()
    main.kbprint(ans)

