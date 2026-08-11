import requests
from bs4 import BeautifulSoup

def print_unicode_grid(url: str):
    response = requests.get(url)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')
    
    if not table:
        raise ValueError("未在文档中找到表格。")
        
    rows = table.find_all('tr')
    
    data = []
    for row in rows[1:]:
        cols = [ele.text.strip() for ele in row.find_all(['td', 'th'])]
        if len(cols) >= 3:
            try:
                x = int(cols[0])
                char = cols[1]
                y = int(cols[2])
                data.append((x, char, y))
            except ValueError:
                continue

    if not data:
        print("未检测到有效数据点。")
        return

    max_x = max(x for x, _, _ in data)
    max_y = max(y for _, _, y in data)

    grid = [[' ' for _ in range(max_x + 1)] for _ in range(max_y + 1)]

    for x, char, y in data:
        grid[y][x] = char

    for y in range(max_y, -1, -1):
        print(''.join(grid[y]))

doc_url = "https://docs.google.com/document/d/e/2PACX-1vTMOmshQe8YvaRXi6gEPKKlsC6UpFJSMAk4mQjLm_u1gmHdVVTaeh7nBNFBRlui0sTZ-snGwZM4DBCT/pub"
print_unicode_grid(doc_url)