"""File where generate the unique token for email confirm."""
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from students.models import Student

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    """Class generate unique token.
    
    Arguments:
        PasswordResetTokenGenerator: superclass which
        generate and check tokens for the password
        reset mechanism.

    """
    def _make_hash_value(self, user, timestamp):
        """Make a hash from values.

        Override the superclass function.

        Arguments:
            user: token generated for this
            student: token generated for this too

        Returns:
            token (str): unique token
        """
        student = Student.objects.get(user=user)
        return (
            str(user.pk) + str(timestamp) + 
            str(student.signup_confirmation)
        )

account_activation_token = AccountActivationTokenGenerator()
