import ast

def detect_keylogger(filename):
    with open(filename, "r") as file:
        tree = ast.parse(file.read())

    suspicious_keywords = ["pynput", "keyboard.Listener", "on_press", "keystrokes.txt"]
    for node in ast.walk(tree):
        if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
            for alias in node.names:
                if alias.name in suspicious_keywords:
                    print(f"Suspicious import: {alias.name}")
        elif isinstance(node, ast.Str) and any(word in node.s for word in suspicious_keywords):
            print(f" Suspicious string: {node.s}")

detect_keylogger("keystroke_logger.py")