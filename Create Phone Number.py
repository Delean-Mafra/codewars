def create_phone_number(n: list[int]) -> str:
    dm_s = "".join(map(str, n))
    return f"({dm_s[0:3]}) {dm_s[3:6]}-{dm_s[6:10]}"
