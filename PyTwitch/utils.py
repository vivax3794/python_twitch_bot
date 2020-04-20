def check_type(name: str, value: any, should_be: type) -> None:  # type: ignore
    """
    Check that the passed in value is the correct type, if not raise TypeError.
    """
    if not isinstance(value, should_be):
        raise TypeError(f"{name} must be type {should_be.__name__}, "
                        "but got {type(value)}")
