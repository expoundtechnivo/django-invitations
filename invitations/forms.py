from django import forms
from django.contrib.auth import get_user_model

from .adapters import get_invitations_adapter
from .exceptions import AlreadyAccepted, AlreadyInvited, UserRegisteredEmail
from .utils import get_invitation_model

Invitation = get_invitation_model()


class CleanEmailMixin(object):

    def validate_invitation(self, email):
        if Invitation.objects.all_valid().filter(
                email__iexact=email, accepted=False):
            raise AlreadyInvited
        elif Invitation.objects.filter(
                email__iexact=email, accepted=True):
            raise AlreadyAccepted
        elif get_user_model().objects.filter(email__iexact=email):
            raise UserRegisteredEmail
        else:
            return True

    def clean_email(self):
        email = self.cleaned_data["email"]
        email = get_invitations_adapter().clean_email(email)

        errors = {
            "already_invited": "This e-mail address has already been"
                                 " invited.",
            "already_accepted": "This e-mail address has already"
                                  " accepted an invite.",
            "email_in_use": "An active user is using this e-mail address",
        }
        try:
            self.validate_invitation(email)
        except(AlreadyInvited):
            raise forms.ValidationError(errors["already_invited"])
        except(AlreadyAccepted):
            raise forms.ValidationError(errors["already_accepted"])
        except(UserRegisteredEmail):
            raise forms.ValidationError(errors["email_in_use"])
        return email


class InviteForm(forms.Form, CleanEmailMixin):

    email = forms.EmailField(
        label="E-mail",
        required=True,
        widget=forms.TextInput(
            attrs={"type": "email", "size": "30"}), initial="")

    def save(self, email):
        return Invitation.create(email=email)


class InvitationAdminAddForm(forms.ModelForm, CleanEmailMixin):
    email = forms.EmailField(
        label="E-mail",
        required=True,
        widget=forms.TextInput(attrs={"type": "email", "size": "30"})
    )

    def save(self, *args, **kwargs):
        cleaned_data = super(InvitationAdminAddForm, self).clean()
        email = cleaned_data.get("email")
        is_employee = cleaned_data.get("is_employee")
        organisation_id = cleaned_data.get("organisation_id")
        params = {
            'email': email,
            'is_employee': is_employee,
            'organisation_id': organisation_id,
        }
        if cleaned_data.get("inviter"):
            params['inviter'] = cleaned_data.get("inviter")
        instance = Invitation.create(**params)
        instance.send_invitation(self.request)
        super(InvitationAdminAddForm, self).save(*args, **kwargs)
        return instance

    class Meta:
        model = Invitation
        fields = ("email", "inviter", "is_employee", "organisation_id")


class InvitationAdminChangeForm(forms.ModelForm):

    class Meta:
        model = Invitation
        fields = '__all__'
