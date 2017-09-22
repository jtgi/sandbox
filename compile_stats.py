import sys
import plotly.graph_objs as go

from os import listdir
from os.path import isfile, join
from plotly.offline import plot
from itertools import groupby

TIME = 0
ROUND = 1
FIGHTER = 2
LANDED = 3
PUNCH = 4

colors = [
    dict(
        color='rgba(226, 63, 81, 1)',
        line=dict(
            color='rgba(246, 73, 101, 1.0)',
            width=0,
        )
    ),
    dict(
        color='rgba(0, 175, 202, 1)',
        line=dict(
            color='rgba(20, 195, 222, 1.0)',
            width=0,
        )
    ),
]

def group_by_fighter(stats):
    fighters = {}
    for stat in stats:
        fighter = stat[0].split(",")[FIGHTER]
        if fighter not in fighters:
            fighters[fighter] = []
            continue

    for stat_list in stats:
        for stat in stat_list:
            fighter = stat.split(",")[FIGHTER]
            fighters[fighter].append(stat)

    return fighters

def draw_punch_variation(title, stats):
    data = []
    max_y = 0
    i = 0

    punch_type = {
        "Jab": 0,
        "Cross": 0,
        "Lead Hook": 0,
        "Rear Hook": 0,
        "Lead Upper": 0,
        "Rear Upper": 0,
        "Body Jab": 0,
        "Body Cross": 0,
        "Body Lead Hook": 0,
        "Body Rear Hook": 0,
        "Body Lead Upper": 0,
        "Body Rear Upper": 0,
    }

    grouped_stats = group_by_fighter(stats)

    for fighter, fighter_stats in grouped_stats.items():
        labels = []
        values = []

        for stat in fighter_stats:
            parts = stat.split(",")
            punch = parts[PUNCH].title()

            if punch not in punch_type:
                punch_type[punch] = 0

            punch_type[punch] += 1
            max_y = max(max_y, punch_type[punch])

        for key, value in punch_type.items():
            labels.append(key)
            values.append(value)

        data.append(go.Bar(
            y=labels,
            x=values,
            name=fighter,
            marker=colors[i % len(colors)]
        ))

        i = i + 1

    layout = histogram_layout(title, max_y)

    for i, stat in enumerate(data):
        fig = go.Figure(data=[stat], layout=layout)
        plot(fig, filename='graphs/punch-variation-{}.html'.format(i))


def draw_punch_timing(title, stats):
    stacked_bar_data = []
    max_y = 0
    i = 0

    grouped_stats = group_by_fighter(stats)

    for fighter, fighter_stats in grouped_stats.items():
        xs = list(range(0, 180))
        ys = [0] * 181
        name = ''
        actions = {}

        for stat in fighter_stats:
            parts = stat.split(",")
            secs = int(parts[TIME])
            name = parts[FIGHTER]
            if secs not in actions:
                actions[secs] = [0, []]

            actions[secs][1].append(secs)
            actions[secs][0] = actions[secs][0] + 1


        for key, value in actions.items():
            ys[key] = value[0]

        stacked_bar_data.append(go.Bar(
            x=xs,
            y=ys,
            name=name,
            marker=colors[i % len(colors)]
       ))

        i = i + 1

    layout = go.Layout(
            barmode='stack',
            paper_bgcolor='rgba(35, 35, 35, 1)',
            plot_bgcolor='rgba(35, 35, 35, 1)',
            title=title,
            margin=dict(
                t=200,
                l=100,
                r=100,
                b=200),
            font=dict(
                size=32,
                family='Avenir Heavy, sans-serif',
                color='rgb(255, 255, 255)'
            ),
            xaxis=dict(
                        title='PUNCH TIME (SECONDS)',
                        titlefont=dict(
                                        size=18,
                                        family='Avenir, sans-serif',
                                        color='rgb(255, 255, 255)'
                                    ),
                        tickfont=dict(
                                        size=24,
                                        family='Avenir, sans-serif',
                                        color='rgb(255, 255, 255)'
                                    )
                    ),
            yaxis=dict(
                        title='PUNCHES THROWN',
                        titlefont=dict(
                                        size=18,
                                        family='Avenir, sans-serif',
                                        color='rgb(255, 255, 255)'
                                    ),
                        tickfont=dict(
                                        size=24,
                                        family='Avenir, sans-serif',
                                        color='rgb(255, 255, 255)'
                                    )
                    ),
            legend=dict(
                        font=dict(
                            family='Avenir Heavy, sans-serif',
                            size=32,
                            color='#FFF'
                        ),
                        x=0,
                        y=1.0,
                        bgcolor='rgba(255, 255, 255, 0)',
                        bordercolor='rgba(255, 255, 255, 0)'
                    ),
            bargap=0.15,
            bargroupgap=0.1
    )

    fig = go.Figure(data=stacked_bar_data, layout=layout)
    plot(fig, filename='graphs/punch-timing.html')

def histogram_layout(title, max_y):
    layout2 = go.Layout(
        paper_bgcolor='rgba(35, 35, 35, 1)',
        plot_bgcolor='rgba(35, 35, 35, 1)',
        title=title,
        margin=dict(
            t=200,
            l=100,
            r=100,
            b=250),
        font=dict(
            size=32,
            family='Avenir Heavy, sans-serif',
            color='rgb(255, 255, 255)'
        ),
        xaxis=dict(
            titlefont=dict(
                size=18,
                family='Avenir, sans-serif',
                color='rgb(255, 255, 255)'
            ),
            tickfont=dict(
                size=24,
                family='Avenir, sans-serif',
                color='rgb(255, 255, 255)'
            )
        ),
        yaxis=dict(
            title='PUNCHES THROWN',
            titlefont=dict(
                size=18,
                family='Avenir, sans-serif',
                color='rgb(255, 255, 255)'
            ),
            tickfont=dict(
                size=24,
                family='Avenir, sans-serif',
                color='rgb(255, 255, 255)'
            ),
            range=[0, max_y]
        ),
        legend=dict(
            font=dict(
                family='Avenir, sans-serif',
                size=32,
                color='#FFF'
            ),
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        )
    )

def main():
    title = sys.argv[1]
    data = []

    if len(sys.argv) == 3:
        dir = sys.argv[2]
        files = ['{}/{}'.format(dir, f) for f in listdir(dir) if isfile(join(dir, f))]
    else:
        files = sys.argv[2:]

    for filename in files:
        with open(filename) as f:
            lines = f.readlines()
            data.append([x.strip() for x in lines])

    draw_punch_timing(title, data)
    draw_punch_variation(title, data)

if __name__ == "__main__":
      main()
