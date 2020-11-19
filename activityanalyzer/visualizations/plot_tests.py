import seaborn as sns
import pandas as pd

import matplotlib.pyplot as plt


def plot_balances(df: pd.DataFrame):
    with sns.plotting_context('notebook', font_scale=1.6):
        fig, ax = plt.subplots(1)
        fig.set_size_inches(24, 12)

        sns.lineplot(data=df, x="date", y="amount", ax=ax)
        ax.set_title('Balances', fontsize=28, pad=20)

        fig.savefig(f"plots/balances.png", bbox_inches='tight', dpi=200)
        plt.show()


def plot_beneficiaries(df, title):

    with sns.plotting_context('notebook', font_scale=1.6):
        fig, ax = plt.subplots(1)
        fig.set_size_inches(12, 16)
        dfi = df.set_index('principal_beneficiary')
        sns.heatmap(dfi[['amount']], annot=True, square=False, xticklabels=True, yticklabels=True, fmt='.2f', ax=ax)
        ax.set_title(title, fontsize=28, pad=20)
        ax.set_xlabel('')
        ax.set_ylabel('')
        fig.savefig(f"plots/{title.lower()}_heatmap.png", bbox_inches='tight', dpi=200)
        plt.show()

        fig, ax = plt.subplots(1)
        fig.set_size_inches(12, 16)
        sns.barplot(x='amount', y='principal_beneficiary', data=df, palette='Spectral', ax=ax)
        ax.set_title(title, fontsize=28, pad=20)
        ax.set_xlabel('')
        ax.set_ylabel('')
        fig.savefig(f"plots/{title.lower()}_barplot.png", bbox_inches='tight', dpi=200)
        plt.show()
