import pandas as pd
import matplotlib.pyplot as plt


def show_plot(data, titles, ylabels, ylims, marker):
    colors = ['blue', 'orange', 'green', 'red']
    _, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

    for v, c in zip(data['Commodity'].unique(), colors):
        d = data[data['Commodity'] == v]
        ax1.plot(d['date'], d['Price'], c, label=v)
    ax1.set_title(titles[0])
    ax1.set_ylabel(ylabels[0])
    ax1.set_ylim(ylims[0])
    ax1.legend(loc='upper right')

    for v, c in zip(data['Commodity'].unique(), colors):
        d = data[data['Commodity'] == v]
        ax2.plot(d['date'], d['change'], c, label=v,
                 marker=marker, linestyle='--')
    ax2.set_title(titles[1])
    ax2.set_ylabel(ylabels[1])
    ax2.set_ylim(ylims[1])
    ax2.grid(True)
    ax2.legend(loc='upper right')

    plt.tight_layout()
    plt.show()


def main():
    data = pd.read_csv('CommodityPrice.csv')
    data['date'] = [d.split('/', 1)[1] for d in data['Date']]
    data['change'] = [float(d[:-1]) for d in data['Change%']]

    show_plot(data.query('Price >= 1000'),
              ['Commodity Price (>=1000)', 'Commodity Change % (>=1000)'],
              ['Price', 'Change %'], [(1000, 3000), (-15, 15)], marker='*')

    show_plot(data.query('Price >= 500 & Price < 1000'),
              ['Commodity Price (>=500 & <1000)',
               'Commodity Change % (>=500 & <1000)'],
              ['Price', 'Change %'], [(500, 1000), (-5, 5)], marker='^')


if __name__ == "__main__":
    main()
