import numpy as np
from scipy.stats import norm


if __name__ == '__main__':
    values = []
    for i in range(400):

        '''Probabilidad aleatoria'''
        p = np.random.rand()

        '''Distribución Normal Inversa'''
        inverse_normal = round(float(round(norm.ppf(p, loc=0, scale=0.3), 4)), 4)

        values.append(str(inverse_normal))

    # values.sort()
    values = '\n'.join(values)
    print(values)
