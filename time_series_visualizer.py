import matplotlib.pyplot as plt
# import matplotlib as mpl
import pandas as pd
import seaborn as sns
import numpy as np

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv")

df.set_index('date', drop=True, inplace=True)
df.index = [pd.Timestamp(d) for d in df.index]

# Clean data
df = df[(df['value'] >= df['value'].quantile(0.025)) & (
           df['value'] <= df['value'].quantile(0.975))]


def draw_line_plot():
    # Draw line plot

    fig, axs = plt.subplots(1, 1)

    fig.set_figwidth(15)
    fig.set_figheight(5)

    plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')

    plt.xlabel('Date')
    plt.ylabel('Page Views')

    plt.plot(df.index, df['value'], color='r')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():
   
    # Draw bar plot
    leglab = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    labels = [2016, 2017, 2018, 2019]
    months = np.zeros([12, 4])

    for i in range(12):
        for j, year in enumerate(labels):
            t = df[df.index.year == year]
            months[i][j] = t[t.index.month == i].value.mean()

    x = np.arange(len(labels))
    width = 0.7
    fig, ax = plt.subplots()
    fig.set_figwidth(10)
    fig.set_figheight(8)
    for i, month in enumerate(months):
        ax.bar(x - (width * (12 - i) / 12), months[i], width / 12, label=leglab[i])

    ax.set_ylabel("Average Page Views")
    ax.set_xlabel("Years")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend(title='Months')

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig


def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box['date'] = df_box.index
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)

    df_box['smonth'] = [d.strftime('%m') for d in df_box.date]

    df_box = df_box.sort_values(by='smonth')

    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.set_figwidth(20)
    fig.set_figheight(10)

    ax1.set_title("Year-wise Box Plot (Trend)")
    ax2.set_title("Month-wise Box Plot (Seasonality)")

    ax1 = sns.boxplot(x=df_box.year, y=df_box.value, ax=ax1)
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Page Views')

    ax2 = sns.boxplot(x= df_box['month'], y= df_box['value'],  ax=ax2)
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
