import argparse
import parse


################
# "Main":
################
if __name__ == "__main__":
    # build command-line parser
    parser = argparse.ArgumentParser(description='Extract character lines from master script.')
    parser.add_argument('character_to_extract', help='Character to extract')

    # parse command line arguments
    args = parser.parse_args()

    # user lower case to find character
    character_to_extract = args.character_to_extract.lower()

    try:
        script_file = open('scripts.txt', 'r')
    except:
        print "Need master script file (scripts.txt) in the same directory as this extract_character.py."
        exit()

    # try {:^} or {:>} for whitespace

    lines = '\n'.join(r.fixed[0] for r in parse.findall(character_to_extract + ": {}\n",
                                                        script_file.read()))

    character_file = open(character_to_extract + '.txt', 'w')
    character_file.write('%s\n' % lines)
