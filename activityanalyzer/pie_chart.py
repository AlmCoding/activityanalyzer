import matplotlib.pyplot as plt
import numpy as np


def pie_chart(data: iter, title: str, min_percentage=3.0):
    # Unpack data
    labels, values = zip(*data)
    # Normalization
    total_sum = sum(values)
    values = np.array(values) / total_sum * 100
    data = dict(zip(labels, values))

    others = 0.0
    for key, val in data.items():
        if val < min_percentage:
            others += val
            data[key] = None
    data['Others'] = others
    data = {k: v for k, v in data.items() if v}

    fig1, ax1 = plt.subplots()
    ax1.set_title('{} ({}€)'.format(title, total_sum))
    ax1.pie(data.values(), labels=data.keys(), autopct='%1.1f%%', shadow=False, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    # plt.show()
    # plt.draw()
    # plt.plot()
    plt.show(block=False)


if __name__ == '__main__':
    l = 'Frogs', 'Hogs', 'Dogs', 'Logs', 'others'
    sizes = (150, 300, 450, 100, 1)
    pie_chart(zip(l, sizes), "asdf")

