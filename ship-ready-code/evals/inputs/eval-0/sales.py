import csv

def process(f):
    d = []
    file = open(f)
    reader = csv.reader(file)
    for row in reader:
        d.append(row)
    file.close()
    result = {}
    for i in range(len(d)):
        if i == 0:
            continue
        name = d[i][0]
        amount = d[i][1]
        if name in result:
            result[name] = result[name] + float(amount)
        else:
            result[name] = float(amount)
    return result

def top(f, n):
    r = process(f)
    s = sorted(r.items(), key=lambda x: x[1], reverse=True)
    out = []
    for i in range(n):
        out.append(s[i])
    return out
