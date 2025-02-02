import re

# Function to update buildozer.spec using regex with flexible context
def update_buildozer_spec(spec_file_path, context, strict_fields=None) -> str:
    """
    Update the buildozer.spec file by replacing the values of specific fields 
    based on the provided context dictionary.
    
    Args:
    - spec_file_path (str): Path to the buildozer.spec file.
    - context (dict): A dictionary containing the fields to be updated and their new values.
    - strict_fields (list): A list of fields for which strict policy applies (uncommented fields only).
    
    Returns:
    - str: The updated content of the buildozer.spec file.
    """
    
    # Read the content of the buildozer.spec file
    with open(spec_file_path, "r", encoding="utf-8") as file:
        file_content = file.read()

    # Default strict_fields to an empty list if not provided
    strict_fields = strict_fields or []

    # Iterate through each key-value pair in the context dictionary
    for field, value in context.items():
        # Escape special regex characters in the value
        escaped_value = str(value)  # Ignore escaping for now

        # Check if the current field is in the strict_fields list
        if field in strict_fields:
            # Strict mode: Only match uncommented fields (no leading # or spaces)
            pattern = rf'^\s*{field} = .+'
        else:
            # Non-strict mode: Match both uncommented and commented fields
            pattern = rf'^\s*#?\s*{field} = .+'
        
        replacement = f'{field} = {escaped_value}'
        
        # Perform the substitution if the pattern is found
        file_content = re.sub(pattern, replacement, file_content, flags=re.MULTILINE)
    
    # Optionally, if any fields do not exist in the file, add them at the end
    for field, value in context.items():
        if not re.search(rf'^\s*#?\s*{field} = ', file_content, flags=re.MULTILINE):
            file_content += f'\n{field} = {re.escape(str(value))}'
    
    # Write the updated content back to the file
    with open(spec_file_path, "w", encoding="utf-8") as file:
        file.write(file_content)
    
    return file_content
