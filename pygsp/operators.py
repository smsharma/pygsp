import numpy as np
from scipy import sparse
from pygsp import utils


class operators(object):
    pass


def grad(G, s):
    r"""
    Graph gradient

    """
    if hasattr(G, 'lap_type'):
        if G.lap_type == 'combinatorial':
            print('Not implemented yet. However ask Nathanael it is very easy')
            break

    D = grad_mat(G)
    gr = D*float(s)

    return gr


def grad_mat(G):
    r"""
    Gradient sparse matrix of the graph

    """
    if not hasattr(G, 'v_in'):
        G = gsp_adj2vec(G)
        print('To be more efficient you should run: G = adj2vec(G); before using this proximal operator.')

    if hasattr(G, 'Diff'):
        D = G.Diff

    else:
        n = G.Ne
        Dc = np.ones((2*n))
        Dv = np.ones((2*n))

        Dr = np.concatenate((np.arange(n), np.arange(n)))
        Dc[:n] = G.v_in
        Dc[n:] = G.v_out
        Dv[:n] = np.sqrt(G.weights)
        Dv[n:] = -np.sqrt(G.weight)
        D = sparse.csc_matrix((Dv, (Dr, Dc)), shape=(n, G.N))

    return D


@utils.graph_array_handler
def compute_fourier_basis(G, exact=None, cheb_order=30, **kwargs):

    if hasattr(G, 'e') or hasattr(G, 'U'):
        print("This graph already has Laplacian eigenvectors or eigenvalues")

    if G.N > 3000:
        print("Performing full eigendecomposition of a large matrix\
              may take some time.")

    if False:
        # TODO
        pass
    else:
        if not hasattr(G, L):
            raise AttributeError("Graph Laplacian is missing")
        G.U, G.e = full_eigen(G.L)


def full_eigen(L):
    eigenvalues, eigenvectors = np.linalg.svd(L)

    # Sort everything
    EV = np.sort(eigenvalues)
