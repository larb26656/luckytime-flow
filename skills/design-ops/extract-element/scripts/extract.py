#!/usr/bin/env python3
"""Deterministic extraction artifacts; requires Pillow. No model/API calls."""
import argparse
import hashlib
import json
import re
import secrets
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps


def save(root, data):
    target = root / 'manifest.json'
    temporary = root / 'manifest.json.tmp'
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temporary.replace(target)


def load(root):
    data = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
    with Image.open(root / 'source.png') as source:
        size = list(source.size)
    if data['source']['size'] != size:
        raise ValueError('Source size differs from manifest')
    elements = data['elements']
    ids = [e['id'] for e in elements]
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate element IDs')
    for e in elements:
        if not re.fullmatch(r'element-[0-9]{3,}', e['id']):
            raise ValueError('IDs must use element-001 format')
        if e['type'] not in ('text', 'visual', 'group'):
            raise ValueError('Unknown element type')
        if not isinstance(e.get('regenerate', False), bool):
            raise ValueError('regenerate must be boolean')
        box = e['bounds']
        if len(box) != 4 or any(type(v) is not int for v in box):
            raise ValueError('Bounds must be four integer pixels')
        x, y, w, h = box
        if min(x, y) < 0 or min(w, h) <= 0 or x + w > size[0] or y + h > size[1]:
            raise ValueError(f"Invalid bounds: {e['id']}")
        if e.get('parent') is not None and e['parent'] not in ids:
            raise ValueError('Unknown parent')
        seen = {e['id']}
        parent = e.get('parent')
        while parent is not None:
            if parent in seen:
                raise ValueError('Parent cycle')
            seen.add(parent)
            parent = next(item for item in elements if item['id'] == parent).get('parent')
        if e['type'] == 'text' and not isinstance(e.get('text'), str):
            raise ValueError('Text elements require text string')
        if type(e.get('order', 0)) is not int:
            raise ValueError('order must be integer')
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    init = sub.add_parser('init')
    init.add_argument('image', type=Path)
    init.add_argument('--output-root', type=Path, default=Path('.extracted'))
    for name in ('prepare', 'text', 'finalize'):
        command = sub.add_parser(name)
        command.add_argument('directory', type=Path)
    args = parser.parse_args()
    if args.command == 'init':
        raw = args.image.read_bytes()
        with Image.open(args.image) as original:
            if getattr(original, 'n_frames', 1) != 1:
                raise ValueError('Provide one still image per run')
            source = ImageOps.exif_transpose(original).convert('RGBA')
        stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
        root = args.output_root / f'{secrets.token_hex(4)}-{stamp}'
        root.mkdir(parents=True, exist_ok=False)
        for folder in ('references', 'assets'):
            (root / folder).mkdir()
        source.save(root / 'source.png')
        save(root, {'version': 1, 'source': {'file': 'source.png', 'original_name': args.image.name,
             'original_sha256': hashlib.sha256(raw).hexdigest(), 'size': list(source.size)},
             'coordinate_system': 'pixel-xywh-top-left', 'elements': []})
        print(root)
        return
    root = args.directory
    data = load(root)
    elements = sorted(data['elements'], key=lambda e: e['id'])
    if not elements:
        raise ValueError('Manifest has no elements; analyze source first')
    if args.command == 'prepare':
        with Image.open(root / 'source.png') as source:
            preview = source.convert('RGB')
            draw = ImageDraw.Draw(preview)
            for e in elements:
                x, y, w, h = e['bounds']
                reference = f"references/{e['id']}.png"
                source.crop((x, y, x + w, y + h)).save(root / reference)
                e['reference'] = reference
                draw.rectangle((x, y, x + w - 1, y + h - 1), outline='red', width=2)
                draw.text((x + 2, y + 2), e['id'], fill='red')
            preview.save(root / 'bounds-preview.png')
        save(root, data)
    elif args.command == 'text':
        ordered = sorted(elements, key=lambda e: (e.get('order', 0), e['id']))
        blocks = [f"## {e['id']}\n\n{e['text']}" for e in ordered if e['type'] == 'text']
        (root / 'text.md').write_text('\n\n'.join(blocks) + '\n', encoding='utf-8')
    else:
        report = []
        for e in elements:
            if not e.get('regenerate', False):
                e['status'] = 'not-requested'
                continue
            asset = root / 'assets' / f"{e['id']}.png"
            e.pop('asset', None)
            e.pop('asset_info', None)
            e['status'] = 'missing'
            if asset.exists():
                try:
                    with Image.open(asset) as generated:
                        generated.load()
                        alpha = generated.getchannel('A').getextrema() if 'A' in generated.getbands() else None
                        transparent = alpha is not None and alpha[0] < 255
                        e['asset_info'] = {'size': list(generated.size), 'has_transparency': transparent}
                        e['asset'] = f"assets/{e['id']}.png"
                        e['status'] = 'needs-review' if e.get('transparent', False) and not transparent else 'generated'
                except (OSError, ValueError):
                    e['status'] = 'invalid'
            report.append({'id': e['id'], 'status': e['status']})
        save(root, data)
        (root / 'report.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
        print(json.dumps(report))
        if any(row['status'] != 'generated' for row in report):
            raise SystemExit(1)


if __name__ == '__main__':
    main()
