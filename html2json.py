import BeautifulSoup
import requests
import simplejson as json
import sys

url = sys.argv[1]
pagedata = requests.get(url)
body = pagedata.text

def get_tabledata(htmldoc):
    soup = BeautifulSoup.BeautifulSoup(htmldoc)
    result = soup.findAll('table')
    return result

def get_polldata(htmldoc):
    soup = BeautifulSoup.BeautifulSoup(htmldoc)
    result = soup.findAll('H3')
    return result

def get_headers(table):
    allrows = table.findAll('tr')
    headers = parse_row(allrows[0])
    return headers

def parse_row(row):
    result = []
    allcols = row.findAll('td')
    for col in allcols:
        thestrings = [unicode(s) for s in col.findAll(text=True)]
        thetext = ''.join(thestrings)
        result.append(thetext)
    return result

def get_tables(table):
    result = []
    allrows = table.findAll('tr')
    headers = get_headers(table)
    for row in allrows[1:]:
        headers = get_headers(table)
        rowdata = parse_row(row)
        output = dict(zip(headers, rowdata))
        result.append(output)
    return result

def json_output():
    table_list = get_tabledata(body)
    for t in table_list:
        print json.dumps(get_tables(t), indent=2, separators=(',', ': '))

json_output()
