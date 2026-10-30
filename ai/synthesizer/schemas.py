from pydantic import BaseModel, Field


class SQLBuilderAgentResponse(BaseModel):
    is_feasible: bool = Field(
        description="true only if a correct SELECT can be generated"
    )
    sql_query: str | None = Field(
        description="the SELECT query; MUST be null if is_feasible is false"
    )
    reason: str = Field(
        description="brief explanation of the decision or the SQL approach"
    )
    tables_used: list[str] = Field(
        description="tables/views referenced (empty if infeasible)"
    )
    assumptions: list[str] = Field(
        description="assumptions made to resolve ambiguity (may be [])"
    )
    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="How certain you are about this decision. Only use 1.0 if you are 100% certain.",
    )
    clarification_needed: str | None = Field(
        description="a concrete question for the user when infeasible due to ambiguity, else null"
    )
    warnings: list[str] = Field(
        description="full-table scan, cross join, likely empty result, approximate match used"
    )
