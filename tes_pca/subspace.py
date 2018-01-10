import numpy as np

# custom
def process_pca(matrix, num_components=0):
    [row, col] = matrix.shape
    if num_components <= 0 or num_components>row:
        num_components = row

    print('before :', matrix)
    # compute mean
    mu = np.sum(matrix, axis=0) / len(matrix)
    print('mean :', mu)

    # compute covariance matrix
    matrix = matrix - mu
    print('after :', matrix)

    if row > col:
        S = np.dot(matrix.T, matrix)
        [eigenvalues, eigenvectors] = np.linalg.eigh(S)
    else:
        S = np.dot(matrix, matrix.T)
        [eigenvalues, eigenvectors] = np.linalg.eigh(S)
        eigenvectors = np.dot(matrix.T, eigenvectors)
        for i in range(row):
            eigenvectors[:,i] = eigenvectors[:,i]/np.linalg.norm(eigenvectors[:,i])
    
    # sort eigenvectors descending by their eigenvalue
    idx = np.argsort(-eigenvalues)
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:,idx]
    
    # select only num_components
    eigenvalues = eigenvalues[0:num_components].copy()
    eigenvectors = eigenvectors[:,0:num_components].copy()

    return [eigenvalues, eigenvectors, mu]

def project(W, X, mu=None):
	if mu is None:
		return np.dot(X,W)
	return np.dot(X - mu, W)

def reconstruct(W, Y, mu=None):
	if mu is None:
		return np.dot(Y,W.T)
	return np.dot(Y, W.T) + mu

def pca(X, y, num_components=0):
	[n,d] = X.shape
	if (num_components <= 0) or (num_components>n):
		num_components = n

	# Calculate Mean
	mu = X.mean(axis=0)
	print('Mean : ')
	print(mu)
	print()

	# Calculate Covariance Matrix
	X = X - mu
	if n>d:
		C = np.dot(X.T,X)
		[eigenvalues,eigenvectors] = np.linalg.eigh(C)
	else:
		C = np.dot(X,X.T)
		[eigenvalues,eigenvectors] = np.linalg.eigh(C)
		eigenvectors = np.dot(X.T,eigenvectors)
		for i in range(n):
			eigenvectors[:,i] = eigenvectors[:,i]/np.linalg.norm(eigenvectors[:,i])
	# or simply perform an economy size decomposition
	# eigenvectors, eigenvalues, variance = np.linalg.svd(X.T, full_matrices=False)
	# sort eigenvectors descending by their eigenvalue
	idx = np.argsort(-eigenvalues)
	eigenvalues = eigenvalues[idx]
	eigenvectors = eigenvectors[:,idx]
	# select only num_components
	eigenvalues = eigenvalues[0:num_components].copy()
	eigenvectors = eigenvectors[:,0:num_components].copy()
	return [eigenvalues, eigenvectors, mu]