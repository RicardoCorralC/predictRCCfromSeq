import sys
import numpy as np
from scipy.spatial.distance import cosine as cosine_distance
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib.cbook import _string_to_bool

def main():
    finREAL = open(sys.argv[1])
    finPRED = open(sys.argv[2])

    dictREAL, dictPRED = dict(), dict()

    for l in finREAL:
        l = l.strip().split(',')
        domname, vector, clase = l[0], map(int,l[1:-1]), l[-1]
        dictREAL[domname] = vector

    for l in finPRED:
        l = l.strip().split(',')
        domname, vector, clase = l[0], map(int,l[1:-1]), l[-1]
        dictPRED[domname] = vector

    finREAL.close()
    finPRED.close()


    X, Y, Z = [], [], []

    for k in dictREAL:
        X.append(np.linalg.norm(dictREAL[k]) )
        Y.append(np.linalg.norm(dictPRED[k]) )

        cosine_dist = cosine_distance(dictREAL[k], dictPRED[k])
        Z.append(cosine_dist)

    plt.grid(color='0.65')
    sct = plt.scatter(X, Y, c=Z, cmap=plt.get_cmap('hot'),edgecolors='none',s=4)
    #plt.colorbar(cax, ticks=[-1, 0, 1])
    cbar = plt.colorbar(sct)
    offset = 100
    plt.axis([0, max(X) + offset, 0, max(Y) + offset])
    plt.xlabel("Real vector norm")
    plt.ylabel("Predicted vector norm")
    plt.plot([0, max(X) + offset], [0, max(X) + offset], ls="--", c=".3")
    plt.savefig("RealVSPredictedv26.png",dpi=150)
    plt.show()


if __name__ == '__main__':
    main()
