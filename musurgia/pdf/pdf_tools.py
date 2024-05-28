from musurgia.pdf.line import HorizontalRuler, VerticalRuler
from musurgia.pdf.text import PageText


def draw_page_numbers(pdf, **kwargs):
    for page in pdf.pages:
        pdf.page = page
        pdf.reset_position()
        page_number = PageText(page, **kwargs)
        page_number.draw(pdf)


def draw_ruler(pdf, mode='h', unit=10, first_label=0, show_first_label=False, label_show_interval=1):
    if mode in ['h', 'horizontal']:
        length = pdf.w - pdf.l_margin - pdf.r_margin
        ruler = HorizontalRuler(length=length, unit=unit, first_label=first_label,
                                show_first_label=show_first_label, label_show_interval=label_show_interval)
    elif mode in ['v', 'vertical']:
        length = pdf.h - pdf.t_margin - pdf.b_margin
        ruler = VerticalRuler(length=length, unit=unit, first_label=first_label,
                              show_first_label=show_first_label, label_show_interval=label_show_interval)
    else:
        raise AttributeError()
    ruler.draw(pdf)
