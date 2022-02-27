from django.conf import settings
from django.db import models

from .managers import BaseInvitationManager


class AbstractBaseInvitation(models.Model):
    accepted = models.BooleanField(verbose_name='accepted', default=False)
    key = models.CharField(verbose_name='key', max_length=64, unique=True)
    sent = models.DateTimeField(verbose_name='sent', null=True)
    inviter = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)  # noqa

    objects = BaseInvitationManager()

    class Meta:
        abstract = True

    @classmethod
    def create(cls, email, inviter=None, **kwargs):
        raise NotImplementedError(
            'You should implement the create method class'
        )

    def key_expired(self):
        raise NotImplementedError(
            'You should implement the key_expired method'
        )

    def send_invitation(self, request, **kwargs):
        raise NotImplementedError(
            'You should implement the send_invitation method'
        )

    def __str__(self):
        raise NotImplementedError(
            'You should implement the __str__ method'
        )
