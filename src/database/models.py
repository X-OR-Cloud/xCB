"""
src/database/models.py — Toàn bộ SQLAlchemy ORM models cho xHR
6 module: A-HR Profiles, B-Training, C-Export Pipeline, D-Finance, E-Internal HR, F-Seafarers + Audit
"""
import enum
from datetime import datetime, date
from typing import Optional

from sqlalchemy import (
    BigInteger, Boolean, Column, Date, DateTime, Enum,
    ForeignKey, Integer, Numeric, String, Text,
    func,
)
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


# ─────────────────────────────────────────────
# A — HR Profiles
# ─────────────────────────────────────────────

class TinhTrangLaoDong(str, enum.Enum):
    dang_xu_ly = "dang_xu_ly"
    da_xuat_canh = "da_xuat_canh"
    da_ve_nuoc = "da_ve_nuoc"
    cho_xuat_canh = "cho_xuat_canh"
    huy = "huy"


class LaoDong(Base):
    """Hồ sơ lao động xuất khẩu."""
    __tablename__ = "lao_dong"

    id = Column(Integer, primary_key=True, index=True)
    ho_ten = Column(String(200), nullable=False)
    ngay_sinh = Column(Date)
    so_cmnd = Column(String(20), unique=True)
    so_ho_chieu = Column(String(20), unique=True)
    so_dien_thoai = Column(String(20))
    dia_chi = Column(Text)
    thi_truong = Column(String(50))          # nhat_ban | han_quoc | dai_loan | ...
    tinh_trang = Column(Enum(TinhTrangLaoDong), default=TinhTrangLaoDong.dang_xu_ly)
    ngay_tao = Column(DateTime(timezone=True), server_default=func.now())
    ngay_cap_nhat = Column(DateTime(timezone=True), onupdate=func.now())

    ho_so_phap_ly = relationship("HoSoPhapLy", back_populates="lao_dong", cascade="all, delete-orphan")
    pipeline_tien_do = relationship("PipelineTienDo", back_populates="lao_dong", cascade="all, delete-orphan")
    hop_dong = relationship("HopDong", back_populates="lao_dong")


class LoaiGiayTo(str, enum.Enum):
    ho_chieu = "ho_chieu"
    visa = "visa"
    cmnd_cccd = "cmnd_cccd"
    giay_kham_suc_khoe = "giay_kham_suc_khoe"
    chung_chi = "chung_chi"
    khac = "khac"


class HoSoPhapLy(Base):
    """Hồ sơ pháp lý đính kèm theo lao động."""
    __tablename__ = "ho_so_phap_ly"

    id = Column(Integer, primary_key=True, index=True)
    lao_dong_id = Column(Integer, ForeignKey("lao_dong.id"), nullable=False)
    loai_giay_to = Column(Enum(LoaiGiayTo), nullable=False)
    so_giay_to = Column(String(50))
    ngay_cap = Column(Date)
    ngay_het_han = Column(Date)
    ghi_chu = Column(Text)
    ngay_tao = Column(DateTime(timezone=True), server_default=func.now())

    lao_dong = relationship("LaoDong", back_populates="ho_so_phap_ly")


# ─────────────────────────────────────────────
# B — Training
# ─────────────────────────────────────────────

class TinhTrangLopHoc(str, enum.Enum):
    mo = "mo"
    dang_hoc = "dang_hoc"
    ket_thuc = "ket_thuc"
    huy = "huy"


class LopHoc(Base):
    """Lớp đào tạo."""
    __tablename__ = "lop_hoc"

    id = Column(Integer, primary_key=True, index=True)
    ten_lop = Column(String(200), nullable=False)
    mon_hoc = Column(String(100))
    giao_vien = Column(String(100))
    ngay_bat_dau = Column(Date)
    ngay_ket_thuc = Column(Date)
    phong_hoc = Column(String(50))
    si_so_toi_da = Column(Integer, default=30)
    tinh_trang = Column(Enum(TinhTrangLopHoc), default=TinhTrangLopHoc.mo)
    ngay_tao = Column(DateTime(timezone=True), server_default=func.now())

    hoc_vien_lop = relationship("HocVienLop", back_populates="lop_hoc", cascade="all, delete-orphan")
    diem_danh = relationship("DiemDanh", back_populates="lop_hoc", cascade="all, delete-orphan")


class HocVienLop(Base):
    """Học viên đăng ký lớp học."""
    __tablename__ = "hoc_vien_lop"

    id = Column(Integer, primary_key=True, index=True)
    lop_hoc_id = Column(Integer, ForeignKey("lop_hoc.id"), nullable=False)
    lao_dong_id = Column(Integer, ForeignKey("lao_dong.id"), nullable=False)
    ngay_dang_ky = Column(Date, server_default=func.current_date())
    diem_cuoi_khoa = Column(Numeric(5, 2))
    xep_loai = Column(String(20))
    ghi_chu = Column(Text)

    lop_hoc = relationship("LopHoc", back_populates="hoc_vien_lop")


class DiemDanh(Base):
    """Điểm danh từng buổi học."""
    __tablename__ = "diem_danh"

    id = Column(Integer, primary_key=True, index=True)
    lop_hoc_id = Column(Integer, ForeignKey("lop_hoc.id"), nullable=False)
    lao_dong_id = Column(Integer, ForeignKey("lao_dong.id"), nullable=False)
    ngay = Column(Date, nullable=False)
    co_mat = Column(Boolean, default=False)
    phut_tre = Column(Integer, default=0)
    ghi_chu = Column(Text)

    lop_hoc = relationship("LopHoc", back_populates="diem_danh")


# ─────────────────────────────────────────────
# C — Export Pipeline
# ─────────────────────────────────────────────

class PipelineTemplate(Base):
    """Mẫu quy trình xuất khẩu cho từng thị trường."""
    __tablename__ = "pipeline_template"

    id = Column(Integer, primary_key=True, index=True)
    ten_template = Column(String(200), nullable=False)
    thi_truong = Column(String(50), nullable=False)
    cac_buoc = Column(Text)   # JSON string: list[{thu_tu, ten_buoc, mo_ta, so_ngay_du_kien}]
    ngay_tao = Column(DateTime(timezone=True), server_default=func.now())

    tien_do = relationship("PipelineTienDo", back_populates="template")


class TinhTrangBuoc(str, enum.Enum):
    chua_bat_dau = "chua_bat_dau"
    dang_thuc_hien = "dang_thuc_hien"
    hoan_thanh = "hoan_thanh"
    bi_loi = "bi_loi"


class PipelineTienDo(Base):
    """Tiến độ pipeline cho từng lao động."""
    __tablename__ = "pipeline_tien_do"

    id = Column(Integer, primary_key=True, index=True)
    lao_dong_id = Column(Integer, ForeignKey("lao_dong.id"), nullable=False)
    template_id = Column(Integer, ForeignKey("pipeline_template.id"), nullable=False)
    buoc_hien_tai = Column(Integer, default=1)
    tinh_trang_buoc = Column(Enum(TinhTrangBuoc), default=TinhTrangBuoc.chua_bat_dau)
    ngay_bat_dau = Column(Date)
    ngay_du_kien_hoan_thanh = Column(Date)
    ghi_chu = Column(Text)
    ngay_cap_nhat = Column(DateTime(timezone=True), onupdate=func.now())

    lao_dong = relationship("LaoDong", back_populates="pipeline_tien_do")
    template = relationship("PipelineTemplate", back_populates="tien_do")


# ─────────────────────────────────────────────
# D — Finance
# ─────────────────────────────────────────────

class TinhTrangHopDong(str, enum.Enum):
    nhap = "nhap"
    hieu_luc = "hieu_luc"
    het_han = "het_han"
    huy = "huy"


class HopDong(Base):
    """Hợp đồng xuất khẩu lao động."""
    __tablename__ = "hop_dong"

    id = Column(Integer, primary_key=True, index=True)
    lao_dong_id = Column(Integer, ForeignKey("lao_dong.id"), nullable=False)
    so_hop_dong = Column(String(50), unique=True)
    ngay_ky = Column(Date)
    ngay_het_han = Column(Date)
    tong_gia_tri = Column(Numeric(15, 2))
    tien_te = Column(String(10), default="VND")
    tinh_trang = Column(Enum(TinhTrangHopDong), default=TinhTrangHopDong.nhap)
    ghi_chu = Column(Text)
    ngay_tao = Column(DateTime(timezone=True), server_default=func.now())

    lao_dong = relationship("LaoDong", back_populates="hop_dong")
    phi_thanh_toan = relationship("PhiVaThanhToan", back_populates="hop_dong", cascade="all, delete-orphan")


class LoaiPhi(str, enum.Enum):
    phi_moi_gioi = "phi_moi_gioi"
    phi_dao_tao = "phi_dao_tao"
    phi_visa = "phi_visa"
    phi_ho_chieu = "phi_ho_chieu"
    phi_kham_suc_khoe = "phi_kham_suc_khoe"
    phi_khac = "phi_khac"


class TinhTrangThanhToan(str, enum.Enum):
    chua_thanh_toan = "chua_thanh_toan"
    da_thanh_toan = "da_thanh_toan"
    qua_han = "qua_han"


class PhiVaThanhToan(Base):
    """Chi tiết phí và trạng thái thanh toán."""
    __tablename__ = "phi_va_thanh_toan"

    id = Column(Integer, primary_key=True, index=True)
    hop_dong_id = Column(Integer, ForeignKey("hop_dong.id"), nullable=False)
    loai_phi = Column(Enum(LoaiPhi), nullable=False)
    so_tien = Column(Numeric(15, 2), nullable=False)
    tien_te = Column(String(10), default="VND")
    ngay_den_han = Column(Date)
    ngay_thanh_toan = Column(Date)
    tinh_trang = Column(Enum(TinhTrangThanhToan), default=TinhTrangThanhToan.chua_thanh_toan)
    ghi_chu = Column(Text)
    ngay_tao = Column(DateTime(timezone=True), server_default=func.now())

    hop_dong = relationship("HopDong", back_populates="phi_thanh_toan")


# ─────────────────────────────────────────────
# E — Internal HR
# ─────────────────────────────────────────────

class VaiTro(str, enum.Enum):
    nhan_vien = "nhan_vien"
    truong_phong = "truong_phong"
    giam_doc = "giam_doc"
    tgd = "tgd"


class PhongBan(str, enum.Enum):
    nhat_ban = "nhat_ban"
    thuy_en_vien = "thuy_en_vien"
    han_quoc = "han_quoc"
    dao_tao = "dao_tao"
    hanh_chinh = "hanh_chinh"
    ke_toan = "ke_toan"
    lanh_dao = "lanh_dao"
    tgd = "tgd"


class NhanVien(Base):
    """Nhân viên nội bộ Thinh Long Group — cột telegram_user_id để map với Telegram."""
    __tablename__ = "nhan_vien"

    id = Column(Integer, primary_key=True, index=True)
    ho_ten = Column(String(200), nullable=False)
    email = Column(String(200), unique=True)
    so_dien_thoai = Column(String(20))
    phong_ban = Column(Enum(PhongBan), nullable=False)
    vai_tro = Column(Enum(VaiTro), default=VaiTro.nhan_vien)
    telegram_user_id = Column(BigInteger, unique=True, index=True)   # Telegram identity mapping
    dang_lam_viec = Column(Boolean, default=True)
    ngay_tao = Column(DateTime(timezone=True), server_default=func.now())

    trinh_ky = relationship("TrinhKy", back_populates="nguoi_duyet", foreign_keys="TrinhKy.nguoi_duyet_id")


class TinhTrangTrinhKy(str, enum.Enum):
    cho_duyet = "cho_duyet"
    da_duyet = "da_duyet"
    tu_choi = "tu_choi"
    het_han = "het_han"


class TrinhKy(Base):
    """Quy trình trình ký / phê duyệt nội bộ."""
    __tablename__ = "trinh_ky"

    id = Column(Integer, primary_key=True, index=True)
    ten_viec = Column(String(300), nullable=False)
    mo_ta = Column(Text)
    nguoi_yeu_cau_id = Column(Integer, ForeignKey("nhan_vien.id"), nullable=False)
    nguoi_duyet_id = Column(Integer, ForeignKey("nhan_vien.id"), nullable=False)
    han_duyet = Column(DateTime(timezone=True))
    tinh_trang = Column(Enum(TinhTrangTrinhKy), default=TinhTrangTrinhKy.cho_duyet)
    ghi_chu_duyet = Column(Text)
    ngay_tao = Column(DateTime(timezone=True), server_default=func.now())
    ngay_cap_nhat = Column(DateTime(timezone=True), onupdate=func.now())

    nguoi_duyet = relationship("NhanVien", back_populates="trinh_ky", foreign_keys=[nguoi_duyet_id])


# ─────────────────────────────────────────────
# F — Seafarers
# ─────────────────────────────────────────────

class TinhTrangDonHang(str, enum.Enum):
    mo = "mo"
    dang_tuyen = "dang_tuyen"
    da_du = "da_du"
    huy = "huy"


class ThuyEnVienDonHang(Base):
    """Đơn hàng thuyền viên từ chủ tàu nước ngoài."""
    __tablename__ = "thuy_en_vien_don_hang"

    id = Column(Integer, primary_key=True, index=True)
    ten_don_hang = Column(String(300), nullable=False)
    ten_chu_tau = Column(String(200))
    quoc_gia = Column(String(100))
    ten_tau = Column(String(200))
    loai_tau = Column(String(100))
    so_luong_can = Column(Integer, default=1)
    vi_tri = Column(String(100))          # chuc_danh trên tàu
    muc_luong_usd = Column(Numeric(10, 2))
    thoi_gian_hop_dong_thang = Column(Integer)
    yeu_cau_bang_cap = Column(Text)
    ngay_khoi_hanh_du_kien = Column(Date)
    tinh_trang = Column(Enum(TinhTrangDonHang), default=TinhTrangDonHang.mo)
    ghi_chu = Column(Text)
    ngay_tao = Column(DateTime(timezone=True), server_default=func.now())


# ─────────────────────────────────────────────
# Audit Log
# ─────────────────────────────────────────────

class AuditLog(Base):
    """Ghi log mọi hành động của agent."""
    __tablename__ = "audit_log"

    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(String(50))            # MOLTY-NB, MOLTY-TV, ...
    nhan_vien_id = Column(Integer, ForeignKey("nhan_vien.id"), nullable=True)
    telegram_user_id = Column(BigInteger)
    hanh_dong = Column(String(300), nullable=False)
    du_lieu_dau_vao = Column(Text)
    ket_qua = Column(Text)
    thanh_cong = Column(Boolean, default=True)
    thoi_gian = Column(DateTime(timezone=True), server_default=func.now())
