import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg') # Backend for Tkinter

def plot_monthly_summary(rows, username):
    """Draw a bar chart comparing monthly income and expenses."""
    if not rows:
        print("There is no data to plot!")
        return
    
    labels = [f"{r['ReportYear']}/{r['ReportMonth']:02d}" for r in rows]
    income = [float(r['TotalIncome'])  for r in rows]
    expense = [float(r['TotalExpense']) for r in rows]

    x = range(len(labels))
    fig, ax = plt.subplots(figsize = (10, 5))
    ax.bar([i - 0.2 for i in x], income,  width=0.4, label='Income',  color='steelblue')
    ax.bar([i + 0.2 for i in x], expense, width=0.4, label='Expenses', color='tomato')
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45)
    ax.set_title(f'Summary of income and expenses - {username}')
    ax.set_ylabel('$')
    ax.yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, _: f'{x:,.0f}')
    )
    ax.legend()
    plt.tight_layout()
    plt.savefig('monthly_summary.png')
    plt.show()

def plot_category_pie(rows, username):
    """Draw a pie chart showing spending by category."""
    if not rows:
        print("There is no data to plot!")
        return
    
    labels = [r['CategoryName'] for r in rows]
    sizes = [float(r['TotalAmount']) for r in rows]

    fig, ax = plt.subplots(figsize = (7, 7))
    ax.pie(sizes, labels = labels, autopct = '%1.1f%%', startangle = 140)
    ax.set_title(f'Spending by Category - {username}')
    plt.tight_layout()
    plt.savfig('category_spending.png')
    plt.show()

def plot_balance_history(rows, username):
    """Draw a line graph of the balance over time."""
    if not rows:
        return
    
    months = [f"{r['ReportYear']}/{r['ReportMonth']:02d}" for r in rows]
    savings = [float(r['TotalIncome']) - float(r['TotalExpense']) for r in rows]

    # Calculate the accumulated balance
    cumulative = []
    total = 0
    for s in savings:
        total += s
        cumulative.append(total)

    fig, ax = plt.subplots(figsize = (10, 5))
    ax.plot(months, cumulative, marker = '0', color = 'green', linewidth = 2)
    ax.fill_between(range(len(months)), cumulative, alpha = 0.2, color = 'green')
    ax.set_xticklabels(months, rotation = 45)
    ax.set_title(f'The trend of saving and accumulating wealth - {username}')
    ax.set_ylabel('$')
    plt.tight_layout()
    plt.savefig('balance_trend.png')
    plt.show()