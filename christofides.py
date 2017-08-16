import sys, math, copy, heapq, re
from scipy.sparse import coo_matrix

# get distance
def getDistance(c1, c2):
  return int(round(math.sqrt(math.pow(c1[0] - c2[0], 2) + math.pow(c1[1] - c2[1], 2))))

inputfile = 'tsp_example_3.txt' #sys.argv[1]
outputfile = inputfile + '.tour'

f = open(inputfile, 'r')
lines = f.read()
input_arr = lines.split('\n');
cities = []

for item in input_arr[:-1]:
  p = re.compile('(\d+)')
  temp = p.findall(item)
  city = {}
  city['id'] = int(temp[0])
  city['coordinates'] = [int(temp[1]), int(temp[2])]
  cities.append(city)

# Distrance matrix
n = len(cities)
w, h = n, n
graph = [[0 for x in range(w)] for y in range(h)]
adjlist = [[] for x in range(w)]
odds = []
euler_path = []
hamilton = []
for i, obj in enumerate(cities):
  for j, obj in enumerate(cities[i:]):
    j+=i
    graph[i][j] = graph[j][i] = getDistance(cities[i]['coordinates'], cities[j]['coordinates'])

# Minkey
def minkey(key, visited):
  min = sys.maxsize;
  min_index = 0;
  for v, val in enumerate(key):
    if (visited[v] == False and key[v] < min):
      min = key[v];
      min_index = v;
  return min_index;

# findMST
def findMST():
  key = [0 for x in cities]
  visited = [False for x in cities]
  parent = [0 for x in cities]

  for i, v in enumerate(key):
    key[i] = sys.maxsize;

  key[0] = 0
  parent[0] = -1

  for i, val in enumerate(key[:-1]):
    v = minkey(key, visited);
    visited[v] = True;

    for u, val in enumerate(key):
      if (graph[v][u] and visited[u] == False and graph[v][u] < key[u]):
        parent[u] = v;
        key[u] = graph[v][u];

  for v1, val in enumerate(key):
    v2 = parent[v1]
    if v2 != -1:
      adjlist[v1].append(v2)
      adjlist[v2].append(v1)

# findOdds
def findOdds():
  for i in range(0, n):
    if len(adjlist[i]) % 2 != 0:
      odds.append(int(i))

# perfect matching
def perfectMatching():
  findOdds()
  while odds:
    i = 0
    first = odds[i]
    j = i + 1 
    at = odds[j]
    end = odds[len(odds)-1]
    length = sys.maxsize

    for val in odds[j:]:
      if (graph[first][val] < length):
        length = graph[first][val]
        closest = val
    adjlist[first].append(closest)
    adjlist[closest].append(first)
    odds.remove(first)
    odds.remove(closest)

# euler
def euler(pos):
  tmp = copy.deepcopy(adjlist)
  stack = []

  while len(stack) > 0 or len(tmp[pos]) > 0:
    if len(tmp[pos]) == 0:
      euler_path.append(pos)
      pos = stack.pop()
    else:
      stack.append(pos)
      neighbor = tmp[pos][0]
      tmp[pos].remove(neighbor)

      if (len(tmp[neighbor]) > 0):
        tmp[neighbor].remove(pos)      
      pos = neighbor

  euler_path.append(pos)

# hamilton
def hamilton():
  visited = [False for x in range(0,n)]
  root = euler_path[0]
  i = 0
  curr = euler_path[i]
  i += 1
  next = euler_path[i]
  end = euler_path[len(euler_path) - 1]
  end_idx = len(euler_path) - 1 

  visited[root] = True
  path_distance = 0

  while i != end_idx:    
    if not visited[next]:
      path_distance += graph[curr][next]

      curr = next
      visited[curr] = True
      i += 1
      next = euler_path[i]
    else:
      euler_path.pop(i)
      next = euler_path[i]
    end_idx = len(euler_path)-1

  path_distance += graph[curr][next]
  return path_distance

findMST()
perfectMatching()
euler(0)
distance = hamilton()

f = open(outputfile, 'w+')
f.write(str(distance)+'\n')

for i in euler_path[0:len(euler_path)-1]:
  f.write(str(i) + '\n')

f.close()













