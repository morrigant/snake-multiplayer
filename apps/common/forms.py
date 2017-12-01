from django import forms


class NameForm(forms.Form):
	name = forms.CharField(label="Choose your username", max_length=40, widget=forms.TextInput(attrs={'class':'input_name'}))

class ChannelForm(forms.Form):
	room_id = forms.IntegerField()
	key = forms.CharField(max_length=34)
	action = forms.IntegerField() # 0 - get info; 1 - snake to top; 2 - snake to right; 3 - snake to bottom; 4 - snake to left;
