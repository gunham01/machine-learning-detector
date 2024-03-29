sql_keywords = [
    "SELECT",
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "TRUNCATE",
    "ALTER",
    "JOIN",
    "UNION",
    "WHERE",
    "FROM",
    "AND",
    "OR",
    "LIKE",
    "EXEC",
    "EXECUTE",
    "DECLARE",
    "CREATE",
    "TABLE",
    "DATABASE",
]

common_sql_functions_name = [
    "CONCAT(",
    "COUNT(",
    "SUM(",
    "AVG(",
    "MIN(",
    "MAX(",
    "CONVERT(",
    "CAST(",
    "SUBSTRING(",
    "SUBSTR(",
    "ASCII(",
    "RAISEERROR(",
    "SIGNAL(",
    "ERROR(",
]

sql_env_variables = [
    "@@VERSION",
    "@@OSVERSION",
    "@@SERVERNAME",
    "@@HOSTNAME",
    "DATABASE()",
]

special_characters = [
    "!",
    "@",
    "#",
    "$",
    "%",
    "^",
    "&",
    "*",
    "(",
    ")",
    "-",
    "_",
    "+",
    "=",
    "{",
    "}",
    "[",
    "]",
    "|",
    "\\",
    ":",
    ";",
    '"',
    "'",
    "<",
    ">",
    ",",
    ".",
    "?",
    "/",
    "`",
    "~",
    " ",
]

comment_symbols = [
    "--",
    "/*",
    "*/",
    "#",
]

wildcard_symbols = [
    "%",
    "_",
    "[",
    "]",
    "^",
    "[^]",
]

escape_symbols = [
    "\\",
    "\n",
    "\t",
    "\r",
    "\b",
    "\f",
    "\v",
]

sql_network_comamnds = [
    "xp_cmdshell",
    "xp_regwrite",
    "xp_regread",
    "OPENROWSET",
    "OPENDATASOURCE",
    "OPENQUERY",
    "BULK INSERT",
    "NET USE",
    "sp_OACreate",
    "sp_OAMethod",
    "sp_OAGetProperty",
    "sp_OADestroy",
]
