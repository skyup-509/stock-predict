import numpy as np

def direction_accuracy(preds, reals):
    pred_dir = np.sign(preds)
    real_dir = np.sign(reals)
    return (pred_dir == real_dir).mean()

def cumulative_return(preds):
    return (1 + preds).prod() - 1