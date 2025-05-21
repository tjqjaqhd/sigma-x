# core.scheduler 모듈 사양

| 객체/함수 | 설명 |
|-----------|------|
| `SimpleScheduler` | 쓰레드를 이용해 주기적으로 작업을 실행하는 간단한 스케줄러 |
| `start_bot_scheduler(bot, interval_seconds)` | 봇을 일정 간격으로 실행하기 위한 헬퍼 함수 |
| `start_maintenance_tasks(bot)` | APScheduler로 일일/주간 작업을 등록 |
