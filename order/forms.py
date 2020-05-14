from django import forms


class RefundTxnidForm(forms.Form):
    txn_id = forms.CharField(max_length=1000)
