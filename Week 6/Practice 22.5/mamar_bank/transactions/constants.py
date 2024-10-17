DEPOSIT = 1
WITHDRAWAL = 2
LOAN = 3
LOAN_PAID = 4
TRANSFER = 5  # New constant for transfer

TRANSACTION_TYPE = (
    (DEPOSIT, 'Deposit'),
    (WITHDRAWAL, 'Withdrawal'),
    (LOAN, 'Loan'),
    (LOAN_PAID, 'Loan Paid'),
    (TRANSFER, 'Transfer'),  # Add the transfer type here
)
