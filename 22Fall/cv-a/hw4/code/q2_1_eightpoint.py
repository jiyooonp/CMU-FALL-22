import numpy as np
import matplotlib.pyplot as plt

from helper import displayEpipolarF, calc_epi_error, toHomogenous, refineF, _singularize

# Insert your package here


'''
Q2.1: Eight Point Algorithm
    Input:  pts1, Nx2 Matrix
            pts2, Nx2 Matrix
            M, a scalar parameter computed as max (imwidth, imheight)
    Output: F, the fundamental matrix

    HINTS:
    (1) Normalize the input pts1 and pts2 using the matrix T.
    (2) Setup the eight point algorithm's equation.
    (3) Solve for the least square solution using SVD. 
    (4) Use the function `_singularize` (provided) to enforce the singularity condition. 
    (5) Use the function `refineF` (provided) to refine the computed fundamental matrix. 
        (Remember to usethe normalized points instead of the original points)
    (6) Unscale the fundamental matrix
'''


def eightpoint(pts1, pts2, M):
    N = pts1.shape[0]

    T = np.diag([1 / M, 1 / M, 1])

    npts1 = pts1 / M
    npts2 = pts2 / M

    x1 = npts1
    x2 = npts2

    A = [
        [x2[i, 0] * x1[i, 0], x2[i, 0] * x1[i, 1], x2[i, 0], x2[i, 1] * x1[i, 0], x2[i, 1] * x1[i, 1], x2[i, 1],
         x1[i, 0], x1[i, 1], 1]
        for i in range(N)
    ]

    A = np.array(A).reshape(N, -1)
    u, s, vh = np.linalg.svd(A)
    F = vh[-1, :].reshape(3, 3)

    F = _singularize(F)
    F = refineF(F, npts1, npts2)

    F = T.T @ F @ T
    F = F / F[-1, -1]

    np.savez('results/q2_1.npz', F=F, M=M)

    return F


if __name__ == "__main__":
    correspondence = np.load('data/some_corresp.npz')  # Loading correspondences
    intrinsics = np.load('data/intrinsics.npz')  # Loading the intrinscis of the camera
    K1, K2 = intrinsics['K1'], intrinsics['K2']
    pts1, pts2 = correspondence['pts1'], correspondence['pts2']
    im1 = plt.imread('data/im1.png')
    im2 = plt.imread('data/im2.png')

    F = eightpoint(pts1, pts2, M=np.max([*im1.shape, *im2.shape]))
    # [:10, :]
    print(F)
    # Q2.1
    displayEpipolarF(im1, im2, F)

    # Simple Tests to verify your implementation:
    pts1_homogenous, pts2_homogenous = toHomogenous(pts1), toHomogenous(pts2)

    assert (F.shape == (3, 3))
    assert (F[2, 2] == 1)
    assert (np.linalg.matrix_rank(F) == 2)
    assert (np.mean(calc_epi_error(pts1_homogenous, pts2_homogenous, F)) < 1)
