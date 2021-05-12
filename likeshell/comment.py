import os

ITEM = ('alias', 'options')
nl = os.linesep


def parse_item(content, item):
    if item == 'alias':
        return parse_alias(content)


def parse_alias(content):
    return content.strip()


def parse_comment(doc):
    """
    Parse comment to get information about method or parameter
    E.g. `:keyword`
    """
    meta = {
        'alias': None
    }
    lines = doc.split(nl)
    for line in lines:
        line = line.strip()
        if line.startswith(':'):
            item = line[1:]
            if item.split(':')[0] in ITEM:
                item_key = item.split(':')[0]
                content = item.split(':')[1]
                meta[item_key] = parse_item(content, item_key)
            elif item.split(' ')[0] in ITEM:
                item_key = item.split(' ')[0]
                content = item.split(' ')[1]
                meta[item_key] = parse_item(content, item_key)
    return meta
