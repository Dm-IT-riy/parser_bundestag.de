from bs4 import BeautifulSoup
import requests
import json
import os



#Deleting an old files to avoid repeating old data
if os.path.isfile('persons_links.txt'):
    os.remove('persons_links.txt')
    print('\n' + '#' * 50)
    print('The old file "persons_links.txt" has been deleted!\nA new file will be created!')
    print('#' * 50 + '\n')
else:
    print('\n' + '#' * 45)
    print('The file "persons_links.txt" will be created!')
    print('#' * 45 + '\n')

if os.path.isfile('data.json'):
    os.remove('data.json')
    print('\n' + '#' * 42)
    print('The old file "data.json" has been deleted!\nA new file will be created!')
    print('#' * 42 + '\n')
else:
    print('\n' + '#' * 37)
    print('The file "data.json" will be created!')
    print('#' * 37 + '\n')



HEADERS = {
    'Accept': '*/*',
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 YaBrowser/21.8.2.381 Yowser/2.5 Safari/537.36'
}

#Collecting a link to the pages
persons_url_links = []
for i in range(0, 760, 20):
    url = f'https://www.bundestag.de/ajax/filterlist/en/members/453158-453158?limit=20&noFilterSet=true&offset={i}'

    req = requests.get(url, headers = HEADERS)
    res = req.content

    soup = BeautifulSoup(res, 'lxml')

    persons = soup.find_all(class_ = 'bt-open-in-overlay')

    for i in persons:
        person_link = i.get('href')
        persons_url_links.append(person_link)

#Saving the list of links
with open('persons_links.txt', 'a') as file:
    for link in persons_url_links:
        file.write(f'{link}\n')

#Follow each link from the file and collect data about each member of Parliament
with open('persons_links.txt') as file:
    lines = [line.strip() for line in file.readlines()]

    count = 0
    data_dict = []
    for line in lines:
        req = requests.get(line)
        res = req.content

        soup = BeautifulSoup(res, 'lxml')

        person = soup.find('div', class_ = 'bt-biografie-name').find('h3').text
        person_name_company = person.strip().split(',')
        person_name = person_name_company[0]
        person_company = person_name_company[1].strip()

        person_contacts = soup.find_all(class_ = 'bt-link-extern')
        
        contacts_urls = []
        for contact in person_contacts:
            contacts_urls.append(contact.get('href'))

        person = {
            'name': person_name,
            'company': person_company,
            'contacts': contacts_urls
        }

        count += 1
        print(f'Member №{count}: {line} is recorded!')

        data_dict.append(person)

        #Saving the collected data to a json file
        with open('data.json', 'w', encoding = 'utf-8') as json_file:
            json.dump(data_dict, json_file, indent=4, ensure_ascii = False)
