import minify_html as _minify

options = dict(
    minify_css=True,
    remove_processing_instructions=True,
    keep_closing_tags=True,
    keep_html_and_head_opening_tags=True,
    keep_comments=False,
)


class minify:
    def __call__(self, text: str):
        text = text.strip()
        if text.startswith("<"):
            return self.html(text)
        return self.css(text)

    @staticmethod
    def css(text: str) -> str:
        """Returns minified css."""
        try:
            return _minify.minify(f"<style>{text}</style>", minify_js=False, **options)[
                7:-8
            ]
        except:
            return text

    @staticmethod
    def html(
        text: str,
    ) -> str:
        """Returns minified html."""
        try:
            return _minify.minify(text, minify_js=False, **options)
        except:
            return text

    @staticmethod
    def js(text: str) -> str:
        """Returns minified js."""
        try:
            return _minify.minify(
                f"<script>{text}</script>", minify_js=True, **options
            )[8:-9]
        except:
            return text


minify = minify()
