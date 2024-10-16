"""empty message

Revision ID: 8cdca92898c6
Revises: 
Create Date: 2024-10-11 16:35:18.536016

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8cdca92898c6"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "click",
        sa.Column("short_path", sa.VARCHAR(length=8), nullable=False),
        sa.Column("query_params", sa.JSON(), nullable=False),
        sa.Column("headers", sa.JSON(), nullable=False),
        sa.Column("cookies", sa.JSON(), nullable=False),
        sa.Column("success", sa.Boolean(), nullable=False),
        sa.Column("user_agent_device_family", sa.String(), nullable=False),
        sa.Column("user_agent_device_brand", sa.String(), nullable=False),
        sa.Column("user_agent_device_model", sa.String(), nullable=False),
        sa.Column("user_agent_os_family", sa.String(), nullable=False),
        sa.Column("user_agent_os_version", sa.String(), nullable=False),
        sa.Column("user_agent_browser_family", sa.String(), nullable=False),
        sa.Column("user_agent_browser_version", sa.String(), nullable=False),
        sa.Column("user_agent_is_pc", sa.Boolean(), nullable=False),
        sa.Column("user_agent_is_mobile", sa.Boolean(), nullable=False),
        sa.Column("user_agent_is_tablet", sa.Boolean(), nullable=False),
        sa.Column("user_agent_is_touch_capable", sa.Boolean(), nullable=False),
        sa.Column("user_agent_is_bot", sa.Boolean(), nullable=False),
        sa.Column("user_agent_is_email_client", sa.Boolean(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "date",
            sa.DateTime(timezone=True),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "shorturl",
        sa.Column("short_path", sa.VARCHAR(length=8), nullable=False),
        sa.Column("full_url", sa.String(), nullable=False),
        sa.Column("meta", sa.JSON(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "date",
            sa.DateTime(timezone=True),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_shorturl_short_path"), "shorturl", ["short_path"], unique=False
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_shorturl_short_path"), table_name="shorturl")
    op.drop_table("shorturl")
    op.drop_table("click")
    # ### end Alembic commands ###
