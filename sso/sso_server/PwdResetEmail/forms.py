from django import forms

class EmailVerificationForm(forms.Form):
    student_id = forms.CharField(label="학번/교직원번호", max_length=20)
    name = forms.CharField(label="성명", max_length=50)
    code = forms.CharField(label="인증번호", max_length=6, required=False)