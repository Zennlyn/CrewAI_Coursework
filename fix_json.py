import json

data = []

with open("./knowledge/test_review_subset.json", 'r', encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        obj = json.loads(line)
        data.append(obj)

with open("./knowledge/test_review_subset.json", "w") as f:
    json.dump(data, f)
