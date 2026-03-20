"""
src/database/models.py — SQLAlchemy ORM models cho xCB Platform
Chuyển đổi từ xHR sang Nền tảng AI Công chức địa phương
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
# Lĩnh vực hành chính công
# ─────────────────────────────────────────────

class LinhVuc(str, enum.Enum):
    phap_ly = "phap_ly"
    giao_duc = "giao_duc"
    bao_hiem = "bao_hiem"
    tai_nguyen = "tai_nguyen"
    nong_nghiep = "nong_nghiep"
    cong_nghiep = "cong_nghiep"
    hanh_chinh = "hanh_chinh"
    doanh_nghiep = "doanh_nghiep"
    giam_sat = "giam_sat"


class CapDonVi(str, enum.Enum):
    tinh = "tinh"
    huyen = "huyen"
    xa = "xa"


# ─────────────────────────────────────────────
# Cán bộ & Nhân sự
# ─────────────────────────────────────────────

class VaiTro(str, enum.Enum):
    can_bo = "can_bo"
    truong_phong = "truong_phong"
    lanh_dao = "lanh_dao"
    quan_tri = "quan_tri"


class CanBo(Base):
    """Bảng cán bộ công chức (thay thế NhanVien)."""
    __tablename__ = "can_bo"

    id = Column(Integer, primary_key=True, index=True)
    ho_ten = Column(String(200), nullable=False)
    email = Column(String(200), unique=True)
    so_dien_thoai = Column(String(20))
    don_vi = Column(String(200))
    cap_don_vi = Column(Enum(CapDonVi), default=CapDonVi.xa)
    linh_vuc = Column(Enum(LinhVuc), nullable=False)
    vai_tro = Column(Enum(VaiTro), default=VaiTro.can_bo)
    telegram_user_id = Column(BigInteger, unique=True, index=True)
    dang_cong_tac = Column(Boolean, default=True)
    ngay_tao = Column(DateTime(timezone=True), server_default=func.now())

    ho_so_giai_quyet = relationship("HoSoHanhChinh", back_populates="can_bo_xu_ly")


# ─────────────────────────────────────────────
# Thủ tục & Hồ sơ hành chính
# ─────────────────────────────────────────────

class TrangThaiHoSo(str, enum.Enum):
    tiep_nhan = "tiep_nhan"
    dang_xu_ly = "dang_xu_ly"
    hoan_thanh = "hoan_thanh"
    qua_han = "qua_han"
    bo_sung = "bo_sung"


class ThuTuc(Base):
    """Danh mục thủ tục hành chính."""
    __tablename__ = "thu_tuc"

    id = Column(Integer, primary_key=True, index=True)
    ma_thu_tuc = Column(String(50), unique=True, nullable=False)
    ten_thu_tuc = Column(String(500), nullable=False)
    linh_vuc = Column(Enum(LinhVuc), nullable=False)
    thoi_han_ngay = Column(Integer)  # Số ngày xử lý quy định
    phi_le_phi = Column(Numeric(15, 2), default=0)
    ngay_tao = Column(DateTime(timezone=True), server_default=func.now())


class HoSoHanhChinh(Base):
    """Quản lý hồ sơ hành chính nộp bởi người dân/doanh nghiệp."""
    __tablename__ = "ho_so_hanh_chinh"

    id = Column(Integer, primary_key=True, index=True)
    ma_ho_so = Column(String(50), unique=True, nullable=False)
    ten_nguoi_nop = Column(String(200), nullable=False)
    so_dienthoai_nop = Column(String(20))
    thu_tuc_id = Column(Integer, ForeignKey("thu_tuc.id"))
    can_bo_xu_ly_id = Column(Integer, ForeignKey("can_bo.id"))
    
    ngay_tiep_nhan = Column(DateTime(timezone=True), server_default=func.now())
    han_tra_ket_qua = Column(DateTime(timezone=True))
    ngay_hoan_thanh = Column(DateTime(timezone=True))
    trang_thai = Column(Enum(TrangThaiHoSo), default=TrangThaiHoSo.tiep_nhan)
    
    linh_vuc = Column(Enum(LinhVuc), nullable=False)
    ghi_chu = Column(Text)

    can_bo_xu_ly = relationship("CanBo", back_populates="ho_so_giai_quyet")


# ─────────────────────────────────────────────
# Kho tri thức & Tài liệu (Giữ nguyên cấu trúc nhưng đổi mapping)
# ─────────────────────────────────────────────

class TinhTrangTaiLieu(str, enum.Enum):
    cho_xu_ly = "cho_xu_ly"
    dang_ocr = "dang_ocr"
    dang_vector_hoa = "dang_vector_hoa"
    hoan_thanh = "hoan_thanh"
    loi = "loi"


class TaiLieu(Base):
    """Tài liệu nạp vào kho tri thức phục vụ RAG."""
    __tablename__ = "tai_lieu"

    id = Column(Integer, primary_key=True, index=True)
    ten_file = Column(String(300), nullable=False)
    dung_luong = Column(BigInteger)
    loai_file = Column(String(50))
    duong_dan_storage = Column(String(500))
    linh_vuc = Column(Enum(LinhVuc), nullable=True)
    tinh_trang = Column(Enum(TinhTrangTaiLieu), default=TinhTrangTaiLieu.cho_xu_ly)
    tien_do_ocr = Column(Integer, default=0)
    tien_do_vector = Column(Integer, default=0)
    ngay_tao = Column(DateTime(timezone=True), server_default=func.now())


class AuditLog(Base):
    """Ghi log hành động của AI Agents."""
    __tablename__ = "audit_log"

    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(String(50))
    can_bo_id = Column(Integer, ForeignKey("can_bo.id"), nullable=True)
    telegram_user_id = Column(BigInteger)
    hanh_dong = Column(String(300), nullable=False)
    du_lieu_dau_vao = Column(Text)
    ket_qua = Column(Text)
    thanh_cong = Column(Boolean, default=True)
    thoi_gian = Column(DateTime(timezone=True), server_default=func.now())
