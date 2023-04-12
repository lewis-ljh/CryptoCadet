from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone



class CreateNewList(forms.Form):
    name = forms.CharField(label="Name", max_length=200)
    check = forms.BooleanField(required=False)

class DepositWithdrawForm(forms.Form):
    type_choices = (
        ('deposit', 'Deposit'),
        ('withdraw', 'Withdraw'),
    )
    type = forms.ChoiceField(choices=type_choices)
    amount = forms.FloatField()


class DepositForm(forms.Form):
    card_number = forms.CharField(label='Card Number', max_length=16)
    expiry_date = forms.DateField(label='Expiry Date (MM/YY)', input_formats=['%m/%y'])
    cvv = forms.CharField(label='CVV', max_length=3)

    def clean_card_number(self):
        card_number = self.cleaned_data.get('card_number')
        if len(card_number) != 16:
            raise ValidationError('Card number must have 16 digits')
        try:
            digits = [int(c) for c in card_number]
        except ValueError:
            raise ValidationError('Invalid card number')

        # compute check digit using luhn_checksum algorithm
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = 0
        checksum += sum(odd_digits)
        for d in even_digits:
            checksum += sum([int(x) for x in str(d * 2)])
        if checksum % 10 != 0:
            raise ValidationError('Invalid card number')

        return card_number

    def clean_expiry_date(self):
        expiry_date = self.cleaned_data.get('expiry_date')
        if expiry_date < timezone.now().date():
            raise ValidationError('Invalid expiry date')
        return expiry_date

    def clean_cvv(self):
        cvv = self.cleaned_data.get('cvv')
        if not cvv.isnumeric() or len(cvv) != 3:
            raise ValidationError('Invalid CVV')
        return cvv

class WithdrawForm(forms.Form):
    account_owner = forms.CharField(label='Account Owner', max_length=100)
    account_number = forms.CharField(label='Account Number', max_length=8)
    sort_code = forms.CharField(label='Sort Code (XX-XX-XX)', max_length=9)

    def clean_account_number(self):
        account_number = self.cleaned_data.get('account_number')
        if len(account_number) != 8:
            raise ValidationError('Account number must have 8 digits')
        try:
            digits = [int(c) for c in account_number]
        except ValueError:
            raise ValidationError('Invalid account number')
        return account_number

    def clean_sort_code(self):
        sort_code = self.cleaned_data.get('sort_code')
        if len(sort_code) != 8 or sort_code[2] != '-' or sort_code[5] != '-':
            raise ValidationError('Sort code must have the format XX-XX-XX')
        digits = []
        for i in [0, 1, 3, 4, 6, 7]:
            try:
                digits.append(int(sort_code[i]))
            except ValueError:
                raise ValidationError('Invalid sort code')
        if digits[0] not in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
            raise ValidationError('First digit of sort code must be between 0 and 9')
        if digits[1] not in [0, 1, 2, 3, 4, 5, 6, 7]:
            raise ValidationError('Second digit of sort code must be between 0 and 7')
        if digits[2] not in [0, 1, 2]:
            raise ValidationError('Third digit of sort code must be between 0 and 2')
        if digits[3] not in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
            raise ValidationError('Fourth digit of sort code must be between 0 and 9')
        if digits[4] not in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
            raise ValidationError('Fifth digit of sort code must be between 0 and 9')
        if digits[5] not in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
            raise ValidationError('Sixth digit of sort code must be between 0 and 9')
        return sort_code


