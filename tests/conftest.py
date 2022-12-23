"""Pytest configuration."""
import pydantic

pydantic.BaseConfig.extra = pydantic.Extra.forbid
