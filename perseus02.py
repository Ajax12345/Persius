import re
from cmd import Cmd
import sys
#TODO: add user input, for loop, while loop
class Interpretor:
    def __init__(self, from_file):
        self.from_file = from_file
        self.assigned_variables = {}
        self.to_print = []
        self.conditionals = []
        self.seen_conditional = False
        self.conditional_count = 0

    def determine_variables(self):
        for loc, i in enumerate(self.from_file):
            if "?/" in i:
                pass
            else:
                if self.seen_conditional:
                    if "]" in i:

                        self.seen_conditional = False

                else:


                    if "+=" in i and "FOR" not in i:
                    #new_val = i.split("+=")
                        new_val = re.split("\s*\+=\s*", i)

                        try:


                        #self.assigned_variables[new_val[0].strip()] = int(self.assigned_variables[new_val[0].strip()])+int(new_val[1][1:])
                            self.assigned_variables[new_val[0]] = int(new_val[-1])
                        except KeyError:
                            raise Warning("Variable", new_val[0], " not declared")

                    if "=" in i and "IF" not in i and "==" not in i:

                    #new_val = i.split("=")
                        parts = re.split("\s*\=\s*", i)
                        self.assigned_variables[parts[0]] = parts[-1]

                    #self.assigned_variables[new_val[0].strip()] = new_val[1][1:] if new_val[1][0] == " " else new_val[1]

                    if "PRINT" in i:
                        print_statements = i.split()

                        self.to_print.append(' '.join(print_statements[1:]))


                    if "IF" in i:

                        self.seen_conditional = True

                        self.find_conditionals(i, loc)

                    if "FOR" in i:

                        self.analyze_for_loop(loc)



    def determine_generic_actions(self, code):
        for loc, i in enumerate(code):

            if "?/" in i:
                pass
            else:

                if self.conditional_count > 1:

                    if "]" in i:

                        self.seen_conditional = False
                        self.conditional_count = 0




                else:


                    if "+=" in i:
                    #new_val = i.split("+=")
                        new_val = re.split("\s*\+=\s*", i)

                        try:


                        #self.assigned_variables[new_val[0].strip()] = int(self.assigned_variables[new_val[0].strip()])+int(new_val[1][1:])
                            self.assigned_variables[new_val[0]] = int(new_val[-1])
                        except KeyError:
                            raise Warning("Variable", new_val[0], " not declared")

                    if "=" in i and "IF" not in i and "==" not in i:

                    #new_val = i.split("=")
                        parts = re.split("\s*\=\s*", i)
                        self.assigned_variables[parts[0]] = parts[-1]

                    #self.assigned_variables[new_val[0].strip()] = new_val[1][1:] if new_val[1][0] == " " else new_val[1]

                    if "PRINT" in i and self.conditional_count == 1:

                        print_statements = i.split()


                        self.to_print.append(' '.join(print_statements[1:]))


                    if "IF" in i:

                        #self.seen_conditional = True
                        if self.conditional_count == 0:

                            self.find_conditionals(i, loc)

                    if "FOR" in i:

                        self.analyze_for_loop(loc)





    def find_conditionals(self, header, starting_place):
        self.found_end = False
        start = starting_place+1
        end = 0

        for i, a in enumerate(self.from_file[start:]):

            if "]" in a:

                end = i
                break



        self.analyze_conditionals(header, self.from_file[start+1:start+end])

        #print self.from_file
        #print self.conditionals
    def analyze_for_loop(self, to_start): #passed index where header of loop begins

        header = self.from_file[to_start]


        parts = re.split(";\s*", header[header.index("<")+1:-1])
        parts = [i for i in parts if i]
        if len(parts) < 3:
            raise Warning("Need to give addition condition")

        else:

            #need to actually execute perseus code here
            first = re.split("\s*\=\s*", parts[0])
            second = re.split("\s*\<*\<=*\s*", parts[1])
            third = re.split("\s*\+\=\s*", parts[2])

            if not all(i[0] == first[0] for i in [first, second, third]):
                raise Warning("Inconsistant variable names in for-loop")

            range_data = [int(first[-1]), int(second[-1]), int(third[-1])]
            #print range_data

            #now, find block:
            bracket_indices = []
            for indexs, i in enumerate(self.from_file[to_start+1:]):
                if i == "[":
                    bracket_indices.append(indexs)
                if i == "]":
                    bracket_indices.append(indexs)
                    break
            #print bracket_indices #note that this is only valid in the data self.from_file[to_start+1:]

            for code_index in range(range_data[0], range_data[1], range_data[2]):
                self.assigned_variables[first[0]] = code_index


                self.determine_generic_actions(self.from_file[to_start+1:][bracket_indices[0]:bracket_indices[-1]])




    def analyze_conditionals(self, condition, conditional_code):

        #for i in self.conditionals:
        #rint "The condition:", condition
        #print "conditional code", conditional_code


        filtered_condition = condition[condition.index("<")+1:-1]
        #IF <Val1 == 234>

        #first = re.split("\s*\==*\<=*\>=*\<*\>*\s*", filtered_condition)
        first = re.split("\s*\==*\<*\>*\s*", filtered_condition)


        if "==" in filtered_condition:
            if first[1].isdigit():
                #print self.assigned_variables

                if int(self.assigned_variables[first[0]]) == int(first[1]):
                    self.conditional_count += 1
                    self.determine_generic_actions(conditional_code)

                    #self.conditional_count += 1


            else:
                if self.assigned_variables[first[0]] == first[1]:
                    self.conditional_count += 1
                    self.determine_generic_actions(conditional_code)


        elif "<" in filtered_condition:
            if first[1].isdigit():

                if self.assigned_variables[first[0]] < int(first[1]):
                    self.conditional_count += 1
                    self.determine_generic_actions(conditional_code)
                    #self.conditional_count += 1

            else:
                if self.assigned_variables[first[0]] < first[1]:
                    self.conditional_count += 1
                    self.determine_generic_actions(conditional_code)
                    #self.conditional_count += 1

        elif ">" in filtered_condition:
            if first[1].isdigit():
                if self.assigned_variables[first[0]] > int(first[1]):
                    self.conditional_count += 1
                    self.determine_generic_actions(conditional_code)
                    #self.conditional_count += 1

            else:
                if self.assigned_variables[first[0]] > first[1]:
                    self.conditional_count += 1
                    self.determine_generic_actions(conditional_code)
                    #self.conditional_count += 1


    def find_errors(self):
        raise NotImplementedError("Still working on it")

    def show_output(self):

        for i in self.to_print:
            if i in self.assigned_variables:
                print self.assigned_variables[i]

            else:
                print i




    def show_variables(self):
        print self.assigned_variables
        print self.to_print

    def __str__(self):
        raise NotImplementedError("Unable to run")


class Perseus(Cmd):
    prompt = ""
    intro = "Welcome to Persius 0.1. Please specify the filename that contains your code"
    def __init__(self):
        Cmd.__init__(self)

    def do_perseus(self, pathname):



        #f = open('my_language.txt').readlines()
        f = open(pathname).readlines()
        f = [i.strip('\n') for i in f]


        code = Interpretor(f)
        code.determine_variables()

        code.show_output()

    def do_exit(self, args):
        sys.exit(1)

if __name__ == "__main__":
    '''
    persius = Perseus()

    persius.cmdloop()
    '''
    f = open("my_language.txt").readlines()
    f = [i.strip('\n') for i in f]


    code = Interpretor(f)
    code.determine_variables()

    code.show_output()
