from collections import deque


class NodeQueue:
    def __init__(self):
        self._elements = deque()

    def enqueue(self, element):
        self._elements.append(element)

    def dequeue(self):
        return self._elements.popleft()

    def is_empty(self):
        return len(self._elements) == 0
