import ast
import pathlib

SRC_DIR = pathlib.Path('src')

class FunctionChecker(ast.NodeVisitor):
    def __init__(self):
        self.current_func_depth = 0
        self.problems = []
        self.filename = ''

    def visit_FunctionDef(self, node):
        self.current_func_depth += 1
        if self.current_func_depth == 1:
            self.check_function(node)
        self.current_func_depth -= 1

    visit_AsyncFunctionDef = visit_FunctionDef

    def check_function(self, node):
        returns = ast.unparse(node.returns) if node.returns else None
        returns_none = returns in (None, 'None')
        found_return_with_value = False
        found_return_without_value = False
        for n in node.body:
            # skip nested functions
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            for sub in ast.walk(n):
                if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    break
            else:
                if isinstance(n, ast.Return):
                    if n.value is not None and not (isinstance(n.value, ast.Constant) and n.value.value is None):
                        found_return_with_value = True
                    else:
                        found_return_without_value = True
                else:
                    for sub in ast.walk(n):
                        if isinstance(sub, ast.Return):
                            if sub.value is not None and not (isinstance(sub.value, ast.Constant) and sub.value.value is None):
                                found_return_with_value = True
                            else:
                                found_return_without_value = True
        if returns_none and found_return_with_value:
            self.problems.append((self.filename, node.name, 'return None annotated but returns value'))
        if not returns_none and found_return_without_value:
            self.problems.append((self.filename, node.name, 'return annotated non-None but returns None'))


def find_return_mismatches():
    problems = []
    for path in SRC_DIR.rglob('*.py'):
        tree = ast.parse(path.read_text())
        checker = FunctionChecker()
        checker.filename = path.name
        checker.visit(tree)
        problems.extend(checker.problems)
    return problems


def find_docstring_mismatches():
    problems = []
    for path in SRC_DIR.rglob('*.py'):
        tree = ast.parse(path.read_text())
        for node in [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]:
            doc = ast.get_docstring(node)
            returns = ast.unparse(node.returns) if node.returns else None
            if doc:
                doc_lower = doc.lower()
                if "반환" in doc_lower or "return" in doc_lower or "리턴" in doc_lower:
                    if returns in (None, "None"):
                        problems.append((path.name, node.name, "docstring says returns but annotation is None"))
    return problems

def test_return_annotations_consistent():
    assert find_return_mismatches() == []


def test_docstring_return_consistent():
    assert find_docstring_mismatches() == []
