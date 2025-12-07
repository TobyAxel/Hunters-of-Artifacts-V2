from backend.sql_connection import cursor

def rows_to_dicts(rows):
    cols = [desc[0] for desc in cursor.description] if cursor.description else []
    return [dict(zip(cols, row)) for row in rows]

def is_ident(ident):
    if isinstance(ident, str) and len(ident) == 4:
        return True
    else:
        return False
