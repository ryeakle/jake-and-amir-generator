import parse

script_file = open('scripts.txt', 'r')

lines = '\n'.join(r.fixed[0] for r in parse.findall("MURPH: {}\n",
  script_file.read()))

character_file = open('murph.txt', 'w')
character_file.write('%s\n' % lines)
