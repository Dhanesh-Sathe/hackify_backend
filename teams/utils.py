from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

def send_team_invitation_email(invitation):
    """
    Send team invitation email
    """
    team = invitation.team
    invited_user = invitation.invited_user
    invited_by = invitation.invited_by
    
    subject = f'Hackify - Team Invitation: {team.name}'
    
    # Render HTML email
    html_message = render_to_string('emails/team_invitation.html', {
        'invited_user_name': invited_user.name,
        'invited_by_name': invited_by.name,
        'invited_by_email': invited_by.email,
        'team_name': team.name,
        'team_description': team.description or 'No description provided',
        'member_count': team.member_count,
        'max_members': team.max_members,
    })
    
    # Plain text fallback
    plain_message = f'''
Hello {invited_user.name},

{invited_by.name} has invited you to join their team "{team.name}" on Hackify!

Team Details:
- Name: {team.name}
- Description: {team.description or 'No description'}
- Current Members: {team.member_count}/{team.max_members}
- Invited By: {invited_by.name} ({invited_by.email})

Log in to your Hackify account to accept or decline this invitation.

Best regards,
The Hackify Team
    '''
    
    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[invited_user.email],
        html_message=html_message,
        fail_silently=False,
    )