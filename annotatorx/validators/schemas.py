from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class AnnotationItem(BaseModel):
	id: int | str
	payload: Dict[str, Any] = Field(default_factory=dict)
	meta: Dict[str, Any] = Field(default_factory=dict)


class AnnotationSet(BaseModel):
	version: int = 1
	items: List[AnnotationItem] = Field(default_factory=list)
