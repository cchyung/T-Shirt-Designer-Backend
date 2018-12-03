from django.core.mail import EmailMultiAlternatives

from django.template.loader import render_to_string
from django.utils.html import strip_tags
from tshirtpricetool.settings.base import get_env_variable
from api import models


def send_report(style_id, quantities, ink_colors, addon_ids, email, name, comments, price, front_image, back_image):
    from_email = "Kastlfel <" + get_env_variable('EMAIL_REPORT_FROM') + ">"
    to_emails = [get_env_variable('EMAIL_REPORT_RECIPIENT'), email]
    email_subject = get_env_variable('EMAIL_REPORT_SUBJECT')

    style = models.Style.objects.get(style_id=style_id)

    addons = [models.Addon.objects.get(id=i).name for i in addon_ids]

    template_vars = {
        'email': email,
        'name': name,
        'style': style.__str__(),
        'brand': style.brand,
        'quantities': quantities,
        'ink_colors': ink_colors,
        'addons': addons if len(addons) > 0 else 'No Addons',
        'comments': comments,
        'price': price,
        'front_image': front_image.__str__(),
        'back_image': back_image.__str__(),
    }

    html_content = render_to_string('api/report_email.html', template_vars).replace("\n", "")
    text_content = strip_tags(html_content)

    msg = EmailMultiAlternatives(email_subject, text_content, from_email, to_emails)

    # embed images
    # front_email_image = decode_image(front_image)
    # front_email_image.add_header('Content-ID', '<front>')
    # back_email_image = decode_image(back_image)
    # back_email_image.add_header('Content-ID', '<back>')
    # msg.attach(front_email_image)
    # msg.attach(back_email_image)

    msg.mixed_subtype = 'related'
    msg.attach_alternative(html_content, 'text/html')

    msg.send()

