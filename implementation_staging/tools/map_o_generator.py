from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from map_o import MapO, MapOError, inspect_map_ref, load_spec, read_map_ref


def add_ref_arguments(parser: argparse.ArgumentParser) -> None:
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--ref', type=Path, help='Path to <id>.map.ref')
    group.add_argument('--apk', type=Path, help='APK containing assets/res/map/<id>.map.ref')
    parser.add_argument('--map-id', type=int, default=58)


def get_ref(args: argparse.Namespace):
    if args.ref is None and args.apk is None:
        return None, None
    data, source = read_map_ref(args.ref, args.apk, args.map_id)
    return inspect_map_ref(data), source


def template_command(args: argparse.Namespace) -> None:
    ref, source = get_ref(args)
    definition = args.tile
    if ref is not None and not 0 <= definition < ref.composite_tile_count:
        raise MapOError(f'--tile must be within 0..{ref.composite_tile_count - 1}')
    spec = {
        '_comment': 'tiles use local definition indexes; null means no ground tile; # means enabled bit',
        'map_id': args.map_id,
        'map_ref': source,
        'width': args.width,
        'height': args.height,
        'map_type': args.map_type,
        'tile_pixel_width': 20,
        'tile_pixel_height': 10,
        'tile_definitions': [definition],
        'tiles': [[0 for _ in range(args.width)] for _ in range(args.height)],
        'collision': ['.' * args.width for _ in range(args.height)],
        'mirror': ['.' * args.width for _ in range(args.height)],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(spec, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'wrote template: {args.output}')
    if ref is not None:
        print(
            f'map.ref: composite_tiles={ref.composite_tile_count} '
            f'image_records={ref.image_record_count} unique_images={len(set(ref.image_ids))} '
            f'bytes={ref.total_bytes}'
        )


def build_command(args: argparse.Namespace) -> None:
    result = MapO.from_spec(load_spec(args.spec))
    ref, source = get_ref(args)
    result.validate(ref)
    data = result.to_file()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(data)
    print(
        f'wrote {args.output}: {len(data)} bytes, {result.width}x{result.height}, '
        f'{len(result.tile_definitions)} definitions'
    )
    if ref is not None:
        print(f'validated against {source}: {ref.composite_tile_count} composite tiles')


def inspect_command(args: argparse.Namespace) -> None:
    result = MapO.from_file(args.input.read_bytes())
    ref, source = get_ref(args)
    result.validate(ref)
    summary = {
        'file': str(args.input),
        'size': args.input.stat().st_size,
        'width': result.width,
        'height': result.height,
        'map_type': result.map_type,
        'tile_pixel_width': result.tile_pixel_width,
        'tile_pixel_height': result.tile_pixel_height,
        'tile_definitions': result.tile_definitions,
        'empty_cells': sum(value == -1 for value in result.tiles),
        'blocked_cells': sum(result.collision),
        'mirrored_cells': sum(result.mirror),
        'map_ref': source,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if args.dump_spec is not None:
        args.dump_spec.write_text(json.dumps(result.to_spec(), ensure_ascii=False, indent=2), encoding='utf-8')
        print(f'wrote specification: {args.dump_spec}')


def main() -> None:
    parser = argparse.ArgumentParser(description='Generate and validate Piao Miao San Jie 2 .map.o files')
    commands = parser.add_subparsers(dest='command', required=True)

    template = commands.add_parser('template', help='Create an editable JSON map specification')
    template.add_argument('--width', type=int, required=True)
    template.add_argument('--height', type=int, required=True)
    template.add_argument('--map-type', type=int, default=0)
    template.add_argument('--tile', type=int, default=0, help='Initial map.ref composite tile index')
    template.add_argument('-o', '--output', type=Path, required=True)
    add_ref_arguments(template)
    template.set_defaults(function=template_command)

    build = commands.add_parser('build', help='Build .map.o from an editable JSON specification')
    build.add_argument('spec', type=Path)
    build.add_argument('-o', '--output', type=Path, required=True)
    add_ref_arguments(build)
    build.set_defaults(function=build_command)

    inspect = commands.add_parser('inspect', help='Validate and summarize a generated .map.o')
    inspect.add_argument('input', type=Path)
    inspect.add_argument('--dump-spec', type=Path)
    add_ref_arguments(inspect)
    inspect.set_defaults(function=inspect_command)

    args = parser.parse_args()
    try:
        args.function(args)
    except (MapOError, OSError, ValueError) as exc:
        parser.error(str(exc))


if __name__ == '__main__':
    main()
