import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd

def main():
    df = pd.read_csv('Average_height6-15years old.csv')
    fig, axs = plt.subplots(2, 2)
    fig.set_size_inches(16, 12)

    queries = ['`school year` == 100', 'age == 13']
    titles = {
        (0, 0): '100-AVG Height Total',
        (0, 1): '100-AVG Height Boys&Girls',
        (1, 0): 'AVG Height Total',
        (1, 1): 'AVG Height Boys&Girls',
    }
    ylims = [(100, 170), (150, 160)]
    xaxis_major_locator = ticker.MultipleLocator(1)
    yaxis_major_locators = [ticker.MultipleLocator(10), ticker.MultipleLocator(1)]
    xks = ['age', 'school year']
    locs = ['upper left', 'upper right']

    for i in range(2):
        query = df.query(queries[i])
        x = np.array(query[xks[i]])
        for j in range(2):
            k = (i, j)
            if j == 0:
                y = np.array(query['total'])
                axs[k].bar(x, y, width=0.5, color='gray', label='total', zorder=0)
                axs[k].scatter(x, y, linewidths=4, color='red', zorder=1)
                axs[k].plot(x, y, linewidth=2, color='green', zorder=2)
            else:
                y = np.array(query['boy'])
                axs[k].bar(x-0.15, y, width=0.3, color='blue', label='boy')
                y = np.array(query['girl'])
                axs[k].bar(x+0.15, y, width=0.3, color='red', label='girl')
            axs[k].set_title(titles[k])
            axs[k].set_ylim(ylims[i])
            axs[k].set_xlabel(xks[i])
            axs[k].set_ylabel('height')
            axs[k].legend(loc=locs[i])
            axs[k].xaxis.set_major_locator(xaxis_major_locator)
            axs[k].yaxis.set_major_locator(yaxis_major_locators[i])
    plt.show()


if __name__ == '__main__':
    main()
