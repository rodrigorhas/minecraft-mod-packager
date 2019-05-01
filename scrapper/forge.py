import requests
from scrapper import parser

def request_mod_page (mod_name, page_number):
  return requests.get("https://minecraft.curseforge.com/projects/"+mod_name+"/files?page="+page_number)

def get_pagination_size (html):
  max_num_page = 1
  pagination_next_button = html.find('li', class_='b-pagination-item b-pagination-item-next')
  if pagination_next_button:
    max_num_page = pagination_next_button.find_previous_sibling('li').get_text()
  return max_num_page

  ### for each mod page
def get_mod_page_data (mod_name, html, current_page):
  if current_page != 1:
    request = request_mod_page(mod_name, str(current_page))
    html = parser.to_html(request.content)
  return get_file_table(html, current_page)

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
      'fileName': file_name,
      'url': file_url,
      'status': mod_status,
      'version': mod_version
    })
  
  return page_files