import math


def mae_error(truth : float, predictions : list[float]):
    return abs(truth - sum(predictions)/len(predictions))

def mean_across_time(errors):
    return sum(errors)/len(errors)

def mean_across_regions(errors):
    return sum(errors) / len(errors)

def mse_error(truth : float, predictions : list[float]):
    return (truth - sum(predictions)/len(predictions))**2

def sqrt_mean_across_time(errors):
    return math.sqrt(sum(errors)/len(errors) )

# --- NEW: sMAPE and MAPE on the mean of samples ---
def smape_error(truth: float, predictions: list[float], eps: float = 1e-8) -> float:
    
    yhat = sum(predictions)/len(predictions)
    return 2.0 * abs(truth - yhat) / (abs(truth) + abs(yhat) + eps)

    """
    sMAPE = 2 * |y - yhat| / (|y| + |yhat| + eps)
    (eps avoids 0/0; if both y and yhat are 0, this returns ~0.)
    """

def mape_error(truth: float, predictions: list[float], eps: float = 1e-8) -> float:

    yhat = sum(predictions)/len(predictions)
    return abs(truth - yhat) / (abs(truth) + eps)

    """
    MAPE = |y - yhat| / (|y| + eps)
    NOTE: If y=0, this explodes (controlled by eps). Often sMAPE/WAPE is preferred
    when zeros occur. Keep as-is if you want the classic behavior.
    """