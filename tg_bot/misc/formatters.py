def format_todo(sql: str, **kwargs):
    sql += " AND ".join(tuple((f"{item} = %s" for item in kwargs.keys())))
    parameters = tuple((values for values in kwargs.values()))
    return sql, parameters
