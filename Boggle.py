from collections import defaultdict
from nltk.corpus import words
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

english_words = ['apple', 'pickle', 'side', 'kick', 'sick', 'mood', 'cat',
                 'cats', 'man', 'super', 'antman', 'godzilla', 'dog', 'dot',
                 'sine', 'cos', 'signal', 'bitcoin', 'cool', 'zapper']

boggle = [
    ['c', 'n', 't', 's', 's'],
    ['d', 'a', 't', 'i', 'n'],
    ['o', 'o', 'm', 'e', 'l'],
    ['s', 'i', 'k', 'n', 'd'],
    ['p', 'i', 'c', 'l', 'e']
]

col_len = len(boggle[0])
row_len = len(boggle)

# Initialize trie datastructure
trie_node = {'valid': False, 'next': {}}

# lets get the delta to find all the nighbors
#L-Left R-Right C-Corner D-Down UP-Up
neighbors_delta = [
    (-1,-1, "LC"),(-1, 0, "UP"),(-1, 1, "RC"),(0, -1, "L"),(0,  1, "R"),(1, -1, "LDC"),(1,  0, "D"),(1,  1, "RDC"),
    ]

def gen_trie(word, trienode):
    """udpates the trie datastructure using the given word"""
    if not word:
        return

    if word[0] not in trienode:
        trienode[word[0]] = {'valid': len(word) == 1, 'next': {}}

    # recursively build trie
    gen_trie(word[1:], trienode[word[0]])
    
def build_trie(words, trie):
    """Builds trie data structure from the list of words given"""
    for word in words:
        gen_trie(word, trie)
    return trie
    
def get_neighbors(row, col):
    """Returns the neighbors for a given co-ordinates"""
    n = []
    for neigh in neighbors_delta:
        new_r = row + neigh[0]
        new_c = col + neigh[1]

        if (new_r >= row_len) or (new_c >= col_len) or (new_r < 0) or (new_c < 0):
            continue
        n.append((new_r, new_c, neigh[2]))
    return n
 
def dfs(row, col, visited, trie, now_word, direction):
    """Scan the graph using DFS"""
    if (row, col) in visited:
        return

    letter = boggle[row][col]
    visited.append((row, col))

    if letter in trie:
        now_word += letter

        if trie[letter]['valid']:
            print('Found "{}" {}'.format(now_word, direction))

        neighbors = get_neighbors(row, col)
        for n in neighbors:
            dfs(n[0], n[1], visited[::], trie[letter], now_word, direction + " " + n[2])
           
def main(trie_node):
    """Initiate the search for words in boggle"""
    trie_node = build_trie(english_words, trie_node)

    # print the board
    print("Given board")
    for i in range(row_len):print (boggle[i])
    print ('\n')

    for row in range(row_len):
        for col in range(col_len):
            letter = boggle[row][col]
            dfs(row, col, [], trie_node, '', 'directions from ({},{})({}) go '.format(row, col, letter))


if __name__ == '__main__':
    main(trie_node)
