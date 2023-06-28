def replace_all(text: str, changes: list[tuple[str, str]] or list[str], replace_all_for=None) -> str:
    """Replace All
    @text: Texto que recebera as modificacoes.

    * Recebe uma lista de tuplas (a, b) ->
    [a] sera substituido; [b] sera o "substituido por".
    * list[str]-> lista com o que sera substituido.
    * [replace_all_for] -> "substituido por" de todos.
    """
    if isinstance(changes[0], tuple):
        for from_, to in changes:
            text = text.replace(from_, (replace_all_for if replace_all_for else to))
    elif isinstance(changes[0], str):
        if replace_all_for != '' and not replace_all_for:
            raise ValueError('[replace_all_for] deve ser passado para list[str]')
        for from_ in changes:
            text = text.replace(from_, replace_all_for)
    else:
        raise ValueError('[changes] type nao suportado')

    return text
