from __future__ import annotations

from pathlib import Path


SERVER = Path(__file__).resolve().parents[1] / 'server.py'


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f'{label}: expected exactly one match, got {count}')
    return text.replace(old, new, 1)


def main() -> None:
    text = SERVER.read_text(encoding='utf-8')

    text = replace_once(
        text,
        "    def handle_task_1403(\n"
        "        self,\n"
        "        role: dict[str, object],\n"
        "        fields: list[Field],\n"
        "        *,\n"
        "        today: str | None = None,\n"
        "    ) -> tuple[bytes, ...]:\n"
        "        result = self.task_runtime.handle_1403(role, fields, today=today)\n"
        "        if result.changed:\n"
        "            self.roles.save()\n"
        "        return result.frames\n\n"
        "    def handle_task_1145(\n",
        "    def handle_task_1403(\n"
        "        self,\n"
        "        role: dict[str, object],\n"
        "        fields: list[Field],\n"
        "        *,\n"
        "        now: int | float = 0,\n"
        "        today: str | None = None,\n"
        "    ) -> tuple[bytes, ...]:\n"
        "        result = self.task_runtime.handle_1403(role, fields, now=now, today=today)\n"
        "        if result.changed:\n"
        "            self.roles.save()\n"
        "        return result.frames\n\n"
        "    def is_known_pathfind_target(self, map_id: int, x: int, y: int) -> bool:\n"
        "        \"\"\"Allow the shared 1145 pathfinder to target gathers or task NPCs.\"\"\"\n"
        "        if self.task_runtime.matches_path_target(map_id, x, y):\n"
        "            return True\n"
        "        return any(\n"
        "            target.map_id == int(map_id)\n"
        "            and target.x == int(x)\n"
        "            and target.y == int(y)\n"
        "            for target in self.settings.life_registry.gather_targets\n"
        "        )\n\n"
        "    def handle_task_1145(\n",
        'task 1403 timing and shared path target helper',
    )

    text = replace_once(
        text,
        "                elif message_id == 1403 and active_role is not None:\n"
        "                    response_frames = self.handle_task_1403(active_role, fields)\n",
        "                elif message_id == 1403 and active_role is not None:\n"
        "                    response_frames = self.handle_task_1403(\n"
        "                        active_role, fields, now=time.time(),\n"
        "                    )\n",
        'pass real time to native task acceptance',
    )

    text = replace_once(
        text,
        "                    known = any(\n"
        "                        target.map_id == map_id and target.x == target_x and target.y == target_y\n"
        "                        for target in self.settings.life_registry.gather_targets\n"
        "                    )\n",
        "                    known = self.is_known_pathfind_target(map_id, target_x, target_y)\n",
        'allow task NPC coordinates through shared pathfinder',
    )

    text = replace_once(
        text,
        "                            'GATHER_REJECT user=%r pathfind map=%d tile=%d,%d reason=unknown_target',\n",
        "                            'PATHFIND_REJECT user=%r map=%d tile=%d,%d reason=unknown_target',\n",
        'make path rejection log generic',
    )

    SERVER.write_text(text, encoding='utf-8')
    print('native task minimum-flow server patch applied')


if __name__ == '__main__':
    main()
