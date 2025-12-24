from tabulate import tabulate

def print_table(headers, rows):
    print(tabulate(rows, headers=headers, tablefmt="grid"))