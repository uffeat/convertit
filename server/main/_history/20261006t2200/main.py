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
    def main(browser_session, name, *args, **kwargs):
        """."""
        # XXX TODO Wrap in try-except
        state = State()
        ##log("state:", state)  ##

        if "_browser_session" in session:
            if session["_browser_session"] != browser_session:
                session["_browser_session"] = browser_session
                state.clear()


        else:
            session["_browser_session"] = browser_session
            state.clear()



        if "count" in state:
            ##count = state["count"] + 1
            ##state(count=count)
            state["count"] += 1
        else:
            state(count=0)

        return dict(id=session.session_id, browser_session=browser_session, name=name, **state)
