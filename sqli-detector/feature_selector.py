from constant import (
    sql_keywords,
    special_characters,
    comment_symbols,
    escape_symbols,
    wildcard_symbols,
)


def total_sql_keyword_in_string(s):
    s_lower = s.lower() if s is str else str(s)
    return sum([s_lower.count(keyword.lower()) for keyword in sql_keywords])


def total_special_characters(s):
    return sum([str(s).count(c) for c in special_characters])


def total_comment_symbols(s):
    return sum([str(s).count(c) for c in comment_symbols])


def total_wildcard_symbols(s):
    return sum([str(s).count(c) for c in wildcard_symbols])


def total_escape_symbols(s):
    return sum([str(s).count(c) for c in escape_symbols])


def select_features(s):
    return dict(
        sql_keyword=total_sql_keyword_in_string(s),
        special_char=total_special_characters(s),
        comment_char=total_comment_symbols(s),
        wildcard_char=total_wildcard_symbols(s),
        escape_char=total_escape_symbols(s),
    )
