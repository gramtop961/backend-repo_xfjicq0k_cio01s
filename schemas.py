"""
Database Schemas for SiMATA (Sistem Informasi Manajemen Aset & Tata Kelola)

Each Pydantic model represents a MongoDB collection. The collection name is the
lowercase of the class name.

Default collections:
- AssetCategory -> "assetcategory"
- Location -> "location"
- Department -> "department"
- Asset -> "asset"
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class AssetCategory(BaseModel):
    name: str = Field(..., description="Nama kategori aset")
    description: Optional[str] = Field(None, description="Deskripsi kategori")


class Location(BaseModel):
    name: str = Field(..., description="Nama lokasi/ruangan")
    address: Optional[str] = Field(None, description="Alamat lokasi")
    floor: Optional[str] = Field(None, description="Lantai/ruang detail")


class Department(BaseModel):
    name: str = Field(..., description="Nama Bagian/Bidang")
    contact_person: Optional[str] = Field(None, description="Kontak penanggung jawab")


class Asset(BaseModel):
    code: str = Field(..., description="Kode inventaris/nomor register unik")
    name: str = Field(..., description="Nama aset")
    category_id: str = Field(..., description="ID kategori aset")
    location_id: str = Field(..., description="ID lokasi aset")
    department_id: Optional[str] = Field(None, description="ID bagian/bidang pemilik")
    status: str = Field("aktif", description="Status aset: aktif, perbaikan, rusak, dihapus")
    condition: str = Field("baik", description="Kondisi aset: baru, baik, sedang, rusak")
    purchase_date: Optional[date] = Field(None, description="Tanggal perolehan")
    value: Optional[float] = Field(None, ge=0, description="Nilai perolehan (Rp)")
    description: Optional[str] = Field(None, description="Keterangan tambahan")
