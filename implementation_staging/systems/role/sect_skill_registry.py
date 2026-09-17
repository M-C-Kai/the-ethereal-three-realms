"""战斗门派技能静态目录。

与 `systems.skill` 生活技能分离。默认读取
`data/catalog/sect_combat_skill_catalog.bundle.json`，该文件是七大门派
战斗技能数据库快照；可用 `tools/materialize_sect_skill_catalog.py` 解包成
普通 `sects.json` / `sect_skills.json` / `sect_skill_rules.json`。
"""
from __future__ import annotations

import base64
import gzip
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


class SectCombatSkillCatalogError(Exception):
    """Raised when the combat sect-skill catalog is invalid."""


@dataclass(frozen=True)
class CatalogRecord:
    """Small immutable record wrapper for catalog rows.

    The static database intentionally keeps many fields data-driven.  Exposing
    rows through attributes keeps call sites readable while preserving the
    original JSON shape in ``raw``.
    """

    raw: dict[str, Any]

    def __getattr__(self, name: str) -> Any:
        try:
            return self.raw[name]
        except KeyError as exc:
            raise AttributeError(name) from exc

    def get(self, key: str, default: Any = None) -> Any:
        return self.raw.get(key, default)

    def as_dict(self) -> dict[str, Any]:
        return dict(self.raw)


def _require_dict(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise SectCombatSkillCatalogError(f'{label} must be an object')
    return value


def _require_list(value: Any, label: str) -> list[Any]:
    if not isinstance(value, list):
        raise SectCombatSkillCatalogError(f'{label} must be a list')
    return value


def _decode_bundle(path: Path) -> dict[str, Any]:
    wrapper = _require_dict(json.loads(path.read_text(encoding='utf-8')), str(path))
    if wrapper.get('encoding') != 'gzip+base64+json':
        raise SectCombatSkillCatalogError(f'unsupported bundle encoding: {path}')
    payload = str(wrapper.get('payload', ''))
    try:
        raw_json = gzip.decompress(base64.b64decode(payload))
    except Exception as exc:  # pragma: no cover - exact decoding exception is unimportant
        raise SectCombatSkillCatalogError(f'cannot decode bundle: {path}: {exc}') from exc
    expected = str(wrapper.get('sha256_uncompressed_json', ''))
    actual = hashlib.sha256(raw_json).hexdigest()
    if expected and actual != expected:
        raise SectCombatSkillCatalogError(
            f'bundle checksum mismatch: expected {expected}, got {actual}'
        )
    return _require_dict(json.loads(raw_json.decode('utf-8')), 'decoded bundle')


class SectCombatSkillCatalog:
    """Data-driven catalog for seven-sect combat skills."""

    def __init__(self, data: dict[str, Any]) -> None:
        self.data = data
        self.sect_names: dict[int, str] = {}
        self.sect_skill_ids: dict[int, tuple[int, ...]] = {}
        self.skills: dict[int, CatalogRecord] = {}
        self.cast_rules: dict[int, CatalogRecord] = {}
        self.effects: dict[int, tuple[CatalogRecord, ...]] = {}
        self.status_effects: dict[str, CatalogRecord] = {}
        self.scaling_rules: dict[int, tuple[CatalogRecord, ...]] = {}
        self.relations: dict[int, tuple[CatalogRecord, ...]] = {}
        self.upgrade_rules: dict[int, CatalogRecord] = {}
        self.client_mappings: dict[int, CatalogRecord] = {}
        self._load()

    @classmethod
    def from_bundle_file(cls, path: Path) -> 'SectCombatSkillCatalog':
        return cls(_decode_bundle(path))

    @classmethod
    def from_plain_files(
        cls,
        sects_path: Path,
        skills_path: Path,
        rules_path: Path,
    ) -> 'SectCombatSkillCatalog':
        return cls({
            'sects': json.loads(sects_path.read_text(encoding='utf-8')),
            'sect_skills': json.loads(skills_path.read_text(encoding='utf-8')),
            'sect_skill_rules': json.loads(rules_path.read_text(encoding='utf-8')),
        })

    def _load(self) -> None:
        sects = _require_dict(self.data.get('sects'), 'sects')
        skill_catalog = _require_dict(self.data.get('sect_skills'), 'sect_skills')
        rules = _require_dict(self.data.get('sect_skill_rules'), 'sect_skill_rules')

        for raw in _require_list(sects.get('sects', []), 'sects.sects'):
            row = _require_dict(raw, 'sect')
            sect_id = int(row['sect_id'])
            if sect_id in self.sect_names:
                raise SectCombatSkillCatalogError(f'duplicate sect_id: {sect_id}')
            self.sect_names[sect_id] = str(row.get('name', ''))
            self.sect_skill_ids[sect_id] = tuple(int(v) for v in row.get('skill_ids', []))

        self.skills = self._records_by_int_id(
            skill_catalog.get('skills', []),
            id_field='skill_id',
            label='skills',
        )
        self.cast_rules = self._records_by_int_id(
            rules.get('cast_rules', []),
            id_field='skill_id',
            label='cast_rules',
        )
        self.status_effects = self._records_by_str_id(
            rules.get('status_effects', []),
            id_field='status_key',
            label='status_effects',
        )
        self.effects = self._group_records(
            rules.get('effects', []),
            id_field='effect_id',
            group_field='skill_id',
            label='effects',
            sort_fields=('effect_order', 'effect_id'),
        )
        self.scaling_rules = self._group_records(
            rules.get('scaling_rules', []),
            id_field='scaling_id',
            group_field='skill_id',
            label='scaling_rules',
        )
        self.relations = self._group_records(
            rules.get('relations', []),
            id_field='relation_id',
            group_field='skill_id',
            label='relations',
        )
        self.upgrade_rules = self._records_by_int_id(
            rules.get('upgrade_rules', []),
            id_field='skill_id',
            label='upgrade_rules',
        )
        self.client_mappings = self._records_by_int_id(
            rules.get('client_mappings', []),
            id_field='skill_id',
            label='client_mappings',
        )
        self._validate()

    def _records_by_int_id(
        self,
        rows: Any,
        *,
        id_field: str,
        label: str,
    ) -> dict[int, CatalogRecord]:
        result: dict[int, CatalogRecord] = {}
        for raw in _require_list(rows, label):
            row = _require_dict(raw, label)
            key = int(row[id_field])
            if key in result:
                raise SectCombatSkillCatalogError(f'duplicate {label}.{id_field}: {key}')
            result[key] = CatalogRecord(dict(row))
        return result

    def _records_by_str_id(
        self,
        rows: Any,
        *,
        id_field: str,
        label: str,
    ) -> dict[str, CatalogRecord]:
        result: dict[str, CatalogRecord] = {}
        for raw in _require_list(rows, label):
            row = _require_dict(raw, label)
            key = str(row[id_field])
            if key in result:
                raise SectCombatSkillCatalogError(f'duplicate {label}.{id_field}: {key}')
            result[key] = CatalogRecord(dict(row))
        return result

    def _group_records(
        self,
        rows: Any,
        *,
        id_field: str,
        group_field: str,
        label: str,
        sort_fields: tuple[str, ...] = (),
    ) -> dict[int, tuple[CatalogRecord, ...]]:
        seen: set[int] = set()
        grouped: dict[int, list[CatalogRecord]] = {}
        for raw in _require_list(rows, label):
            row = _require_dict(raw, label)
            row_id = int(row[id_field])
            if row_id in seen:
                raise SectCombatSkillCatalogError(f'duplicate {label}.{id_field}: {row_id}')
            seen.add(row_id)
            grouped.setdefault(int(row[group_field]), []).append(CatalogRecord(dict(row)))
        if sort_fields:
            return {
                key: tuple(sorted(values, key=lambda r: tuple(int(r.get(f, 0)) for f in sort_fields)))
                for key, values in grouped.items()
            }
        return {key: tuple(values) for key, values in grouped.items()}

    def _validate(self) -> None:
        skill_ids = set(self.skills)
        status_keys = set(self.status_effects)

        for skill_id, skill in self.skills.items():
            sect_id = int(skill.sect_id)
            if sect_id not in self.sect_names:
                raise SectCombatSkillCatalogError(
                    f'skill {skill_id} references unknown sect {sect_id}'
                )
            if skill_id not in self.sect_skill_ids.get(sect_id, ()):
                raise SectCombatSkillCatalogError(
                    f'skill {skill_id} not listed in sect {sect_id} skill_ids'
                )

        for sect_id, listed_skill_ids in self.sect_skill_ids.items():
            for skill_id in listed_skill_ids:
                skill = self.skills.get(skill_id)
                if skill is None:
                    raise SectCombatSkillCatalogError(
                        f'sect {sect_id} lists unknown skill {skill_id}'
                    )
                if int(skill.sect_id) != sect_id:
                    raise SectCombatSkillCatalogError(
                        f'sect {sect_id} lists skill {skill_id} from sect {skill.sect_id}'
                    )

        self._validate_skill_id_set('cast_rules', self.cast_rules)
        self._validate_skill_id_set('effects', self.effects)
        self._validate_skill_id_set('scaling_rules', self.scaling_rules)
        self._validate_skill_id_set('upgrade_rules', self.upgrade_rules)
        self._validate_skill_id_set('client_mappings', self.client_mappings)

        for effect in self._flatten(self.effects.values()):
            status_key = str(effect.get('status_key', ''))
            if status_key and status_key not in status_keys:
                raise SectCombatSkillCatalogError(
                    f'effect {effect.effect_id} references unknown status {status_key}'
                )

        for relation in self._flatten(self.relations.values()):
            skill_id = int(relation.skill_id)
            related_skill_id = int(relation.get('related_skill_id', 0))
            if skill_id not in skill_ids:
                raise SectCombatSkillCatalogError(
                    f'relation {relation.relation_id} references unknown skill {skill_id}'
                )
            if related_skill_id and related_skill_id not in skill_ids:
                raise SectCombatSkillCatalogError(
                    f'relation {relation.relation_id} references unknown related skill '
                    f'{related_skill_id}'
                )

    def _validate_skill_id_set(self, label: str, mapping: dict[int, Any]) -> None:
        missing = sorted(set(mapping) - set(self.skills))
        if missing:
            raise SectCombatSkillCatalogError(f'{label} references unknown skills: {missing}')

    def _flatten(self, groups: Iterable[Iterable[CatalogRecord]]) -> Iterable[CatalogRecord]:
        for group in groups:
            yield from group

    def skill(self, skill_id: int) -> CatalogRecord | None:
        return self.skills.get(int(skill_id))

    def skills_for_sect(
        self,
        sect_id: int,
        *,
        include_follow_up: bool = False,
    ) -> list[CatalogRecord]:
        result = [
            self.skills[skill_id]
            for skill_id in self.sect_skill_ids.get(int(sect_id), ())
            if skill_id in self.skills
        ]
        if not include_follow_up:
            result = [skill for skill in result if skill.skill_kind != 'follow_up']
        return sorted(result, key=lambda skill: (skill.tree_line, int(skill.tree_order), int(skill.skill_id)))

    def combat_skills(self, *, include_follow_up: bool = True) -> list[CatalogRecord]:
        result = list(self.skills.values())
        if not include_follow_up:
            result = [skill for skill in result if skill.skill_kind != 'follow_up']
        return sorted(result, key=lambda skill: int(skill.skill_id))

    def cast_rule(self, skill_id: int) -> CatalogRecord | None:
        return self.cast_rules.get(int(skill_id))

    def effects_for(self, skill_id: int) -> tuple[CatalogRecord, ...]:
        return self.effects.get(int(skill_id), ())

    def status(self, status_key: str) -> CatalogRecord | None:
        return self.status_effects.get(str(status_key))

    def scaling_for(
        self,
        skill_id: int,
        scaling_type: str | None = None,
    ) -> tuple[CatalogRecord, ...]:
        rules = self.scaling_rules.get(int(skill_id), ())
        if scaling_type is None:
            return rules
        return tuple(rule for rule in rules if rule.scaling_type == scaling_type)

    def relations_for(
        self,
        skill_id: int,
        relation_type: str | None = None,
    ) -> tuple[CatalogRecord, ...]:
        rules = self.relations.get(int(skill_id), ())
        if relation_type is None:
            return rules
        return tuple(rule for rule in rules if rule.relation_type == relation_type)

    def upgrade_rule(self, skill_id: int) -> CatalogRecord | None:
        return self.upgrade_rules.get(int(skill_id))

    def client_mapping(self, skill_id: int) -> CatalogRecord | None:
        return self.client_mappings.get(int(skill_id))


def default_sect_combat_skill_catalog() -> SectCombatSkillCatalog:
    catalog_root = Path(__file__).resolve().parents[2] / 'data' / 'catalog'
    bundle_path = catalog_root / 'sect_combat_skill_catalog.bundle.json'
    if bundle_path.exists():
        return SectCombatSkillCatalog.from_bundle_file(bundle_path)
    return SectCombatSkillCatalog.from_plain_files(
        catalog_root / 'sects.json',
        catalog_root / 'sect_skills.json',
        catalog_root / 'sect_skill_rules.json',
    )
