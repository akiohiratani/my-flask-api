from bs4 import BeautifulSoup

class Output:
    # テーブル要素を全て出力するメソッド
    def outputTable(self, soup:BeautifulSoup):
        # table要素を全て取得
        tables = soup.find_all('table')
        with open('output/tables.txt', 'w', encoding='utf-8') as f:
            for i, table in enumerate(tables, 1):
                f.write(f"Table {i}:\n")
                f.write(table.prettify())
                f.write('\n' + '-'*40 + '\n')