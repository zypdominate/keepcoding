#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:zhuyuping
# datetime:2020/8/13 22:13

graph = {}
graph['start'] = {}
graph['start']['A'] = 6
graph['start']['B'] = 2
graph['A'] = {}
graph['A']['Final'] = 1
graph['B'] = {}
graph['B']['A'] = 3
graph['B']['Final'] = 5
graph['Final'] = {}

infinity = float('inf')
costs = {}
costs['A'] = 6
costs['B'] = 2
costs['Final'] = infinity

parents = {}
parents['A'] = 'start'
parents['B'] = 'start'
parents['Final'] = None

processed = []


def find_lowest_cost_node(costs):
    lowest_cost = float('inf')
    lowest_cost_node = None
    for node in costs:
        cost = costs[node]
        if cost < lowest_cost and node not in processed:
            lowest_cost = cost
            lowest_cost_node = node
    return lowest_cost_node


def get_lowest_cost(costs):
    cost = None
    node = find_lowest_cost_node(costs)
    while node is not None:
        cost = costs[node]
        neighbors = graph[node]
        for n in neighbors.keys():
            new_cost = cost + neighbors[n]
            if costs[n] > new_cost:
                costs[n] = new_cost
                neighbors[n] = node
        processed.append(node)
        node = find_lowest_cost_node(costs)
    return cost

if __name__ == '__main__':
    print(get_lowest_cost(costs))