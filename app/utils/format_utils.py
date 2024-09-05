def format_data(data):
    if not data:
        return ""

    headers = data[0].keys()
    formatted_data = []

    formatted_data.append("\t".join(headers))

    for row in data:
        formatted_data.append("\t".join([str(row.get(header, "")) for header in headers]))

    return "\n".join(formatted_data)
