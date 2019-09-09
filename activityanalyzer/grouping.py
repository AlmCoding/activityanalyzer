from activityanalyzer.CsvInterpreter import CsvInterpreter
from activityanalyzer.pie_chart import pie_chart


if __name__ == '__main__':
    csv_files = '../data/dkb_2018.csv', '../data/dkb_2019.csv', 'nudes.png'
    yaml_file = 'DeutscheKreditbank.yaml'

    interpreter = CsvInterpreter(csv_files, yaml_file)
    transactions = interpreter.transactions

    a = len(transactions)

    for t in transactions:
        t.print()

    beneficiaries = {}
    for transaction in interpreter.transactions:
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
