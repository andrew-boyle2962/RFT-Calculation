import numpy as np
import matplotlib.pyplot as plt

'''genericCoeff = { # 'A': {(m, n): x}
    'A': {(-1, 0): 0.0, (0, 0): 0.206, (1, 0): 0.169,
            (-1, 1): 0.0, (0, 1): 0.0, (1, 1): 0.0},
    'B': {(-1, 0): 0.0, (0, 0): 0.0, (1, 0): 0.0,
            (-1, 1): 0.055, (0, 1): 0.358, (1, 1): 0.212},
    'C': {(-1, 0): 0.0, (0, 0): 0.0, (1, 0): 0.0,
            (-1, 1): 0.007, (0, 1): 0.253, (1, 1): -0.124},
    'D': {(-1, 0): 0.0, (0, 0): 0.0, (1, 0): 0.088,
            (-1, 1): 0.0, (0, 1): 0.0, (1, 1): 0.0}
}'''

coeff = {
    name: {(m, n): 0.0 for m in [-1, 0, 1] for n in [0, 1]}
    for name in ['A', 'B', 'C', 'D']
}

# Relevant coefficient values as per Table S2 in supplementary material, Li et al. (2013)
# Coeff < 0.05 A(0, 0) are not included
coeff['A'][(0, 0)] = 0.206
coeff['A'][(1, 0)] = 0.169

coeff['B'][(1, 1)]  = 0.212
coeff['B'][(0, 1)]  = 0.358
coeff['B'][(-1, 1)] = 0.055  

coeff['C'][(1, 1)]  = -0.124
coeff['C'][(0, 1)]  = 0.253
coeff['C'][(-1, 1)] = 0.007

coeff['D'][(1, 0)] = 0.088


def AlphaGeneric(beta, gamma, κ=0):
    gamma_final = gamma - κ # Include correction angle (defaults to κ = 0)

    alpha_z = 0
    alpha_x = 0

    for m in [-1, 0, 1]:
        for n in [0, 1]:
            phase = 2*m*beta + n*gamma_final
            alpha_z += coeff['A'][(m, n)]*np.cos(phase) + coeff['B'][(m, n)]*np.sin(phase)
            alpha_x += coeff['C'][(m, n)]*np.cos(phase) + coeff['D'][(m, n)]*np.sin(phase)

    return alpha_z, alpha_x


def printGenericAlphaContour():
    # Equivalent to Fig. S7 in supplementary material, Li et al. (2013)

    gamma = np.linspace(-np.pi/2, np.pi/2, 200)
    beta = np.linspace(-np.pi/2, np.pi/2, 200)

    Gamma, Beta = np.meshgrid(gamma, beta)

    Alpha_z, Alpha_x = AlphaGeneric(Beta, Gamma)

    # plot
    plt.figure()
    plt.imshow(
        Alpha_z,
        extent=[gamma.min(), gamma.max(), beta.min(), beta.max()],
        origin='lower',
        cmap='jet',
        vmin=-1,
        vmax=1
    )

    plt.colorbar(label=r'$\alpha_z^\text{generic}$', ticks=[-1, 0, 1])
    plt.xlabel(r'$\gamma$')
    plt.ylabel(r'$\beta$')

    plt.figure()
    plt.imshow(
        Alpha_x,
        extent=[gamma.min(), gamma.max(), beta.min(), beta.max()],
        origin='lower',
        cmap='jet',
        vmin=-0.4,
        vmax=0.4
    )
    plt.colorbar(label=r'$\alpha_x^\text{generic}$', ticks=[-0.4, 0, 0.4])
    plt.xlabel(r'$\gamma$')
    plt.ylabel(r'$\beta$')

    plt.show()


if __name__ == '__main__':
    scaling_factor = 1
    print(scaling_factor*AlphaGeneric(0, np.pi/4))

    printGenericAlphaContour()