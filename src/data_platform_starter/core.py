def greet(name: str) -> str:
    """Return a greeting for ``name``, falling back to "world" when blank."""
    return f"Hello, {name.strip() or 'world'}!"
