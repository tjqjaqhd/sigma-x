import json
from pathlib import Path


def _parse_simple_yaml(text: str) -> object:
    def parse_value(val: str):
        if not val:
            return ""
        if val[0] in {'"', "'"} and val[-1] == val[0]:
            return val[1:-1]
        if val.isdigit():
            return int(val)
        try:
            return float(val)
        except ValueError:
            return val

    root: dict | list = {}
    stack = [root]
    indents = [0]
    current_key = None
    for raw_line in text.splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith('#'):
            continue
        indent = len(raw_line) - len(raw_line.lstrip())
        line = raw_line.lstrip()
        while indent < indents[-1]:
            stack.pop()
            indents.pop()
        if line.startswith('- '):
            line = line[2:]
            if not isinstance(stack[-1], list):
                stack[-1][current_key] = []  # type: ignore[index]
                stack.append(stack[-1][current_key])  # type: ignore[index]
                indents.append(indent)
            target_list = stack[-1]
            if ':' in line:
                key, value = line.split(':', 1)
                item: dict = {key.strip(): parse_value(value.strip())}
                target_list.append(item)
                if value.strip() == '':
                    stack.append(item[key.strip()])
                    indents.append(indent + 2)
            else:
                target_list.append(parse_value(line))
        else:
            if ':' in line:
                key, value = line.split(':', 1)
                current_key = key.strip()
                value = value.strip()
                if value == '':
                    new_dict: dict = {}
                    if isinstance(stack[-1], list):
                        stack[-1].append({current_key: new_dict})
                    else:
                        stack[-1][current_key] = new_dict  # type: ignore[index]
                    stack.append(new_dict)
                    indents.append(indent)
                else:
                    if isinstance(stack[-1], list):
                        stack[-1].append({current_key: parse_value(value)})
                    else:
                        stack[-1][current_key] = parse_value(value)  # type: ignore[index]
    return root


def load_yaml(path: Path):
    try:
        import yaml  # type: ignore
    except Exception:
        import sys
        sys.path.append('/usr/lib/python3/dist-packages')
        try:
            import yaml  # type: ignore
        except Exception:
            text = path.read_text()
            return _parse_simple_yaml(text)
        else:
            with path.open() as f:
                return yaml.safe_load(f)
    else:
        with path.open() as f:
            return yaml.safe_load(f)
