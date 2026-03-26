import json

data = []

with open("./knowledge/test_review_subset.json", 'r', encoding="utf-8") as f:
    i = 0
    for line in f:
        if i == 1:
            break
        line = line.strip()
        if not line:
            continue
        obj = json.loads(line)
        data.append(obj)
        i+=1

with open("./knowledge/test_review_subset.json", "w") as f:
    json.dump(data, f)