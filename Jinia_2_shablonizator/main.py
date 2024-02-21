from jinja2 import Template

name = "Федор"

tm = Template('''привет последовательность
{% for i in range(20) -%}{{i}} {% endfor %}
Ну а здесь {{name}} {{print}}
{% filter upper %}Сюда можно суеуть что угодно по сути {%endfilter%}

''')


# Вместо определения, которое написано в фигурных скобках, подставляет
# вместо name соответствующее значение, для этого используется метод render класса Template

msg = tm.render(name = name, print = ("ХУЙ"))

print(msg)