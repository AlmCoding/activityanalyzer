import os
import re
import pandas as pd

from activityanalyzer.CsvInterpreter import CsvInterpreter
from activityanalyzer.visualizations.plot_tests import plot_balances, plot_beneficiaries
from activityanalyzer.pie_chart import pie_chart


# https://www.dataquest.io/blog/tutorial-time-series-analysis-with-pandas/


if __name__ == '__main__':
    directory = 'data'
    csv_files = [os.path.join(directory, file) for file in os.listdir(directory) if re.match(r'.+\.csv$', file)]
    yaml_file = 'activityanalyzer/DeutscheKreditbank.yaml'

    a = os.listdir()

    interpreter = CsvInterpreter(csv_files, yaml_file)
    b = interpreter.get_balances()
    t = interpreter.get_transactions()
    x = interpreter.get_expenses()
    e = interpreter.get_earnings()

    def analyze_beneficiaries(df: pd.DataFrame, ascending: bool):
        collection = {}
        for index, row in df.iterrows():
            beneficiary = row['principal_beneficiary'].split('/')[0]
            amount = row['amount']
            if beneficiary in collection.keys():
                collection[beneficiary] += amount
            else:
                collection[beneficiary] = amount

        total_amount = sum(collection.values())
        ratios = [amount/total_amount for amount in collection.values()]

        df = pd.DataFrame({'principal_beneficiary': list(collection.keys()),
                           'amount': list(collection.values()),
                           'ratio': ratios})
        df = df.sort_values(['amount'], ascending=ascending)
        df = df.reset_index(drop=True)
        return df

    def merge_beneficiaries(df: pd.DataFrame, max_beneficiaries=30):
        cnt = len(df) - max_beneficiaries
        while len(df) > max_beneficiaries:
            df.loc[df.index[-2], 'principal_beneficiary'] = f'Others ({cnt})'
            df.loc[df.index[-2], 'amount'] += df.loc[df.index[-1], 'amount']
            df.loc[df.index[-2], 'ratio'] += df.loc[df.index[-1], 'ratio']
            df = df.drop(df.index[-1])
        return df

    beneficiaries_expenses = merge_beneficiaries(analyze_beneficiaries(x, ascending=True))
    beneficiaries_earnings = merge_beneficiaries(analyze_beneficiaries(e, ascending=False))

    plot_beneficiaries(beneficiaries_expenses, title='Expenses')
    plot_beneficiaries(beneficiaries_earnings, title='Earnings')

    plot_balances(b)

    exit(0)

    for tt in e:
        tt.print()

    beneficiaries = {}
    for transaction in t:
        if transaction.principal_beneficiary not in beneficiaries.keys():
            beneficiaries[transaction.principal_beneficiary] = 0.0
        beneficiaries[transaction.principal_beneficiary] += transaction.amount

    lst = []
    for key, value in beneficiaries.items():
        lst.append((key, value))
    lst = list(sorted(lst, key=lambda x: x[1], reverse=True))

    earnings = [item for item in lst if item[1] > 0]
    expenses = [item for item in lst if item[1] < 0]

    pie_chart(earnings, "Earnings")
    pie_chart(expenses, "Expenses", min_percentage=2.0)

    for i in lst:
        s = "{:100}: {}".format(i[0], i[1])
        print(s)
