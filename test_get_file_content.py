from functions.get_file_content import get_file_content

result = get_file_content("calculator", "lorem.txt")
print(f"Length: {len(result)}")
print(result[-100:])  # print just the end to see the truncation message

print(get_file_content("calculator", "main.py"))
print(get_file_content("calculator", "pkg/calculator.py"))
print(get_file_content("calculator", "/bin/cat"))
print(get_file_content("calculator", "pkg/does_not_exist.py"))
