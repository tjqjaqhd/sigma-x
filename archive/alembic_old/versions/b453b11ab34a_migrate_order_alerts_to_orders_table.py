"""migrate order alerts to orders table

Revision ID: b453b11ab34a
Revises: 
Create Date: 2025-05-22 05:23:31.592278

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b453b11ab34a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """alert 테이블의 주문 관련 데이터를 orders 테이블로 이전."""
    conn = op.get_bind()
    # type 컬럼이 없다면 message 내 '주문' 키워드 등으로 필터링
    # 예시: message LIKE '%주문%' 또는 message LIKE '%order%' 등
    # 실제 데이터에 맞게 조정 필요
    result = conn.execute(
        sa.text("""
            SELECT id, message, timestamp
            FROM alert
            WHERE message LIKE '%주문%' OR message LIKE '%order%'
        """))
    for row in result:
        # signal 추출 로직은 실제 message 포맷에 맞게 조정 필요
        # 여기서는 message 전체를 signal로 저장
        conn.execute(
            sa.text("""
                INSERT INTO orders (signal, status, timestamp)
                VALUES (:signal, 'MIGRATED', :timestamp)
            """),
            {"signal": row.message, "timestamp": row.timestamp}
        )


def downgrade() -> None:
    """orders 테이블에서 migration으로 추가된 데이터만 삭제."""
    conn = op.get_bind()
    # status='MIGRATED'로 구분
    conn.execute(sa.text("DELETE FROM orders WHERE status='MIGRATED'"))
