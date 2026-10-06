def main(
    use,
    Base: type = None,
    log: callable = None,
    path: str = None,
    **kwargs,
) -> None:
    """."""

    from base64 import b64decode, b64encode
    from datetime import datetime, timezone
    import json
    import pathlib
    from mimetypes import guess_type
    import traceback
    from jinja2 import Template
    from anvil import BlobMedia, Media, URLMedia, app, is_server_side
    from anvil.server import (
        HttpResponse,
        FormResponse,
        call,
        callable as server_function,
        context,
        request,
        route,
        session,
        get_app_origin,
    )
    from tools import Dictionary

    use("server/router/router.py")
    State = use("server/state/state.py")

    @server_function
    def main(
        name: str,
        submission: int = None,
        **rest,
    ):
        """."""
        args = rest.get('args', [])
        kwargs = rest.get('kwargs', {})


        
        
        # XXX TODO Wrap in try-except
        state = State()
        ##log("state:", state)  ##

        browser_session = rest.get("session")
        if browser_session:
            if (
                "_browser_session" not in session
                or session["_browser_session"] != browser_session
            ):
                session["_browser_session"] = browser_session
                state.browser.clear()

        state.server(count=state.server.count + 1 if "count" in state.server else 0)
        state.browser(count=state.browser.count + 1 if "count" in state.browser else 0)

        _main = use(f"server/functions/{name}/{name}.py")

        meta = Base(
            session_id=session.session_id,
            browser_session=browser_session,
            name=name,
            state=state,
        )



        result = _main(meta, *args, **kwargs)

        return dict(
            result=result,
            meta=dict(
                session_id=session.session_id,
                browser_session=browser_session,
                name=name,
                server=dict(**state.server),
                browser=dict(**state.browser),
            )
        )
