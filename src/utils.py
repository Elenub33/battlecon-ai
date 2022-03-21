
#TODO: rewrite this
def menu_prompt(options, num_columns=1):
    """Display OPTIONS as a columned menu and solicit a numeric selection.

    Returns:
      The selected index (int)."""
    numbered_options = [f"[{idx}] {item}" for idx, item in enumerate(options)]
    column_length = int(math.ceil(len(options) / num_columns))
    columns = list(IterChunks(enumerate(numbered_options), column_length, fill=(-1, "")))
    column_width = max(map(len, numbered_options))

    for items in itertools.zip_longest(*columns):
        row = "  ".join(map(lambda item: item[1].ljust(column_width), items))
        print("  " + row)

    idx = read_number(0, len(options))
    return options[idx]


def read_number(a, b):
    """Prompt user for a number N such that A <= N < B.

    Returns:
      An integer in the range [`a`, `b`)."""
    while True:
        response = input(f"[{a}-{b-1}] >> ").strip()
        try:
            result = int(response)
            if result < a or result >= b:
                print(f"Please enter an integer between {a} and {b-1} inclusive.")
            else:
                break
        except ValueError:
            print(f"Please enter an integer between {a} and {b-1} inclusive.")
    return result
