import numpy as np
from matplotlib import pyplot as plt



def choose_step(m, step, starting_coord):

    yk, xk = np.array([]), np.array([])

    if len(step) != 0:

        for dir in step:

            if dir == 0 and m[starting_coord[0]+1, starting_coord[1]] == 0: #Nord
                m[starting_coord[0]+1, starting_coord[1]] = 1
                yk = np.concatenate((starting_coord[0]+1, yk), axis=None)
                xk = np.concatenate((starting_coord[1], xk), axis=None)

            elif dir == 1 and m[starting_coord[0]-1, starting_coord[1]] == 0: #Sud
                m[starting_coord[0]-1, starting_coord[1]] = 1
                yk = np.concatenate((starting_coord[0]-1, yk), axis=None)
                xk = np.concatenate((starting_coord[1], xk), axis=None)

            elif dir == 2 and m[starting_coord[0], starting_coord[1]-1] == 0: #Ovest
                m[starting_coord[0], starting_coord[1]-1] = 1
                yk = np.concatenate((starting_coord[0], yk), axis=None)
                xk = np.concatenate((starting_coord[1]-1, xk), axis=None)

            elif dir == 3 and m[starting_coord[0], starting_coord[1]+1] == 0: #Est
                m[starting_coord[0], starting_coord[1]+1] = 1
                yk = np.concatenate((starting_coord[0], yk), axis=None)
                xk = np.concatenate((starting_coord[1]+1, xk), axis=None)

        '''
        b = np.where(m == 1) #b1 sono le x, b0 sono le y
        mask0 = b[0] == starting_coord[0]
        mask1 = b[1] == starting_coord[1]
        mask2 = np.logical_and(mask0, mask1)
        mask3 = np.logical_not(mask2)

        yk = b[0][mask3]
        xk = b[1][mask3]
        '''
    #print(type(yk))
    #print(len(xk))

    return m, yk, xk



def cross_talk(m, y_init, x_init):

    n, epsilon = 4, 0.2
    p = 1 - ((1-epsilon)**(1/n))
    x_trig, y_trig = np.array([x_init]), np.array([y_init])
    #print(x_trig)
    i = 0

    while i < len(x_trig):

        #print(f'Lunghezza: {len(x_trig)}')
        print(x_trig)
        n_ct = np.random.binomial(n, p)
        step = np.random.choice(n, n_ct, replace=False)
        print(x_trig[i])
        m, yi, xi = choose_step(m, step, [int(y_trig[i]), int(x_trig[i])])

        x_trig = np.concatenate((x_trig, xi), axis=None)
        y_trig = np.concatenate((y_trig, yi), axis=None)

        i += 1

        #ytot.append(yi)
        #xtot.append(xi)

    return m, x_trig, y_trig


if __name__ == '__main__':

    sipm_size = 100

    #m, y, x = choose_step(m, step, starting_coord)
    celle = []

    for i in range(1000):
        m = np.zeros(shape=(sipm_size+2, sipm_size+2))
        m[0], m[:,0], m[-1], m[:,-1] = 1, 1, 1, 1
        starting_coord = [50, 50]
        m[starting_coord[0], starting_coord[1]] = 1

        mfin, xfin, yfin = cross_talk(m, [starting_coord[0]], [starting_coord[1]])
        m_sipm = mfin[1:-1,1:-1]
        celle.append(len(m_sipm[m_sipm==1]))

        #plt.figure()
        #plt.imshow(mfin)
    plt.hist(celle, bins=100)
    print(celle)
    plt.show()













