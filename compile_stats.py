import sys
import plotly.plotly as py
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

darker_colors = [
    dict(
        color='#a72b39',
        line=dict(
            color='#b4303f',
            width=0,
        )
    ),
    dict(
        color='#008ca1',
        line=dict(
            color='#018599',
            width=0,
        )
    )
]


colors = [
    dict(
        color='#e23f51',
        line=dict(
            color='#d33c4d',
            width=0,
        )
    ),
    dict(
        color='#00afca',
        line=dict(
            color='#02a8c2',
            width=0,
        )
    )
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

def draw_punch_variation(title, stats, rounds, landed_only):
    data = []
    max_y = 0
    i = 0

    grouped_stats = group_by_fighter(stats)

    for fighter, fighter_stats in grouped_stats.items():
        labels = []
        values = []
        punch_type = punch_map()

        for stat in fighter_stats:
            parts = stat.split(",")
            punch = parts[PUNCH].title()

            if not landed_only or (landed_only and parts[LANDED] == '1'):
                punch_type[punch] += 1
                max_y = max(max_y, punch_type[punch])

        for key, value in punch_type.items():
            labels.append(key)
            values.append(value)

        data.append(go.Bar(
            y=values,
            x=labels,
            name=fighter,
            marker=colors[i % len(colors)]
        ))

        i = i + 1

    graph_title = pretty_rounds(rounds)
    graph_title += ' - Landed Punches' if landed_only else ' - Thrown Punches'
    layout = histogram_layout(graph_title, max_y)

    for i, stat in enumerate(data):
        fig = go.Figure(data=data, layout=layout)
        filename = 'punch-variation-{}-{}-{}'.format('landed' if landed_only else 'thrown', i, "-".join(rounds))
        plot(fig, filename='graphs/{}.html'.format(filename))

def punch_map():
    return {
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

def draw_punch_pie(title, stats, rounds, landed_only):
    i = 0
    grouped_stats = group_by_fighter(stats)

    for fighter, fighter_stats in grouped_stats.items():
        head = 0
        body = 0
        data = []

        for stat in fighter_stats:
            parts = stat.split(",")
            round = parts[ROUND]
            punch = parts[PUNCH]

            if not landed_only or (landed_only and parts[LANDED] == '1'):
                if "body" in punch:
                    body += 1
                else:
                    head +=1

        cs = [colors[i % len(colors)]['color'], darker_colors[i % len(colors)]['color']]

        data.append(go.Pie(
            labels=['Head', 'Body'],
            values=[head, body],
            hoverinfo='label+percent',
            textinfo='label+value+percent',
            marker=dict(
                colors=cs
            )
        ))

        graph_title = "{} - {} - Head vs Body".format(pretty_rounds(rounds), "Landed" if landed_only else "Thrown")
        fig = go.Figure(data=data, layout=pie_layout(graph_title))
        plot(fig, filename='graphs/{}-punch-pie-{}-{}.html'.format(fighter, landed_only, "-".join(rounds)))

        i += 1

def draw_punch_timing(title, stats, rounds):
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

            if i % 2 == 0:
                actions[secs][0] += 1
            else:
                actions[secs][0] -= 1

        for key, value in actions.items():
            ys[key] = value[0]

        stacked_bar_data.append(go.Bar(
            x=xs,
            y=ys,
            name=name,
            marker=colors[i % len(colors)]
       ))

        i = i + 1

        graph_title = "{} - Punch Output".format(pretty_rounds(rounds))

        if title:
            graph_title + ' - ' + title

        layout = bar_layout(graph_title, 'Punch Time (seconds)', 'Punch Count')
        fig = go.Figure(data=stacked_bar_data, layout=layout)
        plot(fig, filename='graphs/punch-timing-{}.html'.format("-".join(rounds)))

def bar_layout(title, x_label, y_label):
    return go.Layout(
            barmode='relative',
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
                        title=x_label,
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
                        title=y_label,
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
                        y=1.25,
                        bgcolor='rgba(255, 255, 255, 0)',
                        bordercolor='rgba(255, 255, 255, 0)'
                    ),
            bargap=0.15,
            bargroupgap=0.1
    )

def work_rate(stats, rounds):
    grouped_stats = group_by_fighter(stats)

    for fighter, fighter_stats in grouped_stats.items():
        round_rate = len(fighter_stats) / len(rounds)
        second_rate = len(fighter_stats) / (len(rounds) * 180)
        print "{} {}ppr {}pps".format(fighter, round_rate, second_rate)

def histogram_layout(title, max_y):
    return go.Layout(
        width=1680,
        height=1050,
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
                family='Avenir Heavy, sans-serif',
                size=32,
                color='#FFF'
            ),
            x=0,
            y=1.25,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        )
    )

def pie_layout(title):
    return go.Layout(
            paper_bgcolor='rgba(35, 35, 35, 1)',
            plot_bgcolor='rgba(35, 35, 35, 1)',
            title=title,
            margin=dict(
                t=300,
                l=100,
                r=100,
                b=200),
            font=dict(
                size=32,
                family='Avenir Heavy, sans-serif',
                color='rgb(255, 255, 255)'
            ),
            legend=dict(
                        font=dict(
                            family='Avenir Heavy, sans-serif',
                            size=32,
                            color='#FFF'
                        ),
                        x=0,
                        y=1.25,
                        bgcolor='rgba(255, 255, 255, 0)',
                        bordercolor='rgba(255, 255, 255, 0)'
                    )
    )

def get_rounds(stats):
    rounds = set()

    grouped_stats = group_by_fighter(stats)

    for fighter, fighter_stats in grouped_stats.items():
        for stat in fighter_stats:
            parts = stat.split(",")
            rounds.add(parts[ROUND])

    return rounds

def pretty_rounds(rounds):
    if len(rounds) == 1:
        return "Round {}".format("".join(rounds))
    elif len(rounds) == 12:
        return "All Rounds"
    else:
        return "Rounds {}".format(", ".join(rounds))

def main():
    data = []
    title = sys.argv[1]

    if len(sys.argv) == 3:
        dir = sys.argv[2]
        files = ['{}/{}'.format(dir, f) for f in listdir(dir) if isfile(join(dir, f))]
    else:
        files = sys.argv[2:]

    for filename in files:
        with open(filename) as f:
            lines = f.readlines()
            data.append([x.strip() for x in lines])

    rounds = get_rounds(data)
    draw_punch_timing(title, data, rounds)
    draw_punch_variation(title, data, rounds, False)
    draw_punch_variation(title, data, rounds, True)
    draw_punch_pie(title, data, rounds, False)
    draw_punch_pie(title, data, rounds, True)
    work_rate(data, rounds)

if __name__ == "__main__":
      main()
