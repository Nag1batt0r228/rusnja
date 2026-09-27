filename = "/home/zenoviibabiak/prog/lisst.txt"
porfolio =[]
with open(filename) as file:
    for line in file:
        line= line.strip()
        if not line:
            continue
        row = line.split(',')
        name = row[0].strip()
        shares = int(row[1].strip())
        price = float(row[2].strip())
        holding = (name, shares, price)
        porfolio.append(holding)

print(porfolio)