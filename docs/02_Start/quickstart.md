# Quickstart

1. Python 3.10+ 환경을 준비합니다.
2. 저장소를 클론하고 루트로 이동합니다.
3. (선택) 가상환경을 만들고 활성화합니다.
4. 예제를 실행하여 엔진 흐름을 확인합니다.

```bash
python examples/01_minimal_world.py
python examples/02_warrior_mage_priest.py
```

## pip로 설치하고 싶다면?

`pyproject.toml`을 이용해 추후 `pip install .` 형태의 설치를 지원할 예정입니다. 현재는 로컬 소스에서 바로 import 하도록 설계되어 있습니다.

## 다음 단계

- `docs/concepts.md`로 철학과 모델을 이해합니다.
- `elysia_engine/hooks`를 참고하여 Godot/웹/CLI 로그를 붙입니다.
- 자신의 세계관/게임/AI에 맞는 역할과 엔티티를 파생시킵니다.
