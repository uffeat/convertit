def main(use, Base=None, anvil=None, **kwargs):

    document = use("use/document/document.py")

    def clean():
        """Cleans up document."""
        # XXX Vanity only, so remove if interferes with Anvil functionality!
        for id in ["anvil-badge", "anvil-header"]:
            element = document.getElementById(id)
            if element:
                element.remove()
            else:
                ...
                ##log("Could not find element with id:", id, native='warn')

