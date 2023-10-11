from django import forms

from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ["post"]
        labels = {
            "user_name": "Your Name",
            "user_email": "Your Email",
            "text": "Your Comment"
        }

        # def clean(self):
 
        #     # data from the form is fetched using super function
        #     super(CommentForm, self).clean()
            
        #     # extract the username and text field from the data
        #     user_name = self.cleaned_data.get('username')
        #     text = self.cleaned_data.get('text')
    
        #     # conditions to be met for the username length
        #     if len(user_name) < 5:
        #         self._errors['user_name'] = self.error_class([
        #             'Minimum 5 characters required'])
        #     if len(text) <10:
        #         self._errors['text'] = self.error_class([
        #             'Post Should Contain a minimum of 10 characters'])
    
        #     # return any errors if found
        #     return self.cleaned_data