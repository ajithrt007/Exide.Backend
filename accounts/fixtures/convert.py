def remove_bom_from_utf8(file_path, output_path):
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        content = file.read()

    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(content)

input_file_path = "Exide.Backend/accounts/fixtures/users.json"
output_file_path = "Exide.Backend/accounts/fixtures/users_withoutbom.json"

remove_bom_from_utf8(input_file_path, output_file_path)



def has_bom(file_path):
    with open(file_path, 'rb') as file:
        start = file.read(3)
    return start == b'\xef\xbb\xbf'

input_file_path = "Exide.Backend/accounts/fixtures/users_withoutbom.json"
print("BOM present:", has_bom(input_file_path))