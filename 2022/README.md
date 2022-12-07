|Task|Date  |Learning|
|----|----  |--------|
|1|02.12.2022|Storing and sorting the entire list is cleaner than keeping track of the max-item. It also provides flexibility for finding top-`n` items with zero refactoring. The performance hit might be worth it.|
|2|02.12.2022|If the nature of input can be subject to change (source, type, etc.), it is best to keep all assumptions related to it localized.
|3|03.12.2022|Use `f.read().splitlines()` to read file as list of lines without the trailing newline character. Use the `string` module to access [uppercase](https://docs.python.org/3/library/string.html#string.ascii_uppercase, "uppercase docs") and [lowercase](https://docs.python.org/3/library/string.html#string.ascii_lowercase, "lowercase docs") alphabets.
|7|07.12.2022|The `setdefault(key, value)` method of `dict` sets `key` to `value` if `key` doesn't exist in the dictionary. Else, it does nothing.