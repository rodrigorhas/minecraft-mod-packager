
import json
import time
import scrapper.forge
import scrapper.parser

mods = [
  # 'industrial-foregoing',
  # 'actually-additions'
  'falling-meteors-mod',
  # 'not-enough-items-1-8',
  # 'applied-energistics-2',
  # 'veinminer',
  # 'yabba',
  # 'tinkers-construct',
  # 'minefactory-reloaded',
  # 'netherores',
  # 'damage-indicators-mod',
  # 'inventory-tweaks',
  # 'enchanting-plus',
  # 'universal-electricity',
  # 'mob-dismemberment',
  # 'mutant-creatures-mod',
  # 'mob-sunscreen',
  # 'thermalexpansion',
  # 'translocators',
  # 'biomes-o-plenty',
  # 'voxelmap',
  # 'ender-storage',
  # 'ender-storage-1-8',
  # 'more-furnaces',
  # 'pure-flesh'
]

def saveToFile (file_name, page):
  Html_file= open(file_name + '.html', "w")
  Html_file.write(page.prettify())
  Html_file.close()

def file_get_contents(filename):
  with open(filename) as f:
    return f.read()

# para cada mod
for mod_name in mods:
  # faz requisicao para o curseforge
  request = scrapper.forge.request_mod_page(mod_name, '1')

  # transforma em html
  html = scrapper.parser.to_html(request.content)
  
  #html = BeautifulSoup(file_get_contents(mod + '.html'), 'html.parser')
  #saveToFile(mod_name, html)

  mod_result = []

  total_page_num = int(scrapper.forge.get_pagination_size(html))
  mod_file = open('mods/' + mod_name + '.json', "w")

  for current_page in range(1, total_page_num + 1):
    print('[{0}::{1}] Getting page {1}'.format(mod_name, current_page))
    mod_result += scrapper.forge.get_mod_page_data(mod_name, html, str(current_page))
    time.sleep(1)

  json.dump(mod_result, mod_file)
  mod_file.close()