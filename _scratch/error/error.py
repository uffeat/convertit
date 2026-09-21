class AssetError(Exception):

    def __init__(self, message):
        Exception.__init__(self, message)

    def __bool__(self):
        return False



print('message:', str(AssetError('Bad')))

print('type:', type(AssetError('Bad')).__name__)
print('type:', AssetError('Bad').__class__.__name__)