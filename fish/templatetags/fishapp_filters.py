from django import template
register = template.Library()


@register.filter
def getList(querydict, item_to_get):
    return querydict.getlist(item_to_get)

@register.filter
def getJSArray(querrydict, item_to_get):
    to_ret = "["
    for el in querrydict.getlist(item_to_get):
        to_ret += el + ", "
    list_ret = list(to_ret)
    print(list_ret)
    list_ret[-2:] = "]"
    print(list_ret)
    to_ret = "".join(list_ret)
    return to_ret
