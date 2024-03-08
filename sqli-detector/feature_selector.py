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
    strLength = len(s)
    sql_keyword_count = total_sql_keyword_in_string(s)
    special_char_count = total_special_characters(s)
    return dict(
        length=strLength,
        sql_keyword_count=sql_keyword_count,
        sql_keyword_freq=sql_keyword_count / strLength,
        special_char_count=special_char_count,
        special_char_freq=special_char_count / strLength,
        comment_char_count=total_comment_symbols(s),
        wildcard_char_count=total_wildcard_symbols(s),
        escape_char_count=total_escape_symbols(s),
    )
