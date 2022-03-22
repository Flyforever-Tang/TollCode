def transformCoordinate(coordinate_1d: int,
                        dimensions: tuple):
    coordinates = []
    for dimension in reversed(dimensions):
        coordinates.append(coordinate_1d % dimension)
        coordinate_1d = int(coordinate_1d / dimension)
    return coordinates[::-1]

for i in range(100):
    print(i, transformCoordinate(i, (100, 4, 3)))
