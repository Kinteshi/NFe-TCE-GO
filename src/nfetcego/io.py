
def read_sql(filename: str) -> str:
    with open(filename, 'r') as f:
        return f.read()
