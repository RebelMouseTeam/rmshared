from typing import Set

from enumclasses import enumclass


class POST:
    @enumclass()
    class TYPE:
        PAGE: 'POST.TYPE' = object()
        IMAGE: 'POST.TYPE' = object()
        VIDEO: 'POST.TYPE' = object()
        EVENT: 'POST.TYPE' = object()
        PLACE: 'POST.TYPE' = object()
        HOW_TO: 'POST.TYPE' = object()
        RECIPE: 'POST.TYPE' = object()
        PRODUCT: 'POST.TYPE' = object()

        ALL: Set['POST.TYPE'] = {PAGE, IMAGE, VIDEO, EVENT, PLACE, RECIPE, HOW_TO, PRODUCT}
