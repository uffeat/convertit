"""
/parcels/component/test/test.py
"""


def main(use, console=None, document=None, js=None, **kwargs):
    """."""
    app = use("@/rollo/").app


    component = use("@@/component/component.py")

    button = component.button(
        "btn.btn-primary",
        component.span(text="Foo"),
        text="Foo",
        parent=app
    )

    button(**{".foo": True, "[foo]": True})

    console.log("button:", button.node)


    @button.on(run=True)
    class click:
        def __call__(self, event):
            console.log("event:", event)
