import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv")
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
df = df.set_index(pd.DatetimeIndex(df['date']))

# Clean data
df = df.loc[
    (df["value"] >= df["value"].quantile(0.025)) &
    (df["value"] <= df["value"].quantile(0.975))
]


def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(15, 5))

    plt.plot(df.index, df["value"], color="red")

    startDate = str("{:%#m/%Y}".format(df["date"][0]))
    endDate = str("{:%m/%Y}".format(df["date"][len(df["date"])-1]))
    plt.title(
        f"Daily freeCodeCamp Forum Page Views {startDate}-{endDate}")
    plt.xlabel("Date")
    plt.ylabel("Page Views")
    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.groupby(pd.Grouper(freq="M")).mean()
    df_bar["year"] = df_bar.index.map(lambda x: x.strftime('%Y'))
    df_bar['month'] = df_bar.index.map(lambda x: x.strftime('%B'))
    months_order = ['January', 'February', 'March', 'April', 'May', 'June',
                    'July', 'August', 'September', 'October', 'November', 'December']
    # Draw bar plot
    fig, ax = plt.subplots(figsize=(10, 10))

    sns.barplot(x="year", y="value", hue="month",
                hue_order=months_order, data=df_bar, palette="bright")

    plt.xlabel("Years")
    plt.ylabel("Average Page Views")
    plt.xticks(rotation=90)
    plt.legend(loc="upper left")

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig


def draw_box_plot():
    # Prepare data for box plots (this part is done!) (modified the reset_index with drop=True)
    df_box = df.copy()
    df_box.reset_index(inplace=True, drop=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    monthOrder = ['Jan', 'Feb', 'Mar', 'Apr', 'May',
                  'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    # Draw box plots (using Seaborn)
    fig, ax = plt.subplots(ncols=2, figsize=(25, 10))
    sns.boxplot(x="year", y="value", data=df_box, ax=ax[0])
    ax[0].set_xlabel("Year")
    ax[0].set_ylabel("Page Views")
    ax[0].set_title("Year-wise Box Plot (Trend)")

    sns.boxplot(x="month", y="value", data=df_box, ax=ax[1], order=monthOrder)
    ax[1].set_xlabel("Month")
    ax[1].set_ylabel("Page Views")
    ax[1].set_title("Month-wise Box Plot (Seasonality)")

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
