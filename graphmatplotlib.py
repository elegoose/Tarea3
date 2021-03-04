import matplotlib.pyplot as plt


def drawgraph(suscount, recoveredcount, deathcount, infectedcount, daycount):
    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    total = suscount + recoveredcount + deathcount + infectedcount
    sus = 'Susceptibles', int(100*(suscount/total))
    recovered = 'Recuperados', int(100*(recoveredcount/total))
    deaths = 'Muertos', int(100*(deathcount/total))
    infected = 'Infectados', int(100*(infectedcount/total))
    possible_labels = (sus, recovered, deaths, infected)
    labels = ()
    sizes = []
    for label in possible_labels:
        label_name = label[0]
        label_percentage = label[1]
        if label_percentage > 0:
            labels += (label_name,)
            sizes += [label_percentage]

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax1.set(title=f'Día {daycount}')
    plt.show()