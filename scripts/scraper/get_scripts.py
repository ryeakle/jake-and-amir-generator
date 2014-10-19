"""
Grap all scripts from script.jakeandamir.com.

Write them out to the file scripts.txt in the data directory.

Behavior adjustable via command-line arguments (run --help for commands.)
"""
import urllib2
from bs4 import BeautifulSoup, SoupStrainer
import argparse
import parse


def remove_scene_direction(text, to_remove="({})"):
    """
    Given an inputted string `text`, remove the scene direction.

    Defaults to removing text between parentheses, but could be configured
    via  `to_remove` kwarg for other things.  `to_remove="[{}]"` for instance
    would remove text inbetween braces.
    """
    scene_direction_text_occurences = parse.findall(to_remove, text)
    indexes_to_remove = []
    for occurence in scene_direction_text_occurences:
        for start_end_index in occurence.spans.values():
            # add 1 to start and end indexes, to include the parentheses
            # in the text to be removed
            start_parens = start_end_index[0] - 1
            end_parens = start_end_index[1] + 1
            indexes_to_remove.append((start_parens, end_parens))

    indexes_to_remove_in_order = sorted(indexes_to_remove)
    text_no_scene_direction = ""
    begin_index = 0
    for start_end_index in indexes_to_remove_in_order:
        start_parens = start_end_index[0]
        end_parens = start_end_index[1]

        # grap the text up to the beginning of the parens
        text_no_scene_direction = text_no_scene_direction + text[begin_index:start_parens]

        # in the next iteration, grab text starting after the close parens
        begin_index = end_parens

    # grab any string hanging at the end
    text_no_scene_direction = text_no_scene_direction + text[begin_index:]
    return text_no_scene_direction


################
# "Main":
################
if __name__ == "__main__":
    # build command-line parser
    parser = argparse.ArgumentParser(description='Extract character lines from master script.')

    # given the --not_remove_scene_direction, don't remove text b/w parens and brackets
    parser.add_argument('--not_remove_scene_direction', help="Don't remove text b/w parentheses and brackets", action='store_false', default=True)

    # given the --not_lower_case, don't make character names lower case
    parser.add_argument('--not_lower_case', help="Don't make character names lower case", action='store_false', default=True)

    # parse command line arguments
    args = parser.parse_args()

    scripts_path = "../../data/scripts.txt"
    script_file = open(scripts_path, 'w')

    all_scripts = 'http://scripts.jakeandamir.com/index.php?search=jake&from-date=&to-date=&do-search=1'

    page = urllib2.urlopen(all_scripts)

    # use class_ to avoid syntax error on 'class' reserved name
    strained = SoupStrainer('div', class_="episode-script-inner")
    soup = BeautifulSoup(page, parse_only=strained)

    names_dict = {}
    for text in soup.strings:
        text = text.strip()
        text = text.encode('ascii', 'ignore')

        if args.not_remove_scene_direction:
            # remove text b/w parens
            text = remove_scene_direction(text)

            # remove text b/w brackets
            text = remove_scene_direction(text, to_remove="[{}]")

        if args.not_lower_case:
            # :^ option handles whitespace:
            # can find strings like "Jake:" or " Jake :" etc.
            search_result = parse.search("{:^}:", text)
            if search_result:
                start_end_index = search_result.spans.values()
                start_index = start_end_index[0][0]
                end_index = start_end_index[0][1]
                character_lower_case = text[start_index:end_index].lower()
                if start_index == 0:
                    text = character_lower_case + text[end_index:]

        if text:
            script_file.write(text + "\n")
