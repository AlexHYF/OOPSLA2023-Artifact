import json
import sexpdata

data = json.loads(open("./synthesized_code.json").read())

def find_all_concepts(expr, ret):
    if isinstance(expr, list):
        for i in range(len(expr)):
            if isinstance(expr[i], sexpdata.Symbol):
                if expr[i]._val == '#':
                    #print(sexpdata.dumps(expr))
                    ret.add(sexpdata.dumps(expr[i+1]).replace("\\",""))
            if isinstance(expr[i], list):
                find_all_concepts(expr[i], ret)

def has_dup_concepts(expr, dup, ans):
    if isinstance(expr, list):
        for i in range(len(expr)):
            if isinstance(expr[i], sexpdata.Symbol):
                if expr[i]._val == '#':
                    to_add =sexpdata.dumps(expr[i+1]).replace("\\","")
                    if to_add in dup:
                        print("duplicated")
                        print(to_add)
                        ans.append([0])
                    dup.add(to_add)
            if isinstance(expr[i], list):
                has_dup_concepts(expr[i], dup, ans)
ret = set()
total = 0
for d in data:
    for impl in d['implementations']:
        total = total + 1
        is_dup = []
        has_dup_concepts(sexpdata.loads(impl.replace("'", "\"")), set(), is_dup)
        if len(is_dup) > 0:
            pass
            #print(impl.replace("'", "\""))
        #find_all_concepts(sexpdata.loads(impl.replace("'", "\"")), ret)
#ret = list(ret)
#ret.sort()
#for r in ret:
#    print(r)
#print(len(ret))
#print(total)

