from app.modules.core import ALL_18_MODULES, CORE_AUDIT_MODULES, AuditOrchestrator
from app.schemas import Beat, GateStatus, ModuleResult, ScriptDraft


def draft():
    return ScriptDraft(
        topic="테스트 주제",
        core_promise="핵심 약속",
        unique_angle="차별화 관점",
        title_options=["테스트 제목"],
        beats=[Beat(id=1, purpose="hook", narration="테스트 훅")],
    )


def test_exactly_18_modules_registered():
    assert len(ALL_18_MODULES) == 18
    assert len(set(ALL_18_MODULES)) == 18


def test_core_audit_passes_when_all_scores_pass():
    def runner(name, _draft, _context):
        return ModuleResult(module=name, score=90, status=GateStatus.PASS)

    audit = AuditOrchestrator(runner=runner, threshold=75).run_core(draft())
    assert audit.overall_status == GateStatus.PASS
    assert audit.blocking_modules == []
    assert len(audit.results) == len(CORE_AUDIT_MODULES)


def test_core_audit_blocks_low_score():
    def runner(name, _draft, _context):
        score = 60 if name == "FACT_CHECK_MODULE" else 90
        return ModuleResult(module=name, score=score, status=GateStatus.PASS)

    audit = AuditOrchestrator(runner=runner, threshold=75).run_core(draft())
    assert "FACT_CHECK_MODULE" in audit.blocking_modules
