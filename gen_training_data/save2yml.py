def intentdata2str(intent, examplelst):
    text = f'  - intent: {intent}\n    examples: |\n'
    for emp in examplelst:
        text += '      - ' + emp + "\n"
    return text


def add_head(head, text_str, version='version: "3.1"'):
    head = version + '\n' + head + ":\n"
    return head + text_str


def save2yml(text_str, save_pth):
    with open(save_pth, 'w') as f:
        f.write(text_str)
