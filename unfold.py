from typing import Iterable


def unfold(array: Iterable):
    unfolded_array = []
    for data in array:
        if isinstance(data, Iterable):
            unfolded_array += unfold(data)
        else:
            unfolded_array.append(data)
    return unfolded_array


if __name__ == '__main__':
    print(unfold([[1, 2, 3], [4, [5, 6]]]))
    