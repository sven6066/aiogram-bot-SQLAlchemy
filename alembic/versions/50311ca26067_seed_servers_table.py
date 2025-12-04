"""seed_servers_table

Revision ID: 50311ca26067
Revises: cd119ccf50c8
Create Date: 2025-12-04 13:08:49.644845

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '50311ca26067'
down_revision: Union[str, Sequence[str], None] = 'cd119ccf50c8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    servers_table = sa.table(
        'servers',
        sa.column('name', sa.String),
        sa.column('admin_url', sa.String),
        sa.column('user_url', sa.String)
    )

    # Вставляем данные с помощью bulk_insert
    op.bulk_insert(
        servers_table,
        [
            {'name': 'Воронеж Блейд', 'admin_url': 'https://panel.pilot-gps.com/',
             'user_url': 'https://blade.pilot-gps.com/'},
            {'name': 'Москва Блейд', 'admin_url': 'https://adm.iglit.tech/', 'user_url': 'https://gps.iglit.tech/'},
            {'name': 'Москва Флойд', 'admin_url': 'https://adm.pilot-gps.com/', 'user_url': 'https://pilot-gps.com/'},
        ]
    )


def downgrade() -> None:
    """Downgrade schema."""
    pass
