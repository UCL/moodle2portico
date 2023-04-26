def save_string_as_file(string_data, filenams):
    """Write (multiline) string to output file."""
    with open(filenams,'w',encoding="utf-8") as f:
        f.write(string_data)
