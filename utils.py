import io
from docxtpl import DocxTemplate
import re

from flask import send_file


def unflatten_dict(flat_dict: dict):
    """
    Unflattens a dictionary representing form data into a nested dictionary.

    This function takes a dictionary with keys that represent nested levels
    using a specific notation (e.g., "education[0][period]") and transforms it
    into a multilevel nested dictionary or list structure.

    Args:
        flat_dict (dict): A flat dictionary where keys represent nested levels.

    Returns:
        dict: A nested dictionary or list structure representing the original form data.

    Example:
        >>> flat_dict = {
        ...     'education[0][period]': '2010-2014',
        ...     'education[0][name_education]': 'Bachelor of Science',
        ...     'education[1][period]': '2015-2017',
        ...     'education[1][name_education]': 'Master of Science',
        ...     'highlights[0]': 'Graduated with honors'
        ... }
        >>> unflatten_dict(flat_dict)
        {
            'education': [
                {
                    'period': '2010-2014',
                    'name_education': 'Bachelor of Science'
                },
                {
                    'period': '2015-2017',
                    'name_education': 'Master of Science'
                }
            ],
            'highlights': ['Graduated with honors']
        }
    """

    def get_or_create_with_padding(lst, index, default=None):
        """
        Ensures the list has an item at the specified index, extending the list with
        the default value if necessary.

        Args:
            lst (list): The list to be accessed or extended.
            index (int): The index at which the item is needed.
            default: The default value to use for padding if the list is extended.

        Returns:
            The item at the specified index, or the default value if the list was extended.
        """
        if index < len(lst):
            return lst[index]
        else:
            lst.extend([default] * (index - len(lst) + 1))
            return default

    def sliding_window(lst):
        """
        Yields pairs of consecutive items from the list, with the second item being None for the last element.

        Args:
            lst (list): The list to iterate over.

        Yields:
            tuple: A pair of consecutive items from the list.
        """
        for i in range(len(lst)):
            if i < len(lst) - 1:
                yield lst[i], lst[i + 1]
            else:
                yield lst[i], None

    def set_nested_item(data_dict, keys, value):
        """
        Sets a value in the nested dictionary or list structure based on the provided keys.

        Args:
            data_dict (dict): The root dictionary to modify.
            keys (list): A list of keys representing the nested levels.
            value: The value to set at the specified location.
        """
        curr = data_dict
        for key, next_key in sliding_window(keys):
            if isinstance(curr, list):
                key = int(key)
                if next_key is None:
                    curr.insert(key, value)
                else:
                    next = get_or_create_with_padding(
                        lst=curr,
                        index=key,
                        default=([] if next_key and next_key.isdigit() else {}),
                    )
                    curr = next
            elif isinstance(curr, dict):
                if next_key is None:
                    curr[key] = value
                elif key not in curr:
                    curr[key] = [] if next_key and next_key.isdigit() else {}
                curr = curr[key]

    unflattened_dict = {}

    for key, value in flat_dict.items():
        keys = re.split(r"\[|\]\[|\]", key)
        keys = [k for k in keys if k]  # Remove empty strings from the list
        set_nested_item(unflattened_dict, keys, value)

    return unflattened_dict


def render_and_send_file(data: dict, tpl: DocxTemplate, download_name: str):
    # Generate docx
    tpl.render(data)
    cv_buffer = io.BytesIO()
    tpl.save(cv_buffer)
    cv_buffer.seek(0)

    # Return CV
    return send_file(
        cv_buffer,
        as_attachment=True,
        download_name=download_name,
    )
