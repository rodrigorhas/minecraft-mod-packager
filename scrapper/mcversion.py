import requests
from scrapper import parser

def request_main_page ():
  return parser.cache_request('https://mcversions.net/')

def get_minecraft_versions (html):
  release_column = html.find('span', class_='btn-stable')
  release_list = release_column.parent.find('ul', class_="list-group")
  release_list_items = release_list.find_all('li', class_='list-group-item')

  all_releases = []

  for release in release_list_items:

    r_version = release.find('strong', class_='version').get_text()
    r_date = release.find('span', class_='time').get_text()
    r_client_anchor = release.find('a', class_='client')
    r_server_anchor = release.find('a', class_='server')

    if not r_client_anchor or not r_server_anchor: continue;

    all_releases.append({
      'version': r_version.strip(),
      'date': r_date.strip(),
      'client': {
        'name': r_client_anchor['download'],
        'url': r_client_anchor['href']
      },
      'server': {
        'name': r_server_anchor['download'],
        'url': r_server_anchor['href']
      }
    })
  
  return all_releases
    
def get_file_table (html, current_page):
  # pega a tabela de arquivos
  mod_version_files = html.find_all('tr',class_='project-file-list-item')

  page_files = []

  print('Page {}: {} mod file versions found'.format(current_page, len(mod_version_files)))

  # para cada arquivo na tabela
  for current_file in mod_version_files:
    mod_version = current_file.find('span', class_='version-label').get_text()
    was_released = bool(current_file.find('div', class_='release-phase'))
    mod_status = 'release' if was_released else 'unstable'
    anchor = current_file.find('a', class_='overflow-tip twitch-link')
    file_name = anchor.get_text()
    file_url = anchor['href']

    page_files.append({
      'filename': file_name,
      'url': file_url,
      'status': mod_status,
      'version': mod_version
    })
  
  return page_files