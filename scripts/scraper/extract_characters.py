"""
Creates files for each character.  Puts them in the
extract_characters_output/ directory. Requires
'scripts.txt' to be in the `data/` directory.

Defaults to creating a file for all characters, can be configured
for just one character via the --character option.
"""
import argparse
import parse
import os


def get_all_characters(script_file_handle):
    """
    Given a file handle for a script file, return a list
    of all the characters.
    """
    characters_dict = {}
    script_file_handle.seek(0)
    for line in script_file_handle.readlines():
        line = line.strip()
        search_result = parse.search('{}:', line)
        if search_result:
            character = search_result.fixed[0]
            if character not in characters_dict:
                characters_dict[character] = True
    return characters_dict.keys()


def clean_character_name(character_name):
    """
    Remvoe trailing whitespace, '/' and '*'
    """
    character_name = character_name.strip()

    # don't allow character_name names with a '/'
    if "/" in character_name:
        character_name = character_name.replace('/', '+')
    # replace '*' with empty string
    if '*' in character_name:
        character_name = character_name.replace('*', '')

    return character_name


################
# "Main":
################
if __name__ == "__main__":
    # build command-line parser
    parser = argparse.ArgumentParser(description='Extract character lines from master script.')

    # use --character to specify a character to extract
    parser.add_argument('--character', help='Extract this specific character')

    # parse command line arguments
    args = parser.parse_args()

    data_directory = "../../data/"
    scripts_path = os.path.join(data_directory, "scripts.txt")
    output_directory = os.path.join(data_directory, "characters")

    try:
        script_file_handle = open(scripts_path, 'r')
    except:
        print "Need master script file (scripts.txt) in the data directory."
        exit()

    if args.character:
        # user lower case to find character
        character_to_extract = args.character_to_extract.lower()
    else:
        characters = get_all_characters(script_file_handle)

    for character in characters:
        character = clean_character_name(character)

        script_file_handle.seek(0)

        # :^ option handles whitespace
        # e.g. can find strings like "Jake:text" or " Jake: text" etc.
        lines = '\n'.join(r.fixed[0] for r in parse.findall(character + ": {:^}\n", script_file_handle.read()))

        if lines:
            character_file = open(os.path.join(output_directory, character) + '.txt', 'w')
            character_file.write('%s\n' % lines)
