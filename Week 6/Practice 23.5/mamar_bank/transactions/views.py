from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.http import HttpResponse
from django.views.generic import CreateView, ListView
from transactions.constants import DEPOSIT, WITHDRAWAL,LOAN, LOAN_PAID, TRANSFER
from datetime import datetime
from django.db.models import Sum
from django.views import View
from accounts.models import UserBankAccount
from transactions.forms import TransferForm
from transactions.forms import (
    DepositForm,
    WithdrawForm,
    LoanRequestForm,
)
from transactions.models import Transaction
from accounts.models import UserBankAccount
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string


def transaction_email(user, amount, subject):
    message = render_to_string(
        "transactions/transaction_mail.html",
        {
            "user": user,
            "amount": amount,
            "operation": subject,
        },
    )
    to_email = [user.email]
    if isinstance(message, tuple):
        message = "".join(message)
    send_email = EmailMultiAlternatives(subject=subject, body="", to=to_email)
    send_email.attach_alternative(message, "text/html")
    send_email.send()


def loan_approved_email(user, amount, subject):
    message = render_to_string(
        "transactions/loanstatus.html",
        {
            "user": user,
            "amount": amount,
            "operation": subject,
        },
    )
    to_email = [user.email]
    if isinstance(message, tuple):
        message = "".join(message)
    send_email = EmailMultiAlternatives(subject=subject, body="", to=to_email)
    send_email.attach_alternative(message, "text/html")
    send_email.send()

class TransactionCreateMixin(LoginRequiredMixin, CreateView):
    template_name = 'transactions/transaction_form.html'
    model = Transaction
    title = ''
    success_url = reverse_lazy('transaction_report')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'account': self.request.user.account
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title
        })

        return context


class DepositMoneyView(TransactionCreateMixin):
    form_class = DepositForm
    title = 'Deposit'

    def get_initial(self):
        initial = {'transaction_type': DEPOSIT}
        return initial

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.account
        # if not account.initial_deposit_date:
        #     now = timezone.now()
        #     account.initial_deposit_date = now
        account.balance += amount
        account.save(
            update_fields=[
                'balance'
            ]
        )

        messages.success(
            self.request,
            f'{"{:,.2f}".format(float(amount))}$ was deposited to your account successfully'
        )
        transaction_email(self.request.user, amount, self.title)
        return super().form_valid(form)


from bank.models import BankModel  # Import the BankModel

class WithdrawMoneyView(TransactionCreateMixin):
    form_class = WithdrawForm
    title = 'Withdraw Money'

    def get_initial(self):
        initial = {'transaction_type': WITHDRAWAL}
        return initial

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')

        # Check if the bank is bankrupt
        bank_status = BankModel.objects.first()  # Assuming there's only one BankModel instance
        if bank_status and bank_status.is_bankrupt:
            messages.error(
                self.request,
                "The bank is currently bankrupt. Withdrawal is not allowed."
            )
            return redirect('withdraw_money')  # Redirect to the withdrawal page or appropriate page

        # Proceed with withdrawal if the bank is not bankrupt
        self.request.user.account.balance -= amount
        self.request.user.account.save(update_fields=['balance'])

        messages.success(
            self.request,
            f'Successfully withdrawn {"{:,.2f}".format(float(amount))}$ from your account'
        )
        transaction_email(self.request.user, amount, self.title)
        return super().form_valid(form)


class LoanRequestView(TransactionCreateMixin):
    form_class = LoanRequestForm
    title = 'Request For Loan'

    def get_initial(self):
        initial = {'transaction_type': LOAN}
        return initial

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        current_loan_count = Transaction.objects.filter(
            account=self.request.user.account,transaction_type=3,loan_approve=True).count()
        if current_loan_count >= 3:
            return HttpResponse("You have cross the loan limits")
        messages.success(
            self.request,
            f'Loan request for {"{:,.2f}".format(float(amount))}$ submitted successfully'
        )
        transaction_email(self.request.user, amount, self.title)
        return super().form_valid(form)
    
class TransactionReportView(LoginRequiredMixin, ListView):
    template_name = 'transactions/transaction_report.html'
    model = Transaction
    balance = 0 # filter korar pore ba age amar total balance ke show korbe
    
    def get_queryset(self):
        queryset = super().get_queryset().filter(
            account=self.request.user.account
        )
        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')
        
        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            
            queryset = queryset.filter(timestamp__date__gte=start_date, timestamp__date__lte=end_date)
            self.balance = Transaction.objects.filter(
                timestamp__date__gte=start_date, timestamp__date__lte=end_date
            ).aggregate(Sum('amount'))['amount__sum']
        else:
            self.balance = self.request.user.account.balance
       
        return queryset.distinct() # unique queryset hote hobe
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'account': self.request.user.account
        })

        return context
    
        
class PayLoanView(LoginRequiredMixin, View):
    def get(self, request, loan_id):
        loan = get_object_or_404(Transaction, id=loan_id)
        print(loan)
        if loan.loan_approve:
            user_account = loan.account
                # Reduce the loan amount from the user's balance
                # 5000, 500 + 5000 = 5500
                # balance = 3000, loan = 5000
            if loan.amount < user_account.balance:
                user_account.balance -= loan.amount
                loan.balance_after_transaction = user_account.balance
                user_account.save()
                loan.loan_approved = True
                loan.transaction_type = LOAN_PAID
                loan.save()
                return redirect('transactions:loan_list')
            else:
                messages.error(
            self.request,
            f'Loan amount is greater than available balance'
        )

        return redirect('loan_list')


class LoanListView(LoginRequiredMixin,ListView):
    model = Transaction
    template_name = 'transactions/loan_request.html'
    context_object_name = 'loans' # loan list ta ei loans context er moddhe thakbe
    
    def get_queryset(self):
        user_account = self.request.user.account
        queryset = Transaction.objects.filter(account=user_account,transaction_type=3)
        print(queryset)
        return queryset

from django.db import transaction 
from decimal import Decimal,InvalidOperation
    
class TransferAmountView(View):
    template_name = 'transactions/transfer_amount.html'
    title = 'Money'
    def get(self, request):
        return render(request, self.template_name, {'title': 'Transfer Amount'})

    def post(self, request):
        sender_account = request.user.account
        recipient_account_no = request.POST.get('recipient_account_no')
        amount = request.POST.get('amount')

        try:
            amount = Decimal(amount)
        except Exception:
            messages.error(request, 'Invalid amount.')
            return redirect('transfer')

        if amount <= 0:
            messages.error(request, 'Amount must be greater than zero.')
            return redirect('transfer')

        if sender_account.balance < amount:
            messages.error(request, 'Insufficient balance.')
            return redirect('transfer')

        try:
            recipient_account = UserBankAccount.objects.get(account_no=recipient_account_no)
        except UserBankAccount.DoesNotExist:
            messages.error(request, 'Recipient account not found.')
            return redirect('transfer')

        try:
            with transaction.atomic():
                sender_account.balance -= amount
                recipient_account.balance += amount
                sender_account.save()
                recipient_account.save()

                Transaction.objects.create(
                    account=sender_account,
                    amount=-amount,
                    balance_after_transaction=sender_account.balance,
                    transaction_type=TRANSFER
                )
                Transaction.objects.create(
                    account=recipient_account,
                    amount=amount,
                    balance_after_transaction=recipient_account.balance,
                    transaction_type=TRANSFER
                )

            messages.success(request, f'Successfully transferred {amount} to account {recipient_account_no}.')
            transaction_email(self.request.user, amount, self.title)
            transaction_email(recipient_account.user, amount, self.title)
            return redirect('transfer')
        except Exception as e:
            messages.error(request, f'Error processing transfer: {str(e)}')
            return redirect('transfer')