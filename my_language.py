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


    def determine_variables(self):
        self.seen_conditional = False
        for i in self.from_file:

            if "?/" in i:
                pass

            if "IF" in i:
                self.seen_conditional = True
            if "+=" in i:
                new_val = i.split("+=")
                try:


                    self.assigned_variables[new_val[0].strip()] = int(self.assigned_variables[new_val[0].strip()])+int(new_val[1][1:])

                except KeyError:
                    raise Warning("Variable", new_val[0].strip(), " not declared")

            elif "=" in i and "IF" not in i:
                new_val = i.split("=")


                self.assigned_variables[new_val[0].strip()] = new_val[1][1:] if new_val[1][0] == " " else new_val[1]

            #elif "PRINT" in i and not self.seen_conditional:
            elif "PRINT" in i:
                print_statements = i.split()
                self.to_print.append(' '.join(print_statements[1:]))

    def determine_generic_actions(self, code):
        for i in code:

            if "+=" in i:
                new_val = i.split("+=")
                try:


                    self.assigned_variables[new_val[0].strip()] = int(self.assigned_variables[new_val[0].strip()])+int(new_val[1][1:])

                except KeyError:
                    raise Warning("Variable", new_val[0].strip(), " not declared")

            if "=" in i and "IF" not in i:
                new_val = i.split("=")


                self.assigned_variables[new_val[0].strip()] = new_val[1][1:] if new_val[1][0] == " " else new_val[1]

            if "PRINT" in i:
                print_statements = i.split()

                self.to_print.append(' '.join(print_statements[1:]))

            if "?/" in i:
                pass





    def find_conditionals(self):
        self.found_end = False
        start = 0
        end = 0
        for i, a in enumerate(self.from_file):
            if "IF" in a:
                start = i
                end = i

                for c, b in enumerate(self.from_file[i+1:]):
                    if "]" == b:

                        self.found_end = True
                        end += c
                        break
                if not self.found_end:
                    raise Warning("Could not find end of control")

                else:
                    self.conditionals.append(self.from_file[start:end+2])

        #print self.from_file
        #print self.conditionals

    def analyze_conditionals(self):

        for i in self.conditionals:

            header = i[0]
            header = header[4:-1]



            condition_met = False



            first_try = re.split('\s', header)



            if len(first_try) == 1:

                first = None
                second = None
                if "==" in first_try:

                    to_evaluate = first_try[0].split("==")

                    first = to_evaluate[0] if not to_evaluate[0].isdigit() else int(to_evaluate[0])
                    second = to_evaluate[-1] if not to_evaluate[-1].isdigit() else int(to_evaluate[-1])


                    if self.assigned_variables[first] == second:

                        condition_met = True

                elif ">" in first_try:
                    to_evaluate = first_try[0].split(">")

                    first = to_evaluate[0] if not to_evaluate[0].isdigit() else int(to_evaluate[0])
                    second = to_evaluate[-1] if not to_evaluate[-1].isdigit() else int(to_evaluate[-1])

                    if self.assigned_variables[first] > second:

                        condition_met = True

                elif "<" in first_try:
                    to_evaluate = first_try[0].split("<")

                    first = to_evaluate[0] if not to_evaluate[0].isdigit() else int(to_evaluate[0])
                    second = to_evaluate[-1] if not to_evaluate[-1].isdigit() else int(to_evaluate[-1])
                    if self.assigned_variables[first] < second:

                        condition_met = True

                elif ">=" in first_try:
                    to_evaluate = first_try[0].split(">=")

                    ffirst = to_evaluate[0] if not to_evaluate[0].isdigit() else int(to_evaluate[0])
                    second = to_evaluate[-1] if not to_evaluate[-1].isdigit() else int(to_evaluate[-1])
                    if self.assigned_variables[first] >= second:

                        condition_met = True

                elif "<=" in first_try:
                    to_evaluate = first_try[0].split("<=")

                    first = to_evaluate[0] if not to_evaluate[0].isdigit() else int(to_evaluate[0])
                    second = to_evaluate[-1] if not to_evaluate[-1].isdigit() else int(to_evaluate[-1])
                    if self.assigned_variables[first] <= second:

                        condition_met = True





            else: #spaces
                first = first_try[0] if not first_try[0].isdigit() else int(first_try[0])
                second = first_try[-1] if not first_try[-1].isdigit() else int(first_try[-1])
                '''
                first = first_try[0]
                second = first_try[-1]
                '''
                if "==" in first_try:

                    if self.assigned_variables[first] == second:

                        condition_met = True

                elif ">" in first_try:
                    if self.assigned_variables[first] > second:

                        condition_met = True

                elif "<" in first_try:
                    if self.assigned_variables[first] < second:

                        condition_met = True

                elif ">=" in first_try:
                    if self.assigned_variables[first] >= second:

                        condition_met = True

                elif "<=" in first_try:
                    if self.assigned_variables[first] <= second:

                        condition_met = True



            if condition_met:

                s = i[2:-1]
                s = [i.split() for i in s]
                final_s = [' '.join(i) if len(i) > 1 else ''.join(i) for i in s]

                self.determine_generic_actions(final_s)
                self.seen_conditional = False








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

        code.find_conditionals()
        code.analyze_conditionals()
        code.show_output()

    def do_exit(self, args):
        sys.exit(1)

if __name__ == "__main__":
    persius = Perseus()

    persius.cmdloop()
