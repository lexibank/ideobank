import csv

concepts = [['ENGLISH', 'SPANISH', 'PORTUGUESE', 'SIMPLIFIED', 'SEMANTIC FIELD', 'SENSORY CATEGORY']]

# Load file with reconstructions
with open('raw.tsv', mode='r', encoding='utf8') as f:
    wl = csv.reader(f, delimiter='\t')

    # skip headers
    next(wl)
    next(wl)
    # Iterate through rows
    IDX = 0
    for line in wl:
        if line[8] == '':
            line[8] = 'MISSING'
        entry = [line[8], line[9], line[10], line[11], line[12], line[13]]
        if entry not in concepts:
            print(entry)
            concepts.append(entry)

print('Concepts:', len(concepts))

with open('../etc/concepts.tsv', 'w', encoding="utf8", newline='') as f:
    writer = csv.writer(f, delimiter="\t")
    writer.writerows(concepts)
