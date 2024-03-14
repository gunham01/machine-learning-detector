import re
from constant import (
    sql_keywords,
    common_sql_functions_name,
    sql_env_variables,
    special_characters,
    comment_symbols,
    escape_symbols,
    wildcard_symbols,
)


def count_sql_keyword_in_string(s):
    s_lower = s.lower() if s is str else str(s)
    return sum([s_lower.count(keyword.lower()) for keyword in sql_keywords])


def count_special_characters(s):
    return sum([str(s).count(c) for c in special_characters])


def count_comment_symbols(s):
    return sum([str(s).count(c) for c in comment_symbols])


def count_wildcard_symbols(s):
    return sum([str(s).count(c) for c in wildcard_symbols])


def count_escape_symbols(s):
    return sum([str(s).count(c) for c in escape_symbols])


def has_union(s):
    return int("union" in str(s).lower())


def union_count(s):
    return str(s).lower().count("union")


def count_selected_column(s):
    selected_columns = re.findall(r"SELECT\s+(.*?)\s+FROM", str(s), re.IGNORECASE)
    return (
        sum(len(columns.split(",")) for columns in selected_columns)
        if selected_columns
        else 0
    )


def has_comment(s):
    return int("--" in str(s))


def has_concatenation(s):
    return int("+" in str(s) or "||" in str(s))


def has_sleep_or_benchmark(s):
    s_lower = s.lower() if s is str else str(s)
    sleep_function_names = ["sleep", "benchmark", "waitfor delay", "pg_sleep"]
    return int(any(name in s_lower for name in sleep_function_names))


def count_single_quote(s):
    return str(s).count("'")


def count_double_quote(s):
    return str(s).count('"')


def count_common_sql_function_names(s):
    s_lower = s.lower() if s is str else str(s)
    return sum([s_lower.count(name) for name in common_sql_functions_name])


def count_sql_env_variables(s):
    s_lower = s.lower() if s is str else str(s)
    return sum([s_lower.count(name) for name in sql_env_variables])


def has_nested_select(s):
    return int("SELECT" in str(s) and "FROM" in str(s))


def has_boolean_based_blind(s):
    patterns = [
        r"\bAND\b\s+\d+\s*=\s*\d+",  # Matches "AND 1=1" or similar patterns
        r"\bOR\b\s+\d+\s*=\s\d+",  # Matches "OR 1=1" or similar patterns
        r"\bNOT\b\s+\d+\s*=\s\d+",  # Matches "NOT 1=1" or similar patterns
        # Add more patterns as needed based on known attack vectors
    ]
    return int(any(re.search(pattern, str(s), re.IGNORECASE) for pattern in patterns))


def select_features(s):
    s_length = len(str(s))
    sql_keyword_count = count_sql_keyword_in_string(s)
    special_char_count = count_special_characters(s)
    sql_keyword_freq = round(sql_keyword_count / s_length, 2) if s_length > 0 else 0
    special_char_freq = round(special_char_count / s_length, 6) if s_length > 0 else 0
    return dict(
        # 1. Độ dài chuỗi
        length=s_length,
        # 2. Số lượng từ khóa SQL
        sql_keyword_count=sql_keyword_count,
        # 3. Tần suất từ khóa SQL
        sql_keyword_freq=sql_keyword_freq,
        # 4. Số lượng ký tự đặc biệt
        special_char_count=special_char_count,
        # 5. Tần suất ký tự đặc biệt
        special_char_freq=special_char_freq,
        # 6. Số lượng ký tự comment
        comment_char_count=count_comment_symbols(s),
        # 7. Số lượng ký tự wildcard
        wildcard_char_count=count_wildcard_symbols(s),
        # 8. Số lượng ký tự escape
        escape_char_count=count_escape_symbols(s),
        # 9. Có chứa từ khóa UNION không
        has_union=has_union(s),
        # 10. Số lượng từ khóa UNION
        union_count=union_count(s),
        # 11. Số lượng cột được chọn
        select_column_count=count_selected_column(s),
        # 12. Có chứa comment không
        has_comment=has_comment(s),
        # 13. Có chứa phép nối chuỗi không
        has_concatenation=has_concatenation(s),
        # 14. Có chứa sleep không
        has_sleep_or_brenchmark=has_sleep_or_benchmark(s),
        # 15. Số lượng ký tự nháy đơn
        single_quote_count=count_single_quote(s),
        # 16. Số lượng ký tự nháy kép
        double_quote_count=count_double_quote(s),
        # 17. Số lượng hàm SQL phổ biến
        common_sql_function_count=count_common_sql_function_names(s),
        # 18. Số lượng biến môi trường SQL
        sql_env_variable_count=count_sql_env_variables(s),
        # 19. Chứa pattern n=n hoặc n=m của trong boolean-based blind không
        has_boolean_based_blind=has_boolean_based_blind(s),
    )
