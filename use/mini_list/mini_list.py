def main(use, *args, **kwargs):
    """."""
    
    class MiniList(list):
        def __init__(self, *args, **kwargs):
            self.append(*args, **kwargs)

        def __getitem__(self, index):
            """Returns value by index (without IndexError risk) or sliced section."""
            if isinstance(index, int):
                if -len(self) <= index < len(self):
                    return list.__getitem__(self, index)
                # Implicit None-return instead of IndexError
            if isinstance(index, slice):
                values = [getattr(index, k) for k in ["start", "stop", "step"]]
                if all([v is None or isinstance(v, int) for v in values]):
                    return list.__getitem__(self, index)
                raise NotImplementedError(f"slice: {index}")

        def __setitem__(self, index, value):
            if -len(self) <= index < len(self):
                list.__setitem__(self, index, value)
            # NOTE Silently ignores attempts to set out of range

        def append(self, *args, **kwargs) -> "MiniList":
            """
            Appends values.
            kwargs are appended as single-item dicts.
            """
            for value in args:
                list.append(self, value)
            for item in kwargs.items():
                list.append(self, {item[0]: item[1]})
            return self

        def copy(self, *args, **kwargs) -> "MiniList":
            return self.__class__(dict.copy(self))

        def dict(self, *args, **kwargs) -> dict:
            """Returns dict representation."""
            return {i: v for i, v in enumerate(self)}

        def extend(self, *args, **kwargs) -> "MiniList":
            """
            Appends values by extension.
            Attempts type-casting for non-standard types.
            kwargs are appended as full dicts.
            """
            for extension in args:
                if isinstance(extension, (dict, list, tuple)):
                    list.extend(self, extension)
                else:
                    try:
                        list.extend(self, list(extension))
                    except:
                        pass
            if kwargs:
                list.append(self, kwargs)
            return self

        def extract(self, *args, **kwargs):
            """Extracts and returns first value that satisfies predicates."""
            predicates = [v for v in args if callable(v)]
            default = next(
                (v for i, v in enumerate(args) if i == len(args) - 1 and not callable(v)),
                None,
            )
            if predicates:
                return next(
                    iter(
                        [
                            list.pop(self, i)
                            for i, v in enumerate(self)
                            if all([p(i, v) for p in predicates])
                        ]
                    ),
                    default,
                )

        def get(self, *args, **kwargs):
            """Returns value by index without IndexError risk (mimics dict.get)."""
            args = iter(args)
            index, default = next(args, -1), next(args, None)
            return (
                list.__getitem__(self, index)
                if isinstance(index, int) and (-len(self) <= index < len(self))
                else default
            )

        def index(self, *args, **kwargs):
            """
            Returns index for first occurance of reference.
            Returns False if value not found.
            Option to provide reference as callable predicate.
            Option to scope search to slice, in which case index is relative to slice
            (in contrast to native method).
            """
            if args:
                ref, *args = args
                section = self.slice(*args) if args else self
                for index, value in enumerate(section):
                    if ref == value or (callable(ref) and ref(index, value)):
                        return index
            return False

        def insert(self, *args, **kwargs):
            """."""
            args = iter(args)
            index, value, error = next(args, -1), next(args, None), next(args, False)
            if isinstance(index, int) and (-len(self) <= index < len(self)):
                list.insert(self, index, value)
                return self

            return error(index, value) if callable(error) else error

        def items(self, *args, **kwargs) -> iter:
            """Returns index-value pairs."""
            return ((i, v) for i, v in enumerate(self))

        def keys(self, *args, **kwargs) -> iter:
            """Returns indices."""
            return (i for i, v in enumerate(self))

        def values(self, *args, **kwargs) -> iter:
            """Returns values."""
            return (v for v in self)

        def pop(self, *args, **kwargs):
            """Removes value by index without IndexError risk (mimics dict.pop)."""
            args = iter(args)
            index, default = next(args, -1), next(args, None)
            return (
                list.pop(self, index)
                if isinstance(index, int) and (-len(self) <= index < len(self))
                else default
            )

        def prepend(self, *args, **kwargs) -> "MiniList":
            """
            Prepends values.
            kwargs are prepended as single-item dicts.
            """
            for value in args:
                list.insert(self, 0, value)
            for item in kwargs.items():
                list.insert(self, 0, {item[0]: item[1]})
            return self

        def remove(self, *args, **kwargs) -> "MiniList":
            """Removes values without ValueError risk."""
            for value in args:
                if value in self:
                    list.remove(self, value)
            return self

        def set(self, *args, **kwargs):
            """."""
            args = iter(args)
            index, value, error = next(args, -1), next(args, None), next(args, False)
            if isinstance(index, int) and (-len(self) <= index < len(self)):
                list.__setitem__(self, index, value)
                return self
            return error(index, value) if callable(error) else error

        def slice(self, *args, **kwargs) -> "MiniList":
            """Returns slice."""
            KEYS = ("start", "stop", "step")
            args = {
                i: v
                for i, v in enumerate(
                    [v for v in args if v is None or isinstance(v, int)][: len(KEYS)]
                )
            }
            return self.__class__(
                *list.__getitem__(
                    self,
                    slice(*[kwargs.get(v, args.get(i)) for i, v in enumerate(KEYS)]),
                )
            )

        def resize(self, *args, **kwargs):
            """."""

        def patch(self, *args, **kwargs):
            """."""

        @staticmethod
        def from_dict(*args, **kwargs):
            """."""

        @staticmethod
        def create(*args, **kwargs):
            """."""
            args = list(args)
            source = next(iter([args.pop(i) for i, v in enumerate(args) if not i]), None)
            ...



    return MiniList


