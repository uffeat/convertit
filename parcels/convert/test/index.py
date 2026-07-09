"""
/parcels/convert/test/index.py
"""


def main(use, app=None, component=None, console=None, document=None, js=None, **kwargs):
    ##print("kwargs:", kwargs)  ##

    button = component.button(
        "btn.btn-primary",
        component.span(text="Foo"),
        text="Foo",
    )

    button(**{".foo": True, "[foo]": True})

    console.log("button:", button.node)

    @button.on(run=True)
    class click:
        def __call__(self, event):
            console.log("event:", event)

    page = use("@@/convert/convert.js").page
    print("page:", page)

    _page = component(page, button, **{".foo": True, "[foo]": True})

    print("page has button:", button in _page)

    for child in _page:
        console.log("child:", child)

    console.log("HTMLElement:", js.HTMLElement)

    print('page is an HTMLElement:', js.isinstance(page, js.HTMLElement))

    console.log("button:", _page('button'))

    

