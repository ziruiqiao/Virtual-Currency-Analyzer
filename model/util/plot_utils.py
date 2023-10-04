import torch
from matplotlib import pyplot as plt
from sklearn.preprocessing import OneHotEncoder


def plot_curve(data):
    fig = plt.figure()
    plt.plot(range(len(data)), data, color='blue')
    plt.legend(['value'], loc='upper right')
    plt.xlabel('step')
    plt.ylabel('value')
    plt.show()


def plot_image(img, label, name):
    fig = plt.figure()
    for i in range(6):
        plt.subplot(2, 3, i+1)
        plt.tight_layout()
        plt.imshow(img[i][0] * 0.3081 + 0.1307, cmap='gray', interpolation='none')
        plt.title(f"{name}: {label[i].item()}")
        plt.xticks([])
        plt.yticks([])
    plt.show()


def one_hot(label, depth=4):
    out = torch.zeros(label.size(0), depth)
    out[torch.arange(label.size(0)), label] = 1
    return out