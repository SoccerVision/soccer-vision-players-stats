class GeneratorError(ValueError):
    """An invalid option combination the generator rejects on purpose (e.g. a role not valid for
    the position, a squad over MAX_SQUAD_SIZE). app.main's exception handler turns this into a
    422 with the message as-is - these are always written to be client-safe. A plain ValueError
    (a bug, not a deliberate rejection) is not caught by that handler and 500s instead, so a
    future unrelated error can't accidentally echo its message to the caller."""
