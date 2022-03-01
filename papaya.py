import maude
import sys

def main(filename, debug=False):
    programFile = open(filename, "r").read().replace("\n", " ")

    maude.init()
    maude.load("src/loads.maude")
    semantics = maude.getModule('SEMANTICS')

    metaProgram = semantics.parseTerm("generate(\" " + programFile + "\")")
    system = " < program : Program | memory: none , input: (${program})  > "
    generatedProgram = system.replace("${program}", str(metaProgram))

    result,rewrites = semantics.parseTerm(generatedProgram).erewrite()
    if debug:
        print("\nResult:")
        print(result)

if __name__ == "__main__":
    debug = False
    if len(sys.argv) > 2 and sys.argv[2] == "-d":
        debug = True
    main(sys.argv[1], debug)