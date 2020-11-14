import os
import re
import pandas as pd

from activityanalyzer.CsvInterpreter import CsvInterpreter
from activityanalyzer.visualizations.plot_balances import plot_balances

from activityanalyzer.pie_chart import pie_chart


if __name__ == '__main__':
    directory = '../data'
    csv_files = [os.path.join(directory, file) for file in os.listdir(directory) if re.match(r'.+\.csv$', file)]
    yaml_file = 'DeutscheKreditbank.yaml'

    interpreter = CsvInterpreter(csv_files, yaml_file)
    b = interpreter.get_balances()
    t = interpreter.get_transactions()
    x = interpreter.get_expenses()
    e = interpreter.get_earnings()

    # https://www.dataquest.io/blog/tutorial-time-series-analysis-with-pandas/

    df_balances = pd.DataFrame()

    plot_balances(df_balances)

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
