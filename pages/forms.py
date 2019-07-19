from django import forms

from .models import QF

class InputForm_g2b( forms.ModelForm):
	Your_Email_id 				= forms.CharField(initial = 'xyz@gmail.com')
	
	Address						= forms.CharField(
									required = False ,
									initial = 'Room No 116, Hall 6, NIT Durgapur',
									widget = forms.Textarea
										(
										attrs={
											"placeholder": "Enter your Address here ",
											"class" : "new-class-name two",
											"id" :"my-id-for-textarea",
											"rows":10,
											"cols":100
											}
										) )
	Name_of_Generic_Medicine 	= forms.CharField(
									widget=forms.TextInput(attrs={"placeholder" : "Enter the generic name here"}),
									initial='paracetamol',
									)
	

	
	class Meta:
		model = QF
		fields = [
			'Your_Email_id',
			'Address',
			'Name_of_Generic_Medicine'
		]



class InputForm_b2g( forms.ModelForm):
	Your_Email_id 				= forms.CharField(initial = 'xyz@gmail.com')
	
	Address						= forms.CharField(
									required = False ,
									initial = 'Room No 116, Hall 6, NIT Durgapur',
									widget = forms.Textarea
										(
										attrs={
											"placeholder": "Enter your Address here ",
											"class" : "new-class-name two",
											"id" :"my-id-for-textarea",
											"rows":10,
											"cols":100
											}
										) )
	Name_of_Brand_Medicine 	= forms.CharField(
									widget=forms.TextInput(attrs={"placeholder" : "Enter the brand name here"}),
									initial='NORDREN',
									)
	

	
	class Meta:
		model = QF
		fields = [
			'Your_Email_id',
			'Address',
			'Name_of_Brand_Medicine'
		]

