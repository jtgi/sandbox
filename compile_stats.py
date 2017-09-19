import sys
import plotly.graph_objs as go

from plotly.offline import plot
from itertools import groupby

TIME = 0
ROUND = 1
FIGHTER = 2
LANDED = 3
PUNCH = 4

colors = [
    dict(
        color='rgba(0, 175, 202, 1)',
        line=dict(
            color='rgba(20, 195, 222, 1.0)',
            width=0,
        )
    ),
    dict(
        color='rgba(226, 63, 81, 1)',
        line=dict(
            color='rgba(246, 73, 101, 1.0)',
            width=0,
        )
    )
]

def draw(stats):
    bar_data = []
    pie_data = []
    i = 0

    for fighter_stats in stats:
        xs = list(range(0, 180))
        ys = [0] * 180
        name = ''
        actions = {}
        punch_type = {
            "jab": 0,
            "cross": 0,
            "lead hook": 0,
            "rear hook": 0,
            "lead upper": 0,
            "rear upper": 0,
            "body jab": 0,
            "body cross": 0,
            "body lead hook": 0,
            "body rear hook": 0,
            "body lead upper": 0,
            "body rear upper": 0,
        }
        pie_labels = []
        pie_values = []

        for stat in fighter_stats:
            parts = stat.split(",")
            time = parts[TIME].split(".")
            secs = int(time[0]) * 60 + int(time[1])
            name = parts[FIGHTER]
            if secs not in actions:
                actions[secs] = [0, []]

            actions[secs][1].append(secs)
            actions[secs][0] = actions[secs][0] + 1

            punch = parts[PUNCH]
            if punch not in punch_type:
                punch_type[punch] = 0

            punch_type[punch] = punch_type[punch] + 1

        for key, value in actions.items():
            ys[key] = value[0]

        for key, value in punch_type.items():
            pie_labels.append(key)
            pie_values.append(value)

        bar_data.append(go.Bar(
            x=xs,
            y=ys,
            name=name,
            marker=colors[i % len(colors)]
       ))

        pie_data.append(go.Bar(
            y=pie_values,
            x=pie_labels,
            name=name,
            marker=colors[i % len(colors)]
        ))

        i = i + 1

    layout = go.Layout(
            barmode='stack',
            paper_bgcolor='rgba(35, 35, 35, 1)',
            plot_bgcolor='rgba(35, 35, 35, 1)',
            title='Punches Thrown By Second - Round 10',
            font=dict(
                size=32,
                family='Avenir, sans-serif',
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
                            family='Avenir, sans-serif',
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

    layout2 = go.Layout(
        paper_bgcolor='rgba(35, 35, 35, 1)',
        plot_bgcolor='rgba(35, 35, 35, 1)',
        title='Punches Thrown By Type - Round 10',
        font=dict(
            size=32,
            family='Avenir, sans-serif',
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
            range=[0, 36]
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

    fig = go.Figure(data=bar_data, layout=layout)
    plot(fig, filename='stacked-bar.html')

    fig = go.Figure(data=[pie_data[0]], layout=layout2)
    plot(fig, filename='pie_1.html')

    fig = go.Figure(data=[pie_data[1]], layout=layout2)
    plot(fig, filename='pie_2.html')

def main():
    files = sys.argv[1:]
    content = []
    for filename in files:
        with open(filename) as f:
            lines = f.readlines()
            content.append([x.strip() for x in lines])
    draw(content)

if __name__ == "__main__":
      main()
