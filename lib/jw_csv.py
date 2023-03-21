import csv
# csv file func
def writeCsv(filepath, header, listBody):    
    with open(filepath, 'wt', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if header != None:
            writer.writerow(header)
        for row in listBody:
            writer.writerow(row)

def readCsv(filepath):
    data = []    
    with open(filepath, 'rt', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        data = list(reader)
    return data


if __name__ == '__main__':
    header = ['1', '2', '3']
    body = [
        ['a', 'b', 'c'],
        ['g', 'e', 'd']
    ]
    writeCsv('csvTest.csv', header, body)

    data = readCsv('csvTest.csv')
    print(data[1])