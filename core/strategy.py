import numpy as np

def compute_direction_accuracy(real, pred):
    return np.mean(np.sign(real) == np.sign(pred)) * 100

def compute_return(real_price, pred_price):
    return (pred_price[-1] - real_price[0]) / real_price[0] * 100