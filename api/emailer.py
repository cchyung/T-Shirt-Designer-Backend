from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from tshirtpricetool.settings.base import get_env_variable
from api import models


def send_report(style_id, quantities, ink_colors, addon_ids, email, comments, price):
    from_email = get_env_variable('EMAIL_REPORT_FROM')
    to_emails = [get_env_variable('EMAIL_REPORT_RECIPIENT')]

    style = models.Style.objects.get(style_id=style_id)

    addons = [models.Addon.objects.get(i).name for i in addon_ids]

    template_vars = {
        'email': email,
        'style': style.__str__(),
        'brand': style.brand,
        'quantities': quantities,
        'ink_colors': ink_colors,
        'addons': addons if len(addons) > 0 else 'No Addons',
        'comments': comments,
        'price': price
    }

    html_content = render_to_string('api/report_email.html', template_vars).replace("\n", "")
    text_content = strip_tags(html_content)

    msg = EmailMultiAlternatives('Report from T Shirt Designer', text_content, from_email, to_emails)
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
