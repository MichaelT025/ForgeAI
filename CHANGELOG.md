# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Model state resource (`solidworks://model/state`) providing document, feature, and sketch metadata.
- Viewport screenshot resource (`solidworks://viewport/screenshot`) that triggers an isometric/fit-to-view update.
- Unit tests for MCP resources in `tests/unit/test_resources.py`.
- Registration of resources in MCP server core.
- Feature operations tools: `extrude`, `fillet`, and `chamfer`.
