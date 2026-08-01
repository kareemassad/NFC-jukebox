def find_album(rows, tag_id):
    for row in rows:
        if str(tag_id) == row["ID"]:
            return row["URI"], row["Artist"], row["Album"]
    return None
