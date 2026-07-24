def main(use, Path=None, **kwargs):
    """."""
    from base64 import b64encode
    import json
    from anvil import BlobMedia
    from anvil.tables import app_tables
    from anvil.server import call

    UTF_8 = "utf-8"

    def create_sheet(rules: list, name: str) -> BlobMedia:
        """."""
        text = "\n".join(rules)
        sheet = BlobMedia("text/css", text.encode(UTF_8), name=name)
        return sheet

    def get_bundle() -> BlobMedia:
        """."""
        table: dict = getattr(app_tables, "use")
        row: dict = table.get(path="bundle.json")
        bundle: BlobMedia = row.get("file")
        print(f"Retrieved {bundle.name} from db.")
        return bundle

    def parse_bundle(bundle: BlobMedia) -> tuple:
        """."""
        # Unpack bundle
        unpacked: dict = json.loads(bundle.get_bytes().decode(UTF_8))
        #  Parse bundle
        use_rules, main_rules = [], []
        for path, text in unpacked.items():
            path = Path(path)

            # XXX text can be manipulated here

            value = b64encode(text.encode(UTF_8)).decode(UTF_8)
            use_rules.append(f'[__path__="{path.path}"] {{\n  --__use__: "{value}";}}')
            # NOTE sheets with same-parcel name are made global (aligns with Vite's lib mode)
            if (
                path.file.type == "css"
                and len(path) > 1
                and path.parts[-2] == path.file.stem
            ):
                main_rules.append(text)
        return use_rules, main_rules

    def upload_sheet(sheet: BlobMedia):
        """."""
        try:
            response: dict = call("_save_file", sheet)
        except Exception as error:
            print(f"{sheet.name} not uploaded. Error: {str(error)}")
        else:
            if response.get("ok"):
                print(f"{sheet.name} uploaded.")
            else:
                print(f"{sheet.name} upload failed. Error: {response.get('error')}")

    
    bundle = get_bundle()
    use_rules, main_rules = parse_bundle(bundle)

    use_sheet, main_sheet = create_sheet(use_rules, "use.css"), create_sheet(
        main_rules, "main.css"
    )
    upload_sheet(use_sheet)
    upload_sheet(main_sheet)
