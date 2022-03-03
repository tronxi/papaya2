import maude
import sys

def main(filename, debug=False):
    programFile = open(filename, "r").read().replace("\n", " ")

    maude.init()
    maude.load("src/loads.maude")
    semantics = maude.getModule('SEMANTICS')

    metaProgram = semantics.parseTerm("generate(\" " + programFile + "\")")
    metaProgram.reduce()
    moduleGrammar = semantics.parseTerm("processModule(grammar, " + str(metaProgram) + ")")
    moduleGrammar.reduce()

    system = "<> < program : Program | memory: none , state: initial , input: (${program}) , module: (${module})  > "
    generatedProgram = system.replace("${program}", str(metaProgram))
    generatedProgram = generatedProgram.replace("${module}", str(moduleGrammar))
    result,rewrites = semantics.parseTerm(generatedProgram).erewrite()
    if debug:
        # print("\nProgram:")
        # print(metaProgram)
        # print("\nGrammar:")
        # print(moduleGrammar)
        print("\nResult:")
        print(result)

if __name__ == "__main__":
    debug = False
    if len(sys.argv) > 2 and sys.argv[2] == "-d":
        debug = True
    main(sys.argv[1], debug)