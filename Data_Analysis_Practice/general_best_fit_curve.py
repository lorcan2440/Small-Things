import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import norm


def poly_funcs(degree: int):
    '''
    Returns a list of polynomial basis functions up to the given degree.
    Can be used in the best_fit function list by unpacking with:
    
    ```
    # for a linear fit, include *poly_funcs(1) in the function list:
    best_fit(x, y, [*poly_funcs(1), lambda x: np.sqrt(x), lambda x: x * np.log(x)])
    ```
    
    #### Arguments
    
    `degree` (int): highest order of the polynomial to include.

    #### Returns

    `list(callable)`: list of vectorised power functions in ascending order
        of the form `[1, x, x ** 2, ..., x ** degree]`.
    '''    

    def single_poly(n: int):
        ''' Returns one power function of a given degree. '''
        return lambda x: np.power(x, n)

    return [single_poly(i) for i in range(degree + 1)]


def best_fit(x: np.ndarray, y: np.ndarray, basis_funcs: list[callable], plot: bool = False):
    '''
    Computes a least-squares fit to a dataset with a given set of basis functions.
    
    #### Arguments
    
    `x` (np.ndarray): x-ordinate of each data point.
        If set to None, this defaults to the indices of the data,
        forcing a linear spacing between data values.
    `y` (np.ndarray): y-ordinate of each data point, representing the values to fit.
    `basis_funcs` (list[callable]): list of functions to fit. All functions must be vectorised.
        To enter a constant function, use `lambda x: np.ones_like(x) * 1`, etc.

    #### Optional Arguments

    `plot` (bool, default = False): if set to True, plot a simple Matplotlib graph showing
    the dataset, the fit curve, and the error distribution.

    #### Returns

    `(coeff, fit_vals, fit_func, errors, R2, MSE)`: a 6-tuple containing:

    `coeff` (np.ndarray): the best-fit coefficients of each basis function, in the order they were provided
    `fit_vals` (np.ndarray): the best-fit function evaluated at each x point
    `fit_func` (callable): a callable function for estimating f(x) using the best-fit function
    `errors` (np.ndarray): an array of the error at each point
    `R2` (float): the square of the Pearson correlation coefficient for the fit.
    `MSE` (float): the mean of the squared errors for the fit.
    '''

    if x is None:
        x = np.array([i for i in range(len(y))])

    A_T = np.vstack(np.array([f(x) for f in basis_funcs]))
    A = A_T.T

    coeff = np.linalg.inv(A_T.dot(A)).dot(A_T).dot(y)
    fit_vals = A.dot(coeff)
    errors = y - fit_vals

    SSE_0 = np.linalg.norm(y - np.mean(y) * np.ones(np.shape(x))) ** 2
    SSE = np.linalg.norm(errors) ** 2
    MSE = SSE / (np.size(y))
    R2 = 1 - SSE / SSE_0

    if plot:

        fig, (ax0, ax1) = plt.subplots(2, 1)
        fig.subplots_adjust(hspace=0.5)

        ax0.set_title('Dataset and Best-Fit')
        ax0.scatter(x, y, s=20)
        ax0.plot(x, fit_vals, 'r',
            label=f'$ R^2 = $ {np.round_(R2, 4)}, $ MSE = $ {np.round_(MSE, 3)}')
        ax0.set_xlabel('$ x $ value')
        ax0.set_ylabel('$ y $ value')
        ax0.legend()

        errors_stdev = np.std(errors)
        errors_mean = np.mean(errors)
        norm_x_vals = np.linspace(-3, 3, 1000)
        ax1.set_title('Standardised $ z $-distribution of errors')
        n, bins, patches = ax1.hist((errors - errors_mean) / errors_stdev,
            bins=20, density=True, facecolor='lightpink')
        ax1.plot(norm_x_vals, norm.pdf(norm_x_vals, loc=0, scale=1), 'r',
            label=f'$ \mu $ = {round(errors_mean, 4)}, $ \sigma $ = {round(errors_stdev, 4)}')
        ax1.set_xlabel('Standard deviations of error')
        ax1.set_ylabel('Frequency density')
        ax1.legend(loc='upper right')

        plt.show()

    return (
        coeff, fit_vals, lambda x: sum([c * f(x) for c, f in zip(coeff, basis_funcs)]),
        errors, R2, MSE
    )


data = np.load(r'C:\Users\lnick\Documents\Personal\Girton Cambridge\Engineering\IB Engineering\Labs and Coursework\Data Science\Data\CO2_data_full.npy')

x, y = data[:, 0], data[:, 1]

basis_funcs = [
    lambda x: np.sin(2 * np.pi * 0.99751439 * x),  # main frequency component from DFT
    lambda x: np.cos(2 * np.pi * 0.99751439 * x),
    *poly_funcs(2)]

coeff, fit_vals, fit_func, *_ = best_fit(x, y, basis_funcs, plot=True)
