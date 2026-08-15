from __future__ import annotations

from enum import Enum
from typing import Any
from pydantic import BaseModel, ConfigDict, Field


class GateStatus(str, Enum):
    PASS = "pass"
    REVIEW = "review"
    BLOCK = "block"


class ModuleResult(BaseModel):
    model_config = ConfigDict(extra="forbid")
    module: str
    score: int = Field(ge=0, le=100)
    status: GateStatus = GateStatus.REVIEW
    reasons: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class ScriptConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")
    language: str = "ko-KR"
    target_duration_sec: int = Field(default=600, ge=30, le=7200)
    audit_threshold: int = Field(default=75, ge=0, le=100)
    max_rewrite_attempts: int = Field(default=3, ge=0, le=10)


class ContentBrief(BaseModel):
    model_config = ConfigDict(extra="forbid")
    topic: str = Field(min_length=2)
    audience: str = ""
    viewer_problem: str = ""
    viewer_desire: str = ""
    source_material: str = ""


class Beat(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: int = Field(ge=1)
    purpose: str
    narration: str
    target_sec: int = Field(default=30, ge=1)
    visual_direction: str = ""
    subtitle: str = ""
    tts_direction: str = ""
    retention_devices: list[str] = Field(default_factory=list)


class ScriptDraft(BaseModel):
    model_config = ConfigDict(extra="forbid")
    topic: str
    core_promise: str
    unique_angle: str
    title_options: list[str] = Field(default_factory=list)
    thumbnail_options: list[str] = Field(default_factory=list)
    beats: list[Beat] = Field(default_factory=list)
    cta: str = ""
    next_video_bridge: str = ""


class AuditBundle(BaseModel):
    model_config = ConfigDict(extra="forbid")
    results: list[ModuleResult] = Field(default_factory=list)
    overall_status: GateStatus = GateStatus.REVIEW
    blocking_modules: list[str] = Field(default_factory=list)


class RewriteDecision(BaseModel):
    model_config = ConfigDict(extra="forbid")
    rewrite_required: bool
    target_modules: list[str] = Field(default_factory=list)
    target_beats: list[int] = Field(default_factory=list)
    preserve_strengths: list[str] = Field(default_factory=list)
    rollback_if_regression: bool = True


class PipelineResult(BaseModel):
    model_config = ConfigDict(extra="forbid")
    status: GateStatus
    draft: ScriptDraft
    audit: AuditBundle
    rewrite: RewriteDecision
