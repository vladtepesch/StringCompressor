
from platform import node
from typing import overload
from functools import reduce
from tabnanny import verbose
from bitarray import bitarray
from bitarray.util import ba2base
from bitarray.util import ba2int
import pprint
import math



def ba2str(ba):
  """generated a binary textstring from the bitarray """
  return ba2base(2, ba)

class StringCompressor:
  """Compresses string data with modified Huffman encoding that allows minimal memory footprint decoding

  """

  def __init__(self, maxTree=20, treeShanon = False, verbose = False):
    """creates new StringCompressor instance

       To actually use it to compress something a model has to be built
       either by calling `trainFrom*` or `loadDecompressData`

    Args:
        maxTree (int, optional): maximum nodes in the tree. Defaults to 20.
        treeShanon (bool, optional): weather to use Shanon Fano encoding principle instead of Huffman. Defaults to False.
        verbose (bool, optional): if true, a lot of intermediate results are output. Defaults to False.
    """

    if maxTree > 63 or maxTree < 3:
      raise Exception("invalid parameter maxTree " + str(maxTree))
    self.decompressionData = None
    self.symbolTable = None
    self.nodes = None
    self.verbose = verbose
    self.maxTree = maxTree
    self.treeShanon = treeShanon
    self.restSym = 255

  def trainFromString(self, str:str):
    """creates the compression model from the given string"""
    strData = bytes(str, 'ascii')
    self.trainFromBytes(strData)

  def trainFromBytes(self, strData:bytes):
    """creates the compression model from the given bytes"""

    histS = self.__createSortedHistogram(strData)

    if self.verbose:
      for h in histS:
          print(h[0],': ', h[1] )
      print(len(histS), 'distinct symbols')

    syms, symsW = self.__buildSymbolList(histS, self.maxTree)

    self.nodes = self.buildTree(syms, symsW)
    if self.verbose:
      pprint.pprint(self.nodes)
    self.decompressData = self.__buildDecompressionData(self.nodes)
    self.symbolTable = self.__buildSymbolTable(self.nodes)
    if self.verbose:
      pprint.pprint(self.symbolTable)

  def printDotGraph(self):
    """prints a dot graph for the trained compression model"""
    gStr = 'digraph G {\n'
    for ni in self.nodes.items():
      a = ni[1]
      if a["P"]:
        i = self.nodes[a["P"]]
        gStr = gStr +  '"' + ba2str(i['code']) +'\\n'+ i['name'] + '" -> "'  + ba2str(a['code']) +'\\n'+ a['name'] + '"' + ";\n"
    print(gStr + "\n}")

  def printMermaidGraph(self):
    """prints a mermaid graph for the trained compression model"""
    gStr = 'graph TD \n'
    for ni in self.nodes.items():
      a = ni[1]
      if a["P"]:
        i = self.nodes[a["P"]]
        gStr = gStr +  '    N'+ ba2str(i['code']) +  '["' + i['name'] + '<br/>' + ba2str(i['code']) +'"] --> |'  + str(a['code'][-1]) +  '| N'+ ba2str(a['code']) +  '["' + a['name'] + '<br/>' + ba2str(a['code']) +'"]' + "\n"
    print(gStr + "\n")


  def loadDecompressData(self, decompressData):
    """reconstructs the compression model from the decompression data bytes  
       
       This may be necessary if only the decompression data is available 
       but new strings should compressed 
    """
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
            aname = ('[' + chr(ca) + ']' ) if ca != self.restSym else 'rest'
            anode = {
              'P':nodeById[cID]['name'],
              'name' : aname,
              'leaf':  True,
              'syms':  [(chr(ca), {'n':1})]  if ca != self.restSym else [('rest', {'n':1})],
              'w':1,
              'code':nodeById[cID]['code'] + bitarray('1')
            }
            nodeById[cID]['a'] = aname
            nodes[aname] = anode
          
          cbleaf = (cRefId & 0x80) != 0
          if cbleaf:
            cb = decompressData[cID][0]
            bname = ('[' + chr(cb) + ']' ) if cb != self.restSym else 'rest'
            bnode = {
              'P':nodeById[cID]['name'],
              'name' : bname,
              'leaf':  True,
              'syms':  [(chr(cb), {'n':1})]  if cb != self.restSym else [('rest', {'n':1})],
              'w':1,
              'code':nodeById[cID]['code'] + bitarray('0')
            }
            nodeById[cID]['b'] = bname
            nodes[bname] = bnode

          cb = decompressData[cID][1]
    self.nodes = nodes
    self.decompressData = decompressData
    self.symbolTable = self.__buildSymbolTable(self.nodes)
    self.maxTree = len(decompressData)
    if verbose:
      pprint.pprint(self.symbolTable)


  def compressString(self, str:str) -> bytes:
    """compresses the given string into a bytearray using the trained/loaded model

    Args:
        str (str): the string to compress

    Returns:
        bytes: compressed data
    """
    strData = bytes(str, 'ascii')
    return self.compressBytes(strData)

  ## compress
  def compressBytes(self, data:bytes) -> bytes:
    """compresses the given data into a bytearray using the trained/loaded model

    Args:
        data (bytes): bytes to compress

    Returns:
        bytes: compressed data
    """
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
    
    return compressed.tobytes()

  ##  decompress
  def decompress (self, compressed : bytes) -> bytes:
    """decompresses the given data using the trained/loaded model

    Args:
        compressed (bytes): the bytes to decompress


    Returns:
        str: the decompressed bytes
    """
    compressedStream = bitarray()
    compressedStream.frombytes(compressed)
    decompressed = bytearray()
    
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
                if nId==self.restSym:
    #                print("    rest - reading addional bits ")
                    ch = compressedStream[0:8]
                    compressedStream = compressedStream[8:]
                    sym = ba2int(ch)
                else:
                    sym = nId
    #            print("  symbol: ", ord(sym), " '", sym, "'")
                decompressed.append(sym)
                finishedSymbol = True
            else:
                nextIsEnd[0] = nId & 0x80 != 0
                nextIsEnd[1] = nId & 0x40 != 0
                s = nId & 0x3F
    #            print("  nextNodeId: ", s, " " ,nextIsEnd )
    return bytes(decompressed)

  ##  decompress
  def decompressString (self, compressed : bytes) -> str:
    """decompresses the given data using the trained/loaded model

    Args:
        compressed (bytes): the bytes to decompress


    Returns:
        str: the decompressed string
    """
    return self.decompress(compressed).decode('ascii')


  def __createSortedHistogram(self, data:bytes):
    """builds a histogram of the input data and returns a sorted list of (symb, {n, bl}) tupel"""
    hist = {}
    for c in data:
        if chr(c) in hist:
            hist[chr(c)]['n'] =  hist[chr(c)]['n'] + 1
        else:
            hist[chr(c)] = {'n':1, 'bl':c.bit_length()}

    histS = sorted(hist.items(), key = lambda x: x[1]['n'], reverse=True)
    #weight = reduce(lambda a,b:a+b[1]['n'], histS, 0)
    return histS


  def __buildSymbolList(self, histS, maxTree):
    restSyms = list(filter(lambda x: ord(x[0][0])==self.restSym , histS))
    histSfiltered = list(filter(lambda x: ord(x[0][0])!=self.restSym , histS))
    regSyms  = histSfiltered[0:maxTree]
    restSyms  = restSyms + histSfiltered[maxTree:]
    regSymsW = reduce(lambda a,b:a+b[1]['n'], regSyms, 0)
    restSymsW = reduce(lambda a,b:a+b[1]['n'], restSyms, 0)
    
    if self.verbose:
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

    if self.verbose:
      print("syms: ", syms)
      print("sum: ", symsW)
      
    return syms, symsW


  def __extendList(l, n, pad=0):
      if len(l) < n:
          l.extend([pad] * (n - len(l)))

  def buildTree(self, syms, symsW):
    if self.treeShanon:
      return self.__buildTreeShannon(syms, symsW)
    else :
      return self.__buildTreeHuffman(syms, symsW)

  def __buildTreeHuffman(self, syms, symsW):
    """creates a tree based on Huffman algorithm and returns a dictionary with the nodes
       
       - sorting the symbol list
       - combining the lasst 2 elements into one
       - repeat until only one element left
    """

    nodelist = []
    nodes = {}
    for s in syms:
        n = {
            'P':None,
            'name': '[' + s[0] + ']',
            'w': s[1]['n'],
            'leaf':True,
            'syms': [s],
        }
        nodelist.append(n)
        nodes[n['name']] = n


    while len(nodelist) >= 2:
      nodelist = sorted(nodelist, key = lambda x: x['w'], reverse=True)
      na = nodelist[-2]
      nb = nodelist[-1]
      # exchange nodes to prefer more deep trees at right ide
      # mainly to reduce effort on root->leaf correction
      if na['leaf'] and not nb['leaf']:
        t = na
        na = nb
        nb = t

      nodelist = nodelist[:-2]
      nn = {
        'P'   : None,
        'id'  : len(nodelist),
        'name': 'N'+str(len(nodelist)),
        'w'   : na['w'] + nb['w'],
        'syms': na['syms'] + nb['syms'],
        'leaf': False,
        'a'   : na['name'],
        'b'   : nb['name'],
      }
      if nn['id'] == 0:
        nn['name'] = 'TOP' 

      na['P'] = nn['name']
      nb['P'] = nn['name']
      nn['refId'] = nn['id'] | (0x80 if nb['leaf'] else 0) | (0x40 if na['leaf'] else 0)

      nodelist.append(nn)
      nodes[nn['name']] = nn

    # prevent root->leaf nodes
    top = nodes['TOP']
    if nodes[top['b']]['leaf']:
      if self.verbose:
        print('had to chose suboptimal tree to prevent root leavenode')

      t0 = nodes[top['b']]
      t1 = nodes[top['a']]
      t11 = nodes[t1['a']]
      top['a'] = t11['name']
      top['b'] = t1['name']
      t11['P'] = 'TOP'
      t0['P'] = t1['name']
      t1['a'] = t0['name']
      t1['refId'] = t1['refId'] | 0x40

    # propagate bits through the tree
    top['code'] = bitarray()
    def distributeCode(node):
      if not node['leaf']:
        nodes[node['a']]['code'] = node['code'] + bitarray('1')
        nodes[node['b']]['code'] = node['code'] + bitarray('0')
        distributeCode(nodes[node['a']])
        distributeCode(nodes[node['b']])
    distributeCode(top)
    return nodes

  def __buildTreeShannon(self, syms, symsW):
    """creates a tree based on Shannon Fano algorithm and returns a dictionary with the nodes
    
       - split the sorted (by frequency) symbol list in the middle
       - assign each to a node and repeat until all nodes only have a single symbol
    """
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
        
        if i['name'] == 'TOP':
          if sp < 2:
            if self.verbose:
              print('had to chose suboptimal tree to prevent root leavenode')
            spS = spS + i['syms'][sp][1]['n']
            sp = 2
          elif sp + 2 > len(i['syms']):
            if self.verbose:
              print('had to chose suboptimal tree to prevent root leavenode')
            sp = sp - 1 
            spS = spS - i['syms'][sp][1]['n']
        
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
            a['name'] = (str(ord(a['syms'][0][0]))  if (a['syms'][0][0]!='rest') else '' ) + ' [' + a['syms'][0][0] + ']'
        if not b['leaf']:
            b['name'] = 'N'+str(noN)
            b['id'] =  noN
            noN = noN + 1
            stack.append(b)
            #print('added b: ', b)
        else:
            b['name'] =  (str(ord(b['syms'][0][0]))  if (b['syms'][0][0]!='rest') else '' ) + ' [' + b['syms'][0][0] + ']'
            
        i['a'] = a['name']
        i['b'] = b['name']
        nodes[b['name']] = b
        nodes[a['name']] = a
    return nodes

  def __buildSymbolTable(self, treeNodes):
    symbolTable = {}
    for ni in treeNodes.items():
        i = ni[1]
        if i['leaf']:
            symbolTable[ i['syms'][0][0]] = i
    return symbolTable

  def __buildDecompressionData(self, treeNodes):
    decompressData = []
    for ni in treeNodes.items():
        i = ni[1]
        if not i['leaf']:
            StringCompressor.__extendList(decompressData, i['id']+1, [])
            decompressData[i['id'] ] = [treeNodes[i['b']]['refId'] if 'refId' in treeNodes[i['b']] else (ord(treeNodes[i['b']]['syms'][0][0]) if treeNodes[i['b']]['syms'][0][0] != 'rest' else self.restSym), 
                                        treeNodes[i['a']]['refId'] if 'refId' in treeNodes[i['a']] else (ord(treeNodes[i['a']]['syms'][0][0]) if treeNodes[i['a']]['syms'][0][0] != 'rest' else self.restSym) ]
    return decompressData


