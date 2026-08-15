from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from app.schemas import AuditBundle, GateStatus, ModuleResult, ScriptDraft


CORE_AUDIT_MODULES = [
    "FACT_CHECK_MODULE",
    "COPYRIGHT_MODULE",
    "AD_SAFETY_MODULE",
    "RETENTION_MODULE",
    "MONETIZATION_MODULE",
    "ORIGINALITY_MODULE",
    "PRODUCTION_MODULE",
]

PRE_PRODUCTION_MODULES = [
    "TREND_TIMING_MODULE",
    "CHANNEL_STRATEGY_MODULE",
    "SEARCH_DISCOVERY_MODULE",
    "AUDIENCE_INTENT_MODULE",
    "INFORMATION_VALUE_MODULE",
    "TRUST_AUTHORITY_MODULE",
]

POST_SCRIPT_MODULES = [
    "EMOTIONAL_ARCH_MODULE",
    "SESSION_GROWTH_MODULE",
    "EXPERIMENTATION_MODULE",
    "CTR_PACKAGING_MODULE",
    "REWRITE_CONTROLLER",
]

ALL_18_MODULES = CORE_AUDIT_MODULES + PRE_PRODUCTION_MODULES + POST_SCRIPT_MODULES


class ModuleRunner(Protocol):
    def __call__(self, module: str, draft: ScriptDraft, context: dict) -> ModuleResult: ...


@dataclass
class AuditOrchestrator:
    runner: ModuleRunner
    threshold: int = 75

    def run_core(self, draft: ScriptDraft, context: dict | None = None) -> AuditBundle:
        context = context or {}
        results = [self.runner(name, draft, context) for name in CORE_AUDIT_MODULES]
        blocking = [
            result.module
            for result in results
            if result.status == GateStatus.BLOCK or result.score < self.threshold
        ]
        status = GateStatus.BLOCK if blocking else GateStatus.PASS
        return AuditBundle(results=results, overall_status=status, blocking_modules=blocking)
