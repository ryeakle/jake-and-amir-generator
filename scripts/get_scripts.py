from lxml import html
import requests

script_file = open('scripts.txt', 'w')

page = requests.get('http://scripts.jakeandamir.com/index.php?search=jake&from-date=&to-date=&do-search=1')
tree = html.fromstring(page.text)

scripts = tree.xpath('//div[@class="episode-script-inner"]/text()')

for episode in scripts:
    script_file.write("%s\n" % episode.encode('ascii', 'ignore'))
