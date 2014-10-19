"""
Grap all scripts from script.jakeandamir.com.

Write them out to the file scripts.txt in the current directory.

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

    # given the --not_to_lower arg, don't convert all text to lower case
    parser.add_argument('--not_to_lower', help="Don't convert text to lowercase", action='store_false', default=True)

    # given the --not_remove_scene_direction, don't remove text b/w parens and brackets
    parser.add_argument('--not_remove_scene_direction', help="Don't remove text b/w parentheses and brackets", action='store_false', default=True)

    # parse command line arguments
    args = parser.parse_args()

    script_file = open('scripts.txt', 'w')

    all_scripts = 'http://scripts.jakeandamir.com/index.php?search=jake&from-date=&to-date=&do-search=1'
    # page = requests.get('http://scripts.jakeandamir.com/index.php?search=Maybe+I+should+IM+him+and+ask+him+if+he+wants+to+switch.+Hey.+%28Jake%27s+computer+makes+an+IM+sound%29&from-date=&to-date=&do-search=1')
    # tree = html.fromstring(page.text)
    one_script = 'http://scripts.jakeandamir.com/index.php?search=Maybe+I+should+IM+him+and+ask+him+if+he+wants+to+switch.+Hey.+%28Jake%27s+computer+makes+an+IM+sound%29&from-date=&to-date=&do-search=1'

    page = urllib2.urlopen(all_scripts)

    # use class_ to avoid syntax error on reserved name
    strained = SoupStrainer('div', class_="episode-script-inner")
    soup = BeautifulSoup(page, parse_only=strained)
    text = soup.get_text().strip()

    # for script_text in all_text:
    text = text.encode('ascii', 'ignore')
    if args.not_to_lower:
        text = text.lower()
    if args.not_remove_scene_direction:
        # remove b/w parens
        text = remove_scene_direction(text)

        # remove b/w brackets
        text = remove_scene_direction(text, to_remove="[{}]")

    script_file.write("%s\n" % text)
