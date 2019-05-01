
import json
import time
import scrapper.mcversion
import scrapper.parser

html = scrapper.mcversion.request_main_page()
all_versions_data = scrapper.mcversion.get_minecraft_versions(html)

minecraft_versions_file = open('output/minecraft-versions.json', 'w')
json.dump(all_versions_data, minecraft_versions_file)
minecraft_versions_file.close()