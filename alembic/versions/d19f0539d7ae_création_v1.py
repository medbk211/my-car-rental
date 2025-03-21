"""Création V1

Revision ID: d19f0539d7ae
Revises: 
Create Date: 2025-03-19 10:50:23.415758

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision: str = 'd19f0539d7ae'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('adminaudit',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('admin_id', sa.Integer(), nullable=False),
    sa.Column('action', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('target_id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('role', sa.Enum('ADMIN', 'USER', 'AGENCE', name='role'), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('first_name', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('last_name', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('birth_date', sa.Date(), nullable=True),
    sa.Column('téléphone', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_password'), 'user', ['password'], unique=False)
    op.create_index(op.f('ix_user_téléphone'), 'user', ['téléphone'], unique=False)
    op.create_table('activationcompte',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('token', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('date_creation', sa.DateTime(), nullable=False),
    sa.Column('date_expiration', sa.DateTime(), nullable=False),
    sa.Column('utilisateur_id', sa.Integer(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['utilisateur_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_activationcompte_date_creation'), 'activationcompte', ['date_creation'], unique=False)
    op.create_index(op.f('ix_activationcompte_date_expiration'), 'activationcompte', ['date_expiration'], unique=False)
    op.create_index(op.f('ix_activationcompte_is_active'), 'activationcompte', ['is_active'], unique=False)
    op.create_index(op.f('ix_activationcompte_token'), 'activationcompte', ['token'], unique=True)
    op.create_table('agence',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nom_agence', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('email', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('téléphone', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('adresse', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('status', sa.Enum('ACTIVE', 'INACTIVE', name='agencestatus'), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id')
    )
    op.create_index(op.f('ix_agence_email'), 'agence', ['email'], unique=False)
    op.create_index(op.f('ix_agence_nom_agence'), 'agence', ['nom_agence'], unique=False)
    op.create_table('passwordreset',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('utilisateur_id', sa.Integer(), nullable=False),
    sa.Column('token', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('date_creation', sa.DateTime(timezone=True), nullable=True),
    sa.Column('date_expiration', sa.DateTime(timezone=True), nullable=True),
    sa.Column('is_used', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['utilisateur_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('car',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('marque', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('moteur', sa.Enum('Essence', 'Diesel', 'Electrique', 'Hybride', name='moteur'), nullable=False),
    sa.Column('annee', sa.Integer(), nullable=False),
    sa.Column('prixParJour', sa.Integer(), nullable=False),
    sa.Column('disponibilité', sa.Boolean(), nullable=False),
    sa.Column('agence_id', sa.Integer(), nullable=False),
    sa.Column('transmission', sa.Enum('Automatique', 'Manuelle', name='transmission'), nullable=False),
    sa.Column('climatisation', sa.Boolean(), nullable=False),
    sa.Column('kilometrage', sa.Integer(), nullable=False),
    sa.Column('photo', sa.JSON(), nullable=True),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('garantie', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['agence_id'], ['agence.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('avis',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('note', sa.Integer(), nullable=True),
    sa.Column('commentaire', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('utilisateur_id', sa.Integer(), nullable=False),
    sa.Column('car_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['car_id'], ['car.id'], ),
    sa.ForeignKeyConstraint(['utilisateur_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('réservation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date_debut', sa.DateTime(), nullable=False),
    sa.Column('date_fin', sa.DateTime(), nullable=False),
    sa.Column('date_creation', sa.DateTime(), nullable=True),
    sa.Column('date_annulation', sa.DateTime(), nullable=True),
    sa.Column('utilisateur_id', sa.Integer(), nullable=False),
    sa.Column('car_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['car_id'], ['car.id'], ),
    sa.ForeignKeyConstraint(['utilisateur_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_réservation_car_id'), 'réservation', ['car_id'], unique=False)
    op.create_index(op.f('ix_réservation_date_debut'), 'réservation', ['date_debut'], unique=False)
    op.create_index(op.f('ix_réservation_date_fin'), 'réservation', ['date_fin'], unique=False)
    op.create_index(op.f('ix_réservation_utilisateur_id'), 'réservation', ['utilisateur_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_réservation_utilisateur_id'), table_name='réservation')
    op.drop_index(op.f('ix_réservation_date_fin'), table_name='réservation')
    op.drop_index(op.f('ix_réservation_date_debut'), table_name='réservation')
    op.drop_index(op.f('ix_réservation_car_id'), table_name='réservation')
    op.drop_table('réservation')
    op.drop_table('avis')
    op.drop_table('car')
    op.drop_table('passwordreset')
    op.drop_index(op.f('ix_agence_nom_agence'), table_name='agence')
    op.drop_index(op.f('ix_agence_email'), table_name='agence')
    op.drop_table('agence')
    op.drop_index(op.f('ix_activationcompte_token'), table_name='activationcompte')
    op.drop_index(op.f('ix_activationcompte_is_active'), table_name='activationcompte')
    op.drop_index(op.f('ix_activationcompte_date_expiration'), table_name='activationcompte')
    op.drop_index(op.f('ix_activationcompte_date_creation'), table_name='activationcompte')
    op.drop_table('activationcompte')
    op.drop_index(op.f('ix_user_téléphone'), table_name='user')
    op.drop_index(op.f('ix_user_password'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_table('adminaudit')
    # ### end Alembic commands ###
