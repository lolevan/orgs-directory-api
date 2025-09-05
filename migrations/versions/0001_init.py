from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0001_init"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "activities",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(255), nullable=False, unique=True),
        sa.Column(
            "parent_id",
            sa.Integer,
            sa.ForeignKey("activities.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("depth", sa.Integer, nullable=False, server_default="0"),
    )
    op.create_index("ix_activities_name", "activities", ["name"])
    op.create_check_constraint("ck_activity_depth", "activities", "depth <= 3")

    op.create_table(
        "buildings",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("address", sa.String(500), nullable=False),
        sa.Column("latitude", sa.Float, nullable=False),
        sa.Column("longitude", sa.Float, nullable=False),
    )
    op.create_index("ix_buildings_lat_lon", "buildings", ["latitude", "longitude"])

    op.create_table(
        "organizations",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(255), nullable=False, index=True),
        sa.Column(
            "building_id",
            sa.Integer,
            sa.ForeignKey("buildings.id", ondelete="CASCADE"),
            nullable=False,
        ),
    )

    op.create_table(
        "organization_phones",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column(
            "organization_id",
            sa.Integer,
            sa.ForeignKey("organizations.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("phone", sa.String(50), nullable=False),
    )
    op.create_index("ix_organization_phones_phone", "organization_phones", ["phone"])

    op.create_table(
        "organization_activities",
        sa.Column(
            "organization_id",
            sa.Integer,
            sa.ForeignKey("organizations.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column(
            "activity_id",
            sa.Integer,
            sa.ForeignKey("activities.id", ondelete="CASCADE"),
            primary_key=True,
        ),
    )


def downgrade() -> None:
    op.drop_table("organization_activities")
    op.drop_index("ix_organization_phones_phone", table_name="organization_phones")
    op.drop_table("organization_phones")
    op.drop_table("organizations")
    op.drop_index("ix_buildings_lat_lon", table_name="buildings")
    op.drop_table("buildings")
    op.drop_index("ix_activities_name", table_name="activities")
    op.drop_constraint("ck_activity_depth", "activities", type_="check")
    op.drop_table("activities")
