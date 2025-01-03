from sqlalchemy.orm import backref
from sqlalchemy.orm.properties import ForeignKey
from . import db
from flask_login import UserMixin


# pelajaran_kelas = db.Table( # MAPEL & KELAS JUNCTION TABEL
#     'pelajaran_kelas',
#     db.Column('kelas_id', db.Integer, db.ForeignKey('kelas.id'), primary_key=True),
#     db.Column('mapel_id', db.Integer, db.ForeignKey('mapel.id'), primary_key=True)
# )


# MAIN MODELS
class Account(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    profile = db.relationship("Profile", backref="account", uselist=False)


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama_lengkap = db.Column(db.String(100), nullable=True, default="")
    nip = db.Column(db.String(100), nullable=True, default="")
    account_id = db.Column(
        db.Integer, db.ForeignKey("account.id"), unique=True, nullable=False
    )


class TahunAjaran(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(50), nullable=False, unique=True)
    selected = db.Column(db.Boolean, nullable=False, default=False)
    nilai_lingkup_materi = db.relationship(
        "NilaiLingkupMateri", backref="nlk_th", lazy=True, cascade="all, delete"
    )
    nilai_tengah = db.relationship(
        "NilaiTengah", backref="nt_th", cascade="all, delete", lazy=True
    )
    nilai_akhir = db.relationship(
        "NilaiAkhir", backref="na_th", cascade="all, delete", lazy=True
    )
    ck = db.relationship(
        "CapaianKompetensi", backref="ck_th", cascade="all, delete", lazy=True
    )
    kd = db.relationship(
        "KompetensiDasar", backref="kd_th", cascade="all, delete", lazy=True
    )
    bobot = db.relationship(
        "BobotPenilaian", backref="bobot_th", cascade="all, delete", lazy=True
    )
    nilai_sumatif_lingkup_materi = db.relationship(
        "NilaiSumatifLingkupMateri", backref="nslk_th", cascade="all, delete", lazy=True
    )
    nilai_sumatif_tengah = db.relationship(
        "NilaiSumatifTengah", backref="nst_th", cascade="all, delete", lazy=True
    )
    nilai_sumatif_akhir = db.relationship(
        "NilaiSumatifAkhir", backref="nsa_th", cascade="all, delete", lazy=True
    )


class Semester(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(50), nullable=False, unique=True)
    selected = db.Column(db.Boolean, nullable=False, default=False)
    nilai_lingkup_materi = db.relationship(
        "NilaiLingkupMateri", backref="nlk_sm", lazy=True, cascade="all, delete"
    )
    nilai_tengah = db.relationship(
        "NilaiTengah", backref="nt_sm", cascade="all, delete", lazy=True
    )
    nilai_akhir = db.relationship(
        "NilaiAkhir", backref="na_sm", cascade="all, delete", lazy=True
    )
    ck = db.relationship(
        "CapaianKompetensi", backref="ck_sm", cascade="all, delete", lazy=True
    )
    kd = db.relationship(
        "KompetensiDasar", backref="kd_sm", cascade="all, delete", lazy=True
    )
    bobot = db.relationship(
        "BobotPenilaian", backref="bobot_sm", cascade="all, delete", lazy=True
    )
    nilai_sumatif_lingkup_materi = db.relationship(
        "NilaiSumatifLingkupMateri",
        backref="nslk_semester",
        cascade="all, delete",
        lazy=True,
    )
    nilai_sumatif_tengah = db.relationship(
        "NilaiSumatifTengah", backref="nst_sm", cascade="all, delete", lazy=True
    )
    nilai_sumatif_akhir = db.relationship(
        "NilaiSumatifAkhir", backref="nsa_sm", cascade="all, delete", lazy=True
    )


class Tingkat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(50), nullable=False, unique=True)
    anggota_tingkat = db.relationship("Kelas", backref="tingkat", lazy=True)
    murid_tingkat = db.relationship("Siswa", backref="kesetaraan", lazy=True)


# SISWA MODELS AND ITS RELATIONS
class Kelas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    wali_kelas = db.Column(db.String(50), nullable=True, default="")
    tingkat_id = db.Column(
        db.Integer,
        db.ForeignKey("tingkat.id", ondelete="SET NULL"),
        nullable=True,
    )
    mapel_kelas = db.relationship(
        "Mapel", backref="kelas", lazy=True, cascade="all, delete"
    )
    anggota_kelas = db.relationship("Siswa", backref="kelas_belajar", lazy=True)
    nlk_kelas = db.relationship("NilaiLingkupMateri", backref="nlk_kelas", lazy=True)
    nilai_sumatif_lingkup_materi = db.relationship(
        "NilaiSumatifLingkupMateri",
        backref="nslk_kelas",
        cascade="all, delete",
        lazy=True,
    )
    # mapel_kelas = db.relationship('Mapel', secondary=pelajaran_kelas, back_populates='kelas_diajar')


class Siswa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    nis = db.Column(db.String(50), nullable=True)
    nisn = db.Column(db.String(50), nullable=True, unique=True)
    tempat_lahir = db.Column(db.String(50), nullable=True)
    tgl_lahir = db.Column(db.String(50), nullable=True)
    alamat = db.Column(db.String(200), nullable=True)
    jenis_kelamin = db.Column(db.String(40), nullable=True)
    agama = db.Column(db.String(40), nullable=True)
    nama_ayah = db.Column(db.String(100), nullable=True)
    nama_ibu = db.Column(db.String(100), nullable=True)
    pekerjaan_ayah = db.Column(db.String(50), nullable=True)
    pekerjaan_ibu = db.Column(db.String(50), nullable=True)
    tingkat_kelas_id = db.Column(
        db.Integer, db.ForeignKey("tingkat.id", ondelete="SET NULL"), nullable=True
    )
    kelas_id = db.Column(
        db.Integer, db.ForeignKey("kelas.id", ondelete="SET NULL"), nullable=True
    )
    nilai_lingkup_materi = db.relationship(
        "NilaiLingkupMateri", backref="nlk_siswa", lazy=True, cascade="all, delete"
    )
    nilai_tengah = db.relationship(
        "NilaiTengah", backref="nt_siswa", cascade="all, delete", lazy=True
    )
    nilai_akhir = db.relationship(
        "NilaiAkhir", backref="na_siswa", cascade="all, delete", lazy=True
    )
    nilai_sumatif_lingkup_materi = db.relationship(
        "NilaiSumatifLingkupMateri",
        backref="nslk_siswa",
        cascade="all, delete",
        lazy=True,
    )
    nilai_sumatif_tengah = db.relationship(
        "NilaiSumatifTengah", backref="nst_siswa", cascade="all, delete", lazy=True
    )
    nilai_sumatif_akhir = db.relationship(
        "NilaiSumatifAkhir", backref="nsa_siswa", cascade="all, delete", lazy=True
    )


# MAPEL MODELS AND ITS RELATIONS
class KelompokMapel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    category = db.Column(db.String(100), nullable=False, default="Umum")
    anggota_kelompok = db.relationship("Mapel", backref="kelompok", lazy=True)


class Mapel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    kelas_id = db.Column(
        db.Integer, db.ForeignKey("kelas.id", ondelete="CASCADE"), nullable=True
    )
    # kelas_diajar = db.relationship('Kelas', secondary=pelajaran_kelas, back_populates='mapel_kelas')
    kelompok_id = db.Column(
        db.Integer,
        db.ForeignKey("kelompok_mapel.id", ondelete="SET NULL"),
        nullable=True,
    )
    kompetensi_dasar = db.relationship(
        "KompetensiDasar", backref="kd_mapel", lazy=True, cascade="all, delete"
    )
    capaian_kompetensi = db.relationship(
        "CapaianKompetensi", backref="mapel", lazy=True, cascade="all, delete"
    )
    bobot_penilaian = db.relationship(
        "BobotPenilaian",
        backref="mapel_terkait",
        lazy=True,
        cascade="all, delete",
        uselist=False,
    )
    nilai_lingkup_materi = db.relationship(
        "NilaiLingkupMateri", backref="nlk_mapel", lazy=True, cascade="all, delete"
    )
    nilai_sumatif_lingkup_materi = db.relationship(
        "NilaiSumatifLingkupMateri",
        backref="nslk_mapel",
        cascade="all, delete",
        lazy=True,
    )
    nilai_tengah = db.relationship(
        "NilaiTengah", backref="nt_mapel", cascade="all, delete", lazy=True
    )
    nilai_akhir = db.relationship(
        "NilaiAkhir", backref="na_mapel", cascade="all, delete", lazy=True
    )
    nilai_sumatif_tengah = db.relationship(
        "NilaiSumatifTengah", backref="nst_mapel", cascade="all, delete", lazy=True
    )
    nilai_sumatif_akhir = db.relationship(
        "NilaiSumatifAkhir", backref="nsa_mapel", cascade="all, delete", lazy=True
    )


class BobotPenilaian(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bobot_materi_p = db.Column(db.Integer, nullable=True)
    bobot_materi_k = db.Column(db.Integer, nullable=True)
    bobot_tengah = db.Column(db.Integer, nullable=True)
    bobot_akhir = db.Column(db.Integer, nullable=True)
    mapel_id = db.Column(
        db.Integer, db.ForeignKey("mapel.id", ondelete="CASCADE"), nullable=False
    )
    th_id = db.Column(
        db.Integer, db.ForeignKey("tahun_ajaran.id", ondelete="CASCADE"), nullable=False
    )
    sm_id = db.Column(
        db.Integer, db.ForeignKey("semester.id", ondelete="CASCADE"), nullable=False
    )


class CapaianKompetensi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String(500), nullable=True)
    mapel_id = db.Column(
        db.Integer, db.ForeignKey("mapel.id", ondelete="CASCADE"), nullable=True
    )
    kompetensi_dasar = db.relationship(
        "KompetensiDasar", backref="ck", lazy=True, cascade="all, delete"
    )
    th_id = db.Column(
        db.Integer, db.ForeignKey("tahun_ajaran.id", ondelete="CASCADE"), nullable=False
    )
    sm_id = db.Column(
        db.Integer, db.ForeignKey("semester.id", ondelete="CASCADE"), nullable=False
    )


class KompetensiDasar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String(500), nullable=True)
    mapel_id = db.Column(
        db.Integer, db.ForeignKey("mapel.id", ondelete="CASCADE"), nullable=True
    )
    th_id = db.Column(
        db.Integer, db.ForeignKey("tahun_ajaran.id", ondelete="CASCADE"), nullable=False
    )
    sm_id = db.Column(
        db.Integer, db.ForeignKey("semester.id", ondelete="CASCADE"), nullable=False
    )
    ck_id = db.Column(
        db.Integer,
        db.ForeignKey("capaian_kompetensi.id", ondelete="CASCADE"),
        nullable=True,
    )
    nilai = db.relationship(
        "NilaiLingkupMateri",
        backref="kd_source",
        cascade="all, delete",
        lazy=True,
    )
    # tujuan_pembelajaran = db.relationship('TujuanPembelajaran', backref='kd', lazy=True)


class NilaiLingkupMateri(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, nullable=False)
    tipe_nilai = db.Column(db.String(50), nullable=False)
    kd_id = db.Column(
        db.Integer,
        db.ForeignKey("kompetensi_dasar.id", ondelete="CASCADE"),
        nullable=False,
    )
    siswa_id = db.Column(
        db.Integer, db.ForeignKey("siswa.id", ondelete="CASCADE"), nullable=False
    )
    mapel_id = db.Column(
        db.Integer, db.ForeignKey("mapel.id", ondelete="CASCADE"), nullable=False
    )
    kelas_id = db.Column(db.ForeignKey("kelas.id", ondelete="SET NULL"), nullable=False)
    th_id = db.Column(
        db.Integer,
        db.ForeignKey("tahun_ajaran.id", ondelete="SET NULL"),
        nullable=False,
    )
    sm_id = db.Column(
        db.Integer, db.ForeignKey("semester.id", ondelete="SET NULL"), nullable=False
    )


class NilaiSumatifLingkupMateri(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, nullable=False)
    siswa_id = db.Column(
        db.Integer, db.ForeignKey("siswa.id", ondelete="CASCADE"), nullable=False
    )
    mapel_id = db.Column(
        db.Integer, db.ForeignKey("mapel.id", ondelete="CASCADE"), nullable=False
    )
    kelas_id = db.Column(db.ForeignKey("kelas.id", ondelete="SET NULL"), nullable=False)
    th_id = db.Column(
        db.Integer,
        db.ForeignKey("tahun_ajaran.id", ondelete="SET NULL"),
        nullable=False,
    )
    sm_id = db.Column(
        db.Integer, db.ForeignKey("semester.id", ondelete="SET NULL"), nullable=False
    )


class NilaiTengah(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, nullable=False)
    siswa_id = db.Column(
        db.Integer, db.ForeignKey("siswa.id", ondelete="CASCADE"), nullable=False
    )
    mapel_id = db.Column(
        db.Integer, db.ForeignKey("mapel.id", ondelete="CASCADE"), nullable=False
    )
    th_id = db.Column(
        db.Integer,
        db.ForeignKey("tahun_ajaran.id", ondelete="SET NULL"),
        nullable=False,
    )
    sm_id = db.Column(
        db.Integer, db.ForeignKey("semester.id", ondelete="SET NULL"), nullable=False
    )


class NilaiSumatifTengah(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, nullable=False)
    nat_value = db.Column(db.Integer, nullable=False)
    siswa_id = db.Column(
        db.Integer, db.ForeignKey("siswa.id", ondelete="CASCADE"), nullable=False
    )
    mapel_id = db.Column(
        db.Integer, db.ForeignKey("mapel.id", ondelete="CASCADE"), nullable=False
    )
    th_id = db.Column(
        db.Integer,
        db.ForeignKey("tahun_ajaran.id", ondelete="SET NULL"),
        nullable=False,
    )
    sm_id = db.Column(
        db.Integer, db.ForeignKey("semester.id", ondelete="SET NULL"), nullable=False
    )


class NilaiAkhir(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, nullable=False)
    siswa_id = db.Column(
        db.Integer, db.ForeignKey("siswa.id", ondelete="CASCADE"), nullable=False
    )
    mapel_id = db.Column(
        db.Integer, db.ForeignKey("mapel.id", ondelete="CASCADE"), nullable=False
    )
    th_id = db.Column(
        db.Integer,
        db.ForeignKey("tahun_ajaran.id", ondelete="SET NULL"),
        nullable=False,
    )
    sm_id = db.Column(
        db.Integer, db.ForeignKey("semester.id", ondelete="SET NULL"), nullable=False
    )


class NilaiSumatifAkhir(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, nullable=False)
    naa_value = db.Column(db.Integer, nullable=False)
    siswa_id = db.Column(
        db.Integer, db.ForeignKey("siswa.id", ondelete="CASCADE"), nullable=False
    )
    mapel_id = db.Column(
        db.Integer, db.ForeignKey("mapel.id", ondelete="CASCADE"), nullable=False
    )
    th_id = db.Column(
        db.Integer,
        db.ForeignKey("tahun_ajaran.id", ondelete="SET NULL"),
        nullable=False,
    )
    sm_id = db.Column(
        db.Integer, db.ForeignKey("semester.id", ondelete="SET NULL"), nullable=False
    )


# class TujuanPembelajaran(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     desc = db.Column(db.String(500), nullable=True)
#     kd_id = db.Column(db.Integer, db.ForeignKey('kompetensi_dasar.id', ondelete='CASCADE'), nullable=True)
