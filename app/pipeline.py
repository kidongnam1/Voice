from __future__ import annotations

from dataclasses import dataclass, field

from app.modules.core import AuditOrchestrator
from app.schemas import GateStatus, PipelineResult, RewriteDecision, ScriptConfig, ScriptDraft


@dataclass
class ScriptPipeline:
    orchestrator: AuditOrchestrator
    config: ScriptConfig = field(default_factory=ScriptConfig)

    def evaluate(self, draft: ScriptDraft, context: dict | None = None) -> PipelineResult:
        audit = self.orchestrator.run_core(draft, context)
        targets = audit.blocking_modules
        rewrite = RewriteDecision(
            rewrite_required=bool(targets),
            target_modules=targets,
            rollback_if_regression=True,
        )
        return PipelineResult(
            status=GateStatus.PASS if not targets else GateStatus.REVIEW,
            draft=draft,
            audit=audit,
            rewrite=rewrite,
        )
