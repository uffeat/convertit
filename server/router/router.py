def main(*args, FormResponse=None, route=None, **kwargs):
    """."""
    print("args:", args)  ##
    print("kwargs:", kwargs)  ##


    def client(*args, **kwargs):
        return FormResponse("client", *args, **kwargs)
    route("/")(client)
    route(f"/:_1")(client)





    return 42

    
