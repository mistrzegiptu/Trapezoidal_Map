def generateParallelSegments(maxX, maxY, n):
    divider = maxY / 2.0
    above = n // 2
    below = n - n // 2
    segments = []

    deltaX = deltaY = (maxY - divider) / (above + 1)
    for i in range(1, above + 1):
        segments.append(((i * deltaX, divider + deltaY), (maxX - i * deltaX, divider + deltaY)))

    deltaY = divider / (below + 1)
    for i in range(1, below + 1):
        segments.append((((i - 0.5) * deltaX, divider - deltaY), (maxX - (i - 0.5) * deltaX, divider - deltaY)))

    return segments


def calculateDSize(node, count, visited):
    if node is None or node in visited:
        return
    count[0] += 1
    visited.add(node)
    calculateDSize(node.left, count, visited)
    calculateDSize(node.right, count, visited)


def generateUniformPoints(maxX, maxY, n):
    x_coord = np.random.uniform(1, maxX, n)
    y_coord = np.random.uniform(1, maxY, n)

    res = [(x, y) for x, y in zip(x_coord, y_coord)]
    return res