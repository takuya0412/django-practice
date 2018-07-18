from django import forms
from .models import Friend,Message

class FindForm(forms.Form):
    find=forms.CharField(label="Find",required=False)


class FriendForm(forms.ModelForm):
    class Meta:
        model=Friend
        fields=['name','mail','gender','age','birthday']

class Test1Form(forms.Form):
    name=forms.CharField(label='Name')
    mail=forms.EmailField(label='Email')
    gender=forms.BooleanField(label='Gender',required=False)
    age=forms.IntegerField(label='Age')
    birthday=forms.DateField(label='Birth')
    
class CheckForm(forms.Form):
    str=forms.CharField(label='String')
    
    def clean(self):
        cleaned_data=super().clean()
        str=cleaned_data['str']
        if (str.lower().startswith('no')):
            raise forms.ValidationError('You input "NO"!')
            
class MessageForm(forms.ModelForm):
    class Meta:
        model=Message
        fields=['title','content','friend']