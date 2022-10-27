from io import BytesIO

from django.db.models import Sum
from django.http import FileResponse

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


def get_pdf(request, model):
    """Получение файла PDF."""
    font = 'arial'
    pdfmetrics.registerFont(
        TTFont(
            'arial',
            'arial.ttf',
            'UTF-8'
        )
    )
    font_size_title = 24
    font_size_text = 14
    pixels_from_top_title = 150
    pixels_from_down_title = 800
    pixels_from_left_text = 50
    pixels_from_bottom_text_str = 700
    pixels_subtraction = 20

    buffer = BytesIO()
    buffer_seek_count = 0
    pdf = canvas.Canvas(buffer)
    pdf.setFont(font, font_size_title)
    pdf.drawString(
        pixels_from_top_title,
        pixels_from_down_title,
        'Shopping list'
    )
    pdf.setFont(font, font_size_text)

    user = request.user
    ingredients = model.objects.filter(
        recipe__shopping_cart__user=user).values(
        'ingredient__name',
        'ingredient__measurement_unit'
    ).annotate(amount=Sum('amount'))
    for ingredient in ingredients:
        shopping_cart = '\n'.join([
            f"{ingredient['ingredient__name']} - {ingredient['amount']} "
            f"{ingredient['ingredient__measurement_unit']}"
        ])
        pdf.drawString(
            pixels_from_left_text,
            pixels_from_bottom_text_str,
            shopping_cart
        )
        pixels_from_bottom_text_str -= pixels_subtraction
    pdf.showPage()
    pdf.save()
    buffer.seek(buffer_seek_count)
    return FileResponse(
        buffer,
        content_type='application/pdf',
        as_attachment=True,
    )
