import numpy as np

plaintext = [[3,4,0,17],[1,14,1,7],[14,22,0,17],[4,24,14,20]]

def egcd(m, n):
    if m == 0:
        return n, 0, 1

    gcd, x_hat, y_hat = egcd(n % m, m)

    x = y_hat - (n // m) * x_hat
    y = x_hat

    return gcd, x, y


def modinv(a, m):
    """
        modinv is a function for calculate a^-1 mod m, this function will return result and
        if error this function will return -inf.
    """

    gcd, x, _ = egcd(a, m)
    if gcd != 1:
        return None
    else:
        return x % m

def matrix_modulo_invers(matrix: np.ndarray, modulus: int = 26) -> np.ndarray:
    matrix_determinant = int(np.round(np.linalg.det(matrix)))
    matrix_adjoint = np.round(
        matrix_determinant * np.linalg.inv(matrix)
    ).astype(int)
    modulo_invers_determinant = modinv(matrix_determinant % modulus, modulus)

    if(not(modulo_invers_determinant)):
        return None

    matrix_result = modulo_invers_determinant * matrix_adjoint

    return (matrix_result % modulus)


x = np.array(plaintext)

print(matrix_modulo_invers(x))