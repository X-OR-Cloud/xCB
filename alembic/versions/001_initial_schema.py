"""initial_schema

Revision ID: 001
Revises:
Create Date: 2026-03-16 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ── lao_dong ──────────────────────────────────────────────────────────
    op.create_table('lao_dong',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('ho_ten', sa.String(length=200), nullable=False),
        sa.Column('ngay_sinh', sa.Date(), nullable=True),
        sa.Column('so_cmnd', sa.String(length=20), nullable=True),
        sa.Column('so_ho_chieu', sa.String(length=20), nullable=True),
        sa.Column('so_dien_thoai', sa.String(length=20), nullable=True),
        sa.Column('email', sa.String(length=200), nullable=True),
        sa.Column('dia_chi', sa.Text(), nullable=True),
        sa.Column('thi_truong', sa.String(length=50), nullable=True),
        sa.Column('tinh_trang', sa.Enum('dang_xu_ly','da_xuat_canh','da_ve_nuoc','cho_xuat_canh','huy', name='tinhtranglaodong'), nullable=True),
        sa.Column('ngay_tao', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('ngay_cap_nhat', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('so_cmnd'),
        sa.UniqueConstraint('so_ho_chieu'),
    )
    op.create_index(op.f('ix_lao_dong_id'), 'lao_dong', ['id'], unique=False)

    # ── ho_so_phap_ly ─────────────────────────────────────────────────────
    op.create_table('ho_so_phap_ly',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('lao_dong_id', sa.Integer(), nullable=False),
        sa.Column('loai_giay_to', sa.Enum('ho_chieu','visa','cmnd_cccd','giay_kham_suc_khoe','chung_chi','khac', name='loaigiayto'), nullable=False),
        sa.Column('so_giay_to', sa.String(length=50), nullable=True),
        sa.Column('ngay_cap', sa.Date(), nullable=True),
        sa.Column('ngay_het_han', sa.Date(), nullable=True),
        sa.Column('ghi_chu', sa.Text(), nullable=True),
        sa.Column('ngay_tao', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(['lao_dong_id'], ['lao_dong.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ho_so_phap_ly_id'), 'ho_so_phap_ly', ['id'], unique=False)

    # ── lop_hoc ───────────────────────────────────────────────────────────
    op.create_table('lop_hoc',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('ten_lop', sa.String(length=200), nullable=False),
        sa.Column('mon_hoc', sa.String(length=100), nullable=True),
        sa.Column('giao_vien', sa.String(length=100), nullable=True),
        sa.Column('ngay_bat_dau', sa.Date(), nullable=True),
        sa.Column('ngay_ket_thuc', sa.Date(), nullable=True),
        sa.Column('phong_hoc', sa.String(length=50), nullable=True),
        sa.Column('si_so_toi_da', sa.Integer(), nullable=True),
        sa.Column('tinh_trang', sa.Enum('mo','dang_hoc','ket_thuc','huy', name='tinhtranglophoc'), nullable=True),
        sa.Column('ngay_tao', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_lop_hoc_id'), 'lop_hoc', ['id'], unique=False)

    # ── hoc_vien_lop ──────────────────────────────────────────────────────
    op.create_table('hoc_vien_lop',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('lop_hoc_id', sa.Integer(), nullable=False),
        sa.Column('lao_dong_id', sa.Integer(), nullable=False),
        sa.Column('ngay_dang_ky', sa.Date(), server_default=sa.func.current_date(), nullable=True),
        sa.Column('diem_cuoi_khoa', sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column('xep_loai', sa.String(length=20), nullable=True),
        sa.Column('ghi_chu', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['lao_dong_id'], ['lao_dong.id'], ),
        sa.ForeignKeyConstraint(['lop_hoc_id'], ['lop_hoc.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_hoc_vien_lop_id'), 'hoc_vien_lop', ['id'], unique=False)

    # ── diem_danh ─────────────────────────────────────────────────────────
    op.create_table('diem_danh',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('lop_hoc_id', sa.Integer(), nullable=False),
        sa.Column('lao_dong_id', sa.Integer(), nullable=False),
        sa.Column('ngay', sa.Date(), nullable=False),
        sa.Column('co_mat', sa.Boolean(), nullable=True),
        sa.Column('phut_tre', sa.Integer(), nullable=True),
        sa.Column('ghi_chu', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['lao_dong_id'], ['lao_dong.id'], ),
        sa.ForeignKeyConstraint(['lop_hoc_id'], ['lop_hoc.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_diem_danh_id'), 'diem_danh', ['id'], unique=False)

    # ── pipeline_template ─────────────────────────────────────────────────
    op.create_table('pipeline_template',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('ten_template', sa.String(length=200), nullable=False),
        sa.Column('thi_truong', sa.String(length=50), nullable=False),
        sa.Column('cac_buoc', sa.Text(), nullable=True),
        sa.Column('ngay_tao', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_pipeline_template_id'), 'pipeline_template', ['id'], unique=False)

    # ── pipeline_tien_do ──────────────────────────────────────────────────
    op.create_table('pipeline_tien_do',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('lao_dong_id', sa.Integer(), nullable=False),
        sa.Column('template_id', sa.Integer(), nullable=False),
        sa.Column('buoc_hien_tai', sa.Integer(), nullable=True),
        sa.Column('tinh_trang_buoc', sa.Enum('chua_bat_dau','dang_thuc_hien','hoan_thanh','bi_loi', name='tinhtrangbuoc'), nullable=True),
        sa.Column('ngay_bat_dau', sa.Date(), nullable=True),
        sa.Column('ngay_du_kien_hoan_thanh', sa.Date(), nullable=True),
        sa.Column('ghi_chu', sa.Text(), nullable=True),
        sa.Column('ngay_cap_nhat', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['lao_dong_id'], ['lao_dong.id'], ),
        sa.ForeignKeyConstraint(['template_id'], ['pipeline_template.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_pipeline_tien_do_id'), 'pipeline_tien_do', ['id'], unique=False)

    # ── hop_dong ──────────────────────────────────────────────────────────
    op.create_table('hop_dong',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('lao_dong_id', sa.Integer(), nullable=False),
        sa.Column('so_hop_dong', sa.String(length=50), nullable=True),
        sa.Column('ngay_ky', sa.Date(), nullable=True),
        sa.Column('ngay_het_han', sa.Date(), nullable=True),
        sa.Column('tong_gia_tri', sa.Numeric(precision=15, scale=2), nullable=True),
        sa.Column('tien_te', sa.String(length=10), nullable=True),
        sa.Column('tinh_trang', sa.Enum('nhap','hieu_luc','het_han','huy', name='tinhtranghopdong'), nullable=True),
        sa.Column('ghi_chu', sa.Text(), nullable=True),
        sa.Column('ngay_tao', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(['lao_dong_id'], ['lao_dong.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('so_hop_dong')
    )
    op.create_index(op.f('ix_hop_dong_id'), 'hop_dong', ['id'], unique=False)

    # ── phi_va_thanh_toan ─────────────────────────────────────────────────
    op.create_table('phi_va_thanh_toan',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('hop_dong_id', sa.Integer(), nullable=False),
        sa.Column('loai_phi', sa.Enum('phi_moi_gioi','phi_dao_tao','phi_visa','phi_ho_chieu','phi_kham_suc_khoe','phi_khac', name='loaiphi'), nullable=False),
        sa.Column('so_tien', sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column('tien_te', sa.String(length=10), nullable=True),
        sa.Column('ngay_den_han', sa.Date(), nullable=True),
        sa.Column('ngay_thanh_toan', sa.Date(), nullable=True),
        sa.Column('tinh_trang', sa.Enum('chua_thanh_toan','da_thanh_toan','qua_han', name='tinhtrangthanhtoan'), nullable=True),
        sa.Column('ghi_chu', sa.Text(), nullable=True),
        sa.Column('ngay_tao', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(['hop_dong_id'], ['hop_dong.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_phi_va_thanh_toan_id'), 'phi_va_thanh_toan', ['id'], unique=False)

    # ── nhan_vien ─────────────────────────────────────────────────────────
    op.create_table('nhan_vien',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('ho_ten', sa.String(length=200), nullable=False),
        sa.Column('email', sa.String(length=200), nullable=True),
        sa.Column('so_dien_thoai', sa.String(length=20), nullable=True),
        sa.Column('phong_ban', sa.Enum('nhat_ban','thuy_en_vien','han_quoc','dao_tao','hanh_chinh','ke_toan','lanh_dao','tgd', name='phongban'), nullable=False),
        sa.Column('vai_tro', sa.Enum('nhan_vien','truong_phong','giam_doc','tgd', name='vaitro'), nullable=True),
        sa.Column('telegram_user_id', sa.BigInteger(), nullable=True),
        sa.Column('dang_lam_viec', sa.Boolean(), nullable=True),
        sa.Column('ngay_tao', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_nhan_vien_id'), 'nhan_vien', ['id'], unique=False)
    op.create_index(op.f('ix_nhan_vien_telegram_user_id'), 'nhan_vien', ['telegram_user_id'], unique=True)

    # ── trinh_ky ──────────────────────────────────────────────────────────
    op.create_table('trinh_ky',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('ten_viec', sa.String(length=300), nullable=False),
        sa.Column('mo_ta', sa.Text(), nullable=True),
        sa.Column('nguoi_yeu_cau_id', sa.Integer(), nullable=False),
        sa.Column('nguoi_duyet_id', sa.Integer(), nullable=False),
        sa.Column('han_duyet', sa.DateTime(timezone=True), nullable=True),
        sa.Column('tinh_trang', sa.Enum('cho_duyet','da_duyet','tu_choi','het_han', name='tinhtrangtrinh_ky'), nullable=True),
        sa.Column('ghi_chu_duyet', sa.Text(), nullable=True),
        sa.Column('ngay_tao', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('ngay_cap_nhat', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['nguoi_duyet_id'], ['nhan_vien.id'], ),
        sa.ForeignKeyConstraint(['nguoi_yeu_cau_id'], ['nhan_vien.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_trinh_ky_id'), 'trinh_ky', ['id'], unique=False)

    # ── thuy_en_vien_don_hang ─────────────────────────────────────────────
    op.create_table('thuy_en_vien_don_hang',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('ten_don_hang', sa.String(length=300), nullable=False),
        sa.Column('ten_chu_tau', sa.String(length=200), nullable=True),
        sa.Column('quoc_gia', sa.String(length=100), nullable=True),
        sa.Column('ten_tau', sa.String(length=200), nullable=True),
        sa.Column('loai_tau', sa.String(length=100), nullable=True),
        sa.Column('so_luong_can', sa.Integer(), nullable=True),
        sa.Column('vi_tri', sa.String(length=100), nullable=True),
        sa.Column('muc_luong_usd', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('thoi_gian_hop_dong_thang', sa.Integer(), nullable=True),
        sa.Column('yeu_cau_bang_cap', sa.Text(), nullable=True),
        sa.Column('ngay_khoi_hanh_du_kien', sa.Date(), nullable=True),
        sa.Column('tinh_trang', sa.Enum('mo','dang_tuyen','da_du','huy', name='tinhtrangdonhang'), nullable=True),
        sa.Column('ghi_chu', sa.Text(), nullable=True),
        sa.Column('ngay_tao', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_thuy_en_vien_don_hang_id'), 'thuy_en_vien_don_hang', ['id'], unique=False)

    # ── tai_lieu ──────────────────────────────────────────────────────────
    op.create_table('tai_lieu',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('ten_file', sa.String(length=300), nullable=False),
        sa.Column('dung_luong', sa.BigInteger(), nullable=True),
        sa.Column('loai_file', sa.String(length=50), nullable=True),
        sa.Column('duong_dan_storage', sa.String(length=500), nullable=True),
        sa.Column('phong_ban', sa.Enum('nhat_ban','thuy_en_vien','han_quoc','dao_tao','hanh_chinh','ke_toan','lanh_dao','tgd', name='phongban'), nullable=True),
        sa.Column('tinh_trang', sa.Enum('cho_xu_ly','dang_ocr','dang_vector_hoa','hoan_thanh','loi', name='tinhtrangtailieu'), nullable=True),
        sa.Column('tien_do_ocr', sa.Integer(), nullable=True),
        sa.Column('tien_do_vector', sa.Integer(), nullable=True),
        sa.Column('loi_nhan', sa.Text(), nullable=True),
        sa.Column('ngay_tao', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('ngay_cap_nhat', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tai_lieu_id'), 'tai_lieu', ['id'], unique=False)

    # ── audit_log ─────────────────────────────────────────────────────────
    op.create_table('audit_log',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('agent_id', sa.String(length=50), nullable=True),
        sa.Column('nhan_vien_id', sa.Integer(), nullable=True),
        sa.Column('telegram_user_id', sa.BigInteger(), nullable=True),
        sa.Column('hanh_dong', sa.String(length=300), nullable=False),
        sa.Column('du_lieu_dau_vao', sa.Text(), nullable=True),
        sa.Column('ket_qua', sa.Text(), nullable=True),
        sa.Column('thanh_cong', sa.Boolean(), nullable=True),
        sa.Column('thoi_gian', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(['nhan_vien_id'], ['nhan_vien.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_audit_log_id'), 'audit_log', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_audit_log_id'), table_name='audit_log')
    op.drop_table('audit_log')
    op.drop_index(op.f('ix_tai_lieu_id'), table_name='tai_lieu')
    op.drop_table('tai_lieu')
    op.drop_index(op.f('ix_thuy_en_vien_don_hang_id'), table_name='thuy_en_vien_don_hang')
    op.drop_table('thuy_en_vien_don_hang')
    op.drop_index(op.f('ix_trinh_ky_id'), table_name='trinh_ky')
    op.drop_table('trinh_ky')
    op.drop_index(op.f('ix_nhan_vien_telegram_user_id'), table_name='nhan_vien')
    op.drop_index(op.f('ix_nhan_vien_id'), table_name='nhan_vien')
    op.drop_table('nhan_vien')
    op.drop_index(op.f('ix_phi_va_thanh_toan_id'), table_name='phi_va_thanh_toan')
    op.drop_table('phi_va_thanh_toan')
    op.drop_index(op.f('ix_hop_dong_id'), table_name='hop_dong')
    op.drop_table('hop_dong')
    op.drop_index(op.f('ix_pipeline_tien_do_id'), table_name='pipeline_tien_do')
    op.drop_table('pipeline_tien_do')
    op.drop_index(op.f('ix_pipeline_template_id'), table_name='pipeline_template')
    op.drop_table('pipeline_template')
    op.drop_index(op.f('ix_diem_danh_id'), table_name='diem_danh')
    op.drop_table('diem_danh')
    op.drop_index(op.f('ix_hoc_vien_lop_id'), table_name='hoc_vien_lop')
    op.drop_table('hoc_vien_lop')
    op.drop_index(op.f('ix_lop_hoc_id'), table_name='lop_hoc')
    op.drop_table('lop_hoc')
    op.drop_index(op.f('ix_ho_so_phap_ly_id'), table_name='ho_so_phap_ly')
    op.drop_table('ho_so_phap_ly')
    op.drop_index(op.f('ix_lao_dong_id'), table_name='lao_dong')
    op.drop_table('lao_dong')
