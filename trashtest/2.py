type Vector = list[float]

def scale(scalar: float, vector: Vector) -> Vector:
    return [scalar * num for num in vector]

scales = scale(2, [1.2, -2.4, 3.6])
print(scales)
