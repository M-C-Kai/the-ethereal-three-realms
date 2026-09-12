from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE_PATCH = Path(__file__).with_name('apply_task_server_integration.py')
PROTOCOL_TEST = ROOT / 'tests' / 'test_protocol.py'


def main() -> None:
    # Reuse the already-reviewed deterministic patch while replacing only the
    # 1145 ownership predicate.  The four-field task navigation packet and
    # gathering pathfinding packet share the same TLV type signature, so the
    # server must claim it only when the route resolves in the task catalog.
    source = BASE_PATCH.read_text(encoding='utf-8')
    old = (
        '        "                    and parse_task_1145_request(fields) is not None\\n"\n'
    )
    new = (
        '        "                    and self.task_runtime.matches_1145(fields)\\n"\n'
    )
    if source.count(old) != 1:
        raise RuntimeError('1145 integration predicate patch point is not unique')
    source = source.replace(old, new, 1)

    namespace = {
        '__name__': '__main__',
        '__file__': str(BASE_PATCH),
    }
    exec(compile(source, str(BASE_PATCH), 'exec'), namespace)

    # 1403 is now a real task protocol.  Keep the legacy empty-prefetch test
    # aligned with the remaining unavailable modules instead of requiring the
    # removed 1403 fallback.
    test_text = PROTOCOL_TEST.read_text(encoding='utf-8')
    old_expected = '        expected = {1403: 1, 1090: 0, 1153: 0, 1061: 3}\n'
    new_expected = '        expected = {1090: 0, 1153: 0, 1061: 3}\n'
    if test_text.count(old_expected) != 1:
        raise RuntimeError('legacy menu-prefetch expectation patch point is not unique')
    PROTOCOL_TEST.write_text(
        test_text.replace(old_expected, new_expected, 1),
        encoding='utf-8',
    )
    print('task server integration v2 applied')


if __name__ == '__main__':
    main()
