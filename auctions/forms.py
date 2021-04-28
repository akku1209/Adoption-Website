from django import forms
from django.forms import ModelForm, TextInput, PasswordInput, Textarea, \
    Select, NumberInput

from .models import Listing, Comment, Bid, User, Article_list


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['headline', 'description']
        widgets = {
            'headline': TextInput(attrs={
                'class': 'form-control mb-2',
                'placeholder': 'Headline'
            }),
            'description': Textarea(attrs={
                'class': 'form-control mb-2',
                'placeholder': 'Your comments'
            })
        }


class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['bid']
        widgets = {
            'bid': NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Bid here.'}
            )
        }

    def __init__(self, *args, **kwargs):
        """
        Constructor that looks for top_bid and min_bid
        values needed when validating new bid entered on this form.
        """
        if kwargs:
            self.top_bid = kwargs.pop('top_bid')
            self.min_bid = kwargs.pop('min_bid')
        super(BidForm, self).__init__(*args, **kwargs)

    def clean_bid(self):
        """
        Custom validator to make sure the bid entered
        is greater than or equal to the listings minimum bid and
        larger than the current top bid.
        """
        new_bid = int(self.cleaned_data['bid'])
        top_bid = int(self.top_bid)
        min_bid = int(self.min_bid)
        if new_bid < 0:
            raise forms.ValidationError(
                f"Days cannot be less 0."
            )
        if new_bid < top_bid or new_bid == top_bid:
            raise forms.ValidationError(
                "Number of days have to be greater than the Option available.")

        if new_bid < min_bid:
            raise forms.ValidationError(
                "Number of days have to be greater than or equal to the Option available."
            )
        return new_bid


class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['image_url', 'headline', 'description', 'category',
                  'min_bid','breed', 'age', 'weight', 'gender' , 'city', 'contact']
        widgets = {
            'image_url': TextInput(attrs={
                'class': 'form-control mb-2',
                'placeholder': 'Image url'}
            ),
            'headline': TextInput(attrs={
                'class': 'form-control mb-2',
                'placeholder': 'Headline'}
            ),
            'breed':  TextInput(attrs={
                'class': 'form-control mb-2',
                'placeholder': 'Breed'}
            ),
            'weight': TextInput(attrs={
                'class': 'form-control mb-2',
                'placeholder': 'Weight'}
            ),
            'age': TextInput(attrs={
                'class': 'form-control mb-2',
                'placeholder': 'Age'}
            ),
            'gender': Select(choices=Listing.GENDER_CHOICES, attrs={
                'class': 'form-control'}
            ),
            'description': Textarea(attrs={
                'class': 'form-control mb-2',
                'placeholder': 'Description (required)'}
            ),
            'category': Select(choices=Listing.CATEGORY_CHOICES, attrs={
                'class': 'form-control'}
            ),
            'city': Select(choices=Listing.CITY_CHOICES, attrs={
                'class': 'form-control'}
            ),
            'contact': TextInput(attrs={
                'class': 'form-control mb-2',
                'placeholder': 'Contact'}
            ),
            'min_bid': NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Minimum Bid '}
            )
        }
        labels = {'image_url': '', 'headline': '', 'description': '',
                  'min_bid': 'Minimum Bid', 'category': '', 'weight': '', 'breed': '', 'age': '', 'gender':'', 'city':'', 'contact':''}
        help_texts = {'headline': '', 'description': '', 'min_bid': '', 'weight': '', 'age': '', 'breed':'', 'contact': ''}


class RegisterForm(ModelForm):
    confirm_password = forms.CharField(
        label='',
        help_text='',
        required=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control mb-2',
                'placeholder': 'Confirm Password'}
        )
    )


    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': TextInput(attrs={
                'class': 'form-control mb-2',
                'placeholder': 'Username'}
            ),
            'email': TextInput(attrs={
                'class': 'form-control mb-2',
                'placeholder': 'Email'}
            ),
            'password': PasswordInput(attrs={
                'class': 'form-control mb-2',
                'placeholder': 'Password'}
            )

        }
        labels = {'username': '', 'email': '', 'password': ''}
        help_texts = {'username': '', 'password': ''}

    def clean(self):
        """
        Custom validator ensuring the entered password
        and confirm password values match.
        """
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError(
                "The passwords entered do not match."
            )

class ArticleForm(ModelForm):
    class Meta:
        model = Article_list
        fields = ['id', 'category', 'headline', 'link']
        widgets = {
            'link': TextInput(attrs={
                'class': 'form-control mb-2',
                'placeholder': 'Link'}
            ),
            'headline': TextInput(attrs={
                'class': 'form-control mb-2',
                'placeholder': 'Headline'}
            ),
            'category':  TextInput(attrs={
                'class': 'form-control mb-2',
                'placeholder': 'Category'}
            ),
            'id': TextInput(attrs={
                'class': 'form-control mb-2',
                'placeholder': 'Id'}
            )
        }
        labels = {'id':'', 'category':'', 'headline':'', 'link':''}
        help_texts = {'id':'', 'category':'', 'headline':'', 'link':''}

