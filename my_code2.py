# coding: utf-8

import sys
import math
import time

from Tkinter import *
from common import print_solution, read_input

class UnionFind:
    def __init__(self, size):
        # 負の値はルート (集合の代表) で集合の個数
        # 正の値は次の要素を表す
        self.table = [-1 for _ in xrange(size)]

    # 集合の代表を求める
    def find(self, x):
        if self.table[x] < 0:
            return x
        else:
            # 経路の圧縮
            self.table[x] = self.find(self.table[x])
            return self.table[x]

    # 併合
    def union(self, x, y):
        s1 = self.find(x)
        s2 = self.find(y)
        if s1 != s2:
            if self.table[s1] <= self.table[s2]:
                # 小さいほうが個数が多い
                self.table[s1] += self.table[s2]
                self.table[s2] = s1
            else:
                self.table[s2] += self.table[s1]
                self.table[s1] = s2
            return True
        return False

    # 部分集合とその要素数を返す
    def subsetall(self):
        a = []
        for i in xrange(len(self.table)):
            if self.table[i] < 0:
                a.append((i, -self.table[i]))
        return a


class PQueue:
    def __init__(self, buff = []):
        self.buff = buff[:]
        for n in xrange(len(self.buff) / 2 - 1, -1, -1):
            _downheap(self.buff, n)

    # データの追加
    def push(self, data):
        self.buff.append(data)
        upheap(self.buff, len(self.buff) - 1)

    # 最小値を取り出す
    def pop(self):
        if len(self.buff) == 0: raise IndexError
        value = self.buff[0]
        last = self.buff.pop()
        if len(self.buff) > 0:
            # ヒープの再構築
            self.buff[0] = last
            downheap(self.buff, 0)
        return value

def upheap(buff, n):
    while True:
        p = (n - 1) / 2
        if p < 0 or buff[p] <= buff[n]: break
        temp = buff[n]
        buff[n] = buff[p]
        buff[p] = temp
        n = p

def downheap(buff, n):
    size = len(buff)
    while True:
        c = 2 * n + 1
        if c >= size: break
        if c + 1 < size:
            if buff[c] > buff[c + 1]: c += 1
        if buff[n] <= buff[c]: break
        temp = buff[n]
        buff[n] = buff[c]
        buff[c] = temp
        n = c

# 距離の計算
def distance(ps):
    size = len(ps)
    table = [[0] * size for _ in xrange(size)]
    for i in xrange(size):
        for j in xrange(size):
            if i != j:
                dx = ps[i][0] - ps[j][0]
                dy = ps[i][1] - ps[j][1]
                table[i][j] = math.sqrt(dx * dx + dy * dy)
    return table

# クラスカルのアルゴリズムの応用

# 辺の定義
class Edge:
    def __init__(self, p1, p2, weight):
        self.p1 = p1
        self.p2 = p2
        self.weight = weight

    def __cmp__(x, y):
        return x.weight - y.weight

# 辺のデータを作成
def make_edge(size):
    global distance_table
    edges = PQueue()
    for i in xrange(0, size - 1):
        for j in xrange(i + 1, size):
            e = Edge(i, j, distance_table[i][j])
            edges.push(e)
    return edges

# 巡路の生成
def greedy1(size, edges):
    edge_count = [0] * size
    u = UnionFind(size)
    i = 0
    select_edge = []
    while i < size:
        e = edges.pop()
        if edge_count[e.p1] < 2 and edge_count[e.p2] < 2 and (u.find(e.p1) != u.find(e.p2) or i == size - 1):
            u.union(e.p1, e.p2)
            edge_count[e.p1] += 1
            edge_count[e.p2] += 1
            select_edge.append(e)
            i += 1
    return select_edge

# 距離の計算
def path_length(select_edge):
    n = 0
    for e in select_edge:
        n += e.weight
    return n

# データ入力
point_table = read_input(sys.argv[1])
point_size = len(point_table)
distance_table = distance(point_table)

s = time.clock()
edges = make_edge(point_size)
select_edge = greedy1(point_size, edges)
print path_length(select_edge)
print time.clock() - s


