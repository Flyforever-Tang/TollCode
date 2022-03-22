import inspect as ist


def getSource(fun):
    f = open('./' + fun.__name__ + '.py', 'w')
    f.write(ist.getsource(fun))
    f.close()


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    getSource(plt.show)
    