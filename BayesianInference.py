file_path = 'input2.txt'

file = open(file_path, "r")

noOfnodes = int(file.readline())
nodeValues = []
for i in range(noOfnodes):
    data = file.readline().strip().split(',')
    val = [d.strip() for d in data]
    nodeValues.append(val)

dependencies = []
for i in range(noOfnodes):
    data = file.readline().strip().split()
    val = [int(d.strip()) for d in data]
    dependencies.append(val)

numberOfSamples = int(file.readline())
samples = []
for i in range(numberOfSamples):
    data = file.readline().strip().split(',')
    val = [d.strip() for d in data]
    samples.append(val)

samplesColumns = list(zip(*samples))
edges = {i: [] for i in range(noOfnodes)}
for i in range(noOfnodes):
    for j in range(noOfnodes):
        if i != j and dependencies[i][j] > 0 and i not in edges[j] and j not in edges[i]:
            edges[j].append(i)

finalProbOfNode = []
for i in range(noOfnodes):
    parrent = edges[i]
    lst = []
    if not parrent:
        for nv in nodeValues[i]:
            countVal = len(list(filter(lambda sub : sub == nv, samplesColumns[i])))
            lst.append(countVal / numberOfSamples)
    else:
        df = []
        for p in parrent:
            df.append(samplesColumns[p])

        df.append(samplesColumns[i])
        df = list(zip(*df))
        
        probDict = {n: [] for n in nodeValues[i]}
        k = len(nodeValues[i])
        pl = len(parrent)
        for comb in range(k**pl):
            ds = list(df)
            newTuple = ()
            for j in reversed(range(pl)):
                newTuple += (nodeValues[i][comb//k**j%k],)
            
            ds = list(filter(lambda sub : sub[0:pl] == newTuple, ds))
            total = len(ds)
            for n in nodeValues[i]:
                if total == 0:
                    probDict[n].append(1/len(nodeValues[i]))
                else:
                    countVal = len(list(filter(lambda sub : sub[pl] == n, ds)))
                    probDict[n].append(countVal / total)
        for n in nodeValues[i]:
            lst += probDict[n]
            
    finalProbOfNode.append(lst)

for finalProb in finalProbOfNode:
    for prob in finalProb:
        print('{:.4f}'.format(prob), end = ' ')
    print('')