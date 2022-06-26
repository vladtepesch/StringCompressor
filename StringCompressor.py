from functools import reduce
from tabnanny import verbose
from bitarray import bitarray
from bitarray.util import ba2base
from bitarray.util import ba2int
import pprint
import math



def ba2str(ba):
  return ba2base(2, ba)

class StringCompressor:
  def __init__(self, maxTree=20, verbose = False):
     self.decompressionData = None
     self.symbolTable = None
     self.nodes = None
     self.verbose = verbose
     self.maxTree = maxTree

  def train(self, strData):

    histS = StringCompressor.__createSortedHistogram(strData)

    if self.verbose:
      for h in histS:
          print(h[0],': ', h[1] )
      print(len(histS), 'distinct symbols')

    syms, symsW = StringCompressor.__buildSymbolList(histS, self.maxTree)

    self.nodes = StringCompressor.__buildTree(syms, symsW)
    if verbose:
      pprint.pprint(self.nodes)
    self.decompressData = StringCompressor.__buildDecompressionData(self.nodes)
    self.symbolTable = StringCompressor.__buildSymbolTable(self.nodes)
    if verbose:
      pprint.pprint(self.symbolTable)

  def printDotGraph(self):
    gStr = 'digraph G {\n'
    for ni in self.nodes.items():
      a = ni[1]
      if a["P"]:
        i = self.nodes[a["P"]]
        gStr = gStr +  '"' + ba2str(i['code']) +'\\n'+ i['name'] + '" -> "'  + ba2str(a['code']) +'\\n'+ a['name'] + '"' + ";\n"
    print(gStr + "\n}")


  def loadDecompressData(self, decompressData):
    nodes = {}
    nodeById = []
    for i in range(len(decompressData)):
      nn = ('N' + str(i)) if i>0 else 'TOP'
      n = {
        'name':nn,
        'leaf':False,
        'id':i,
        'refId': i,
        'code':bitarray()
      }
      nodeById.append(n)
      nodes[nn] = n

    nodes['TOP']['P'] = None
    for i in range(len(decompressData)):
      n = nodeById[i]
      for j in [0,1]:
        if (n['refId'] & (0x80 >> j)) == 0:
          cRefId = decompressData[i][j]
          cID = cRefId & 0x3F
          nodeById[cID]['P'] = n['name']
          nodeById[cID]['refId'] = cRefId
          nodeById[cID]['code'] = n['code'] + bitarray(str(j))
          n[chr(ord('a')+j)] = nodeById[cID]['name']

          caleaf = (cRefId & 0x40) != 0
          if caleaf:
            ca = decompressData[cID][1]
            aname = ('[' + chr(ca) + ']' ) if ca != 255 else 'rest'
            anode = {
              'P':nodeById[cID]['name'],
              'name' : aname,
              'leaf':  True,
              'syms':  [(chr(ca), {'n':1})]  if ca != 255 else [('rest', {'n':1})],
              'w':1,
              'code':nodeById[cID]['code'] + bitarray('1')
            }
            nodeById[cID]['a'] = aname
            nodes[aname] = anode
          
          cbleaf = (cRefId & 0x80) != 0
          if cbleaf:
            cb = decompressData[cID][0]
            bname = ('[' + chr(cb) + ']' ) if cb != 255 else 'rest'
            bnode = {
              'P':nodeById[cID]['name'],
              'name' : bname,
              'leaf':  True,
              'syms':  [(chr(cb), {'n':1})]  if cb != 255 else [('rest', {'n':1})],
              'w':1,
              'code':nodeById[cID]['code'] + bitarray('0')
            }
            nodeById[cID]['b'] = bname
            nodes[bname] = bnode

          cb = decompressData[cID][1]
    self.nodes = nodes
    self.decompressData = decompressData
    self.symbolTable = StringCompressor.__buildSymbolTable(self.nodes)
    self.maxTree = len(decompressData)
    if verbose:
      pprint.pprint(self.symbolTable)



  ## compress
  def compress(self, data):
    compressed = bitarray()
    #compressedDbgStr = ''
    for c in data:
        if chr(c) in self.symbolTable:
    #        compressedDbgStr = compressedDbgStr + ' ' + ba2str(symbolTable[chr(c)]['code'])
            compressed = compressed + ' ' + self.symbolTable[chr(c)]['code']
        else:
    #        compressedDbgStr = compressedDbgStr + ' ' + ba2str(symbolTable['rest']['code']) + '_' + "{0:08b}".format(c)
            compressed = compressed + ' ' + self.symbolTable['rest']['code'] + '_' + bitarray("{0:08b}".format(c))

    #print(compressedDbgStr)
    #print(ba2str(compressed))
    #print("length: ", len(compressed))

    # add 1 start bit and right align with padded 0 at front (and throw this away in decoder)
    # --> we always end at byte boundaries so there is no ambiguity in decoder when to stop
    compressed.insert(0, 1)
    if len(compressed)%8 != 0:
      compressed = bitarray('0') * (8-len(compressed)%8)  + compressed
    
    return compressed


  ##  decompress
  def decompress (self, compressed):
    compressedStream = compressed
    decompressed = ''
    
    # throw away padded 0
    while compressedStream[0] != 1:
      compressedStream = compressedStream[1:]
    # throw away start bit
    compressedStream = compressedStream[1:]

    while len(compressedStream) > 0:
        s = 0
        nextIsEnd = [False, False]
        finishedSymbol = False
        
        while not finishedSymbol:
            bit = compressedStream[0]
    #        print("next bit: ", bit)
            compressedStream = compressedStream[1:]
            nId = self.decompressData[s][bit]
            if nextIsEnd[bit]:
    #            print("  is end: ")
                if nId==255:
    #                print("    rest - reading addional bits ")
                    ch = compressedStream[0:8]
                    compressedStream = compressedStream[8:]
                    sym = chr(ba2int(ch))
                else:
                    sym = chr(nId)
    #            print("  symbol: ", ord(sym), " '", sym, "'")
                decompressed = decompressed + sym
                finishedSymbol = True
            else:
                nextIsEnd[0] = nId & 0x80 != 0
                nextIsEnd[1] = nId & 0x40 != 0
                s = nId & 0x3F
    #            print("  nextNodeId: ", s, " " ,nextIsEnd )
    return decompressed


  def __createSortedHistogram(data):
    hist = {}
    for c in data:
        if chr(c) in hist:
            hist[chr(c)]['n'] =  hist[chr(c)]['n'] + 1
        else:
            hist[chr(c)] = {'n':1, 'bl':c.bit_length()}

    histS = sorted(hist.items(), key = lambda x: x[1]['n'], reverse=True)
    #weight = reduce(lambda a,b:a+b[1]['n'], histS, 0)
    return histS


  def __buildSymbolList(histS, maxTree):
    regSyms  = histS[0:maxTree]
    regSymsW = reduce(lambda a,b:a+b[1]['n'], regSyms, 0)
    restSyms  = histS[maxTree:]
    restSymsW = reduce(lambda a,b:a+b[1]['n'], restSyms, 0)

    print()
    print("reg: ", regSyms)
    print("sum: ", regSymsW)

    print("rest: ", restSyms)
    print("sum: ", restSymsW)
    if len(restSyms) > 0:
        syms = regSyms + [('rest',{'n':restSymsW})]
    else:
        syms = regSyms
        
    syms = sorted(syms, key = lambda x: x[1]['n'], reverse=True)
    symsW =  restSymsW + regSymsW
    print("syms: ", syms)
    print("sum: ", symsW)
    return syms, symsW


  def __extendList(l, n, pad=0):
      if len(l) < n:
          l.extend([pad] * (n - len(l)))

  def __buildTree(syms, symsW):
    top = {
        'id':0,
        'refId':0,
        'name':'TOP',
        'leaf':False,
        'P':None,
        'syms': syms,
        'w': symsW,
        'code':bitarray()
    }
    nodes = {top['name']:top}

    stack = [top]
    noN = 1
    while (len(stack) > 0):
        i = stack.pop()
        wh = i['w']/2
        sp = 0
        spS = 0
        while spS < wh:
            spS = spS + i['syms'][sp][1]['n']
            sp = sp + 1
        
        a = {
            'P':i['name'],
            'w': spS,
            'leaf':False,
            'syms':i['syms'][:sp],
            'code':i['code']+bitarray('1'),
        }
        b = {
            'P':i['name'],
            'w': i['w']-spS,
            'leaf':False,
            'syms':i['syms'][sp:],
            'code':i['code']+bitarray('0'),
        }
        a['leaf'] = len(a['syms'])<=1
        b['leaf'] = len(b['syms'])<=1
        i['refId'] =  i['id'] | (0x80 if b['leaf'] else 0) | (0x40 if a['leaf'] else 0)
        if not a['leaf']:
            a['name'] = 'N'+str(noN)
            a['id'] = noN
            noN = noN + 1
            stack.append(a)
            #print('added a: ', a)
        else:        
            a['name'] = '[' + a['syms'][0][0] + ']'
        if not b['leaf']:
            b['name'] = 'N'+str(noN)
            b['id'] =  noN
            noN = noN + 1
            stack.append(b)
            #print('added b: ', b)
        else:
            b['name'] = '[' + b['syms'][0][0] + ']'
            
        i['a'] = a['name']
        i['b'] = b['name']
        nodes[a['name']] = a
        nodes[b['name']] = b
    return nodes

  def __buildSymbolTable(treeNodes):
    symbolTable = {}
    for ni in treeNodes.items():
        i = ni[1]
        if i['leaf']:
            symbolTable[ i['syms'][0][0]] = i
    return symbolTable

  def __buildDecompressionData(treeNodes):
    decompressData = []
    for ni in treeNodes.items():
        i = ni[1]
        if not i['leaf']:
            StringCompressor.__extendList(decompressData, i['id']+1, [])
            decompressData[i['id'] ] = [treeNodes[i['b']]['refId'] if 'refId' in treeNodes[i['b']] else (ord(treeNodes[i['b']]['syms'][0][0]) if treeNodes[i['b']]['syms'][0][0] != 'rest' else 255), 
                                        treeNodes[i['a']]['refId'] if 'refId' in treeNodes[i['a']] else (ord(treeNodes[i['a']]['syms'][0][0]) if treeNodes[i['a']]['syms'][0][0] != 'rest' else 255) ]
    return decompressData


