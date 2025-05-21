# core.adaptation 모듈 사양

| 객체/함수 | 설명 |
|-----------|------|
| `RegimeDetector.detect(prices)` | 가격 배열을 받아 시장 국면(`bull` 또는 `bear`)을 반환합니다. |
| `ParamAdjuster.update_parameter(name, value)` | `strategy_param` 테이블에 전략 파라미터를 저장합니다. |
| `QualityAssessment.evaluate(returns)` | 수익률 목록을 받아 평균 수익률을 반환합니다. |
| `FeedbackMechanism.record(metric)` | 평가 지표를 내부 목록에 기록합니다. |

