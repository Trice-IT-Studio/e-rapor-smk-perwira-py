from flask import Blueprint, redirect, request, render_template, url_for, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash

from . import models
from . import db

views = Blueprint("views", __name__)


# BERANDA MAPEL HANDLERS #
@views.route("/dashboard", methods=["GET"])
@login_required
def beranda():
    # general data
    current_th = models.TahunAjaran.query.filter(
        models.TahunAjaran.selected == True
    ).first()
    current_sm = models.Semester.query.filter(models.Semester.selected == True).first()
    all_mapel = models.Mapel.query.all()

    # tambah mapel modal data
    all_kelompok = models.KelompokMapel.query.all()
    all_kelas = models.Kelas.query.all()

    return render_template(
        "views/beranda.html",
        current_th=current_th,
        current_sm=current_sm,
        all_mapel=all_mapel,
        all_kelompok=all_kelompok,
        all_kelas=all_kelas,
    )


@login_required
@views.route("/data_mapel_perkelompok/<int:kelmapel_id>", methods=["GET"])
def data_mapel_perkelompok(kelmapel_id):
    # general data
    current_th = models.TahunAjaran.query.filter(
        models.TahunAjaran.selected == True
    ).first()
    current_sm = models.Semester.query.filter(models.Semester.selected == True).first()
    all_kelas = models.Kelas.query.all()
    mapel_perkelompok = models.Mapel.query.filter(
        models.Mapel.kelompok_id == kelmapel_id
    )
    kelmapel = models.KelompokMapel.query.get(kelmapel_id)

    return render_template(
        "views/mapel_perkelompok.html",
        current_th=current_th,
        current_sm=current_sm,
        mapel_perkelompok=mapel_perkelompok,
        all_kelas=all_kelas,
        kelmapel=kelmapel,
    )


@views.route("/handle_mapel", methods=["POST"])
@login_required
def handle_mapel():
    if request.method == "POST":
        mapel_input = request.form.get("mapel-input")
        kelas_select = request.form.get("kelas-select")
        kelompok_select = request.form.get("kelompok-select")
        mapel_id = request.form.get("mapel-id")

        kelas = models.Kelas.query.get(int(kelas_select))
        kelompok = models.KelompokMapel.query.get(int(kelompok_select))

        # redirect to data_mapel
        to = request.form.get("to")

        if kelas and kelompok:
            if not mapel_id:
                new_mapel = models.Mapel(
                    name=mapel_input,
                )
                db.session.add(new_mapel)
                db.session.commit()
                kelas.mapel_kelas.append(new_mapel)
                kelompok.anggota_kelompok.append(new_mapel)
                db.session.commit()
                flash("Berhasil menambahkan mapel", category="success")
            else:
                to_edit_mapel = models.Mapel.query.get(int(mapel_id))
                to_edit_mapel.name = mapel_input
                kelas.mapel_kelas.append(to_edit_mapel)
                kelompok.anggota_kelompok.append(to_edit_mapel)
                db.session.commit()
                flash(f"Berhasil mengedit {to_edit_mapel.name}", category="success")

            if to == "perkelompok":
                return redirect(
                    url_for("views.data_mapel_perkelompok", kelmapel_id=kelompok_select)
                )
            return redirect(url_for("views.beranda"))

        flash(
            "Gagal menambahkan mapel, pastikan seluruh form terisi.", category="warning"
        )
        if to == "perkelompok":
            return redirect(
                url_for("views.data_mapel_perkelompok", kelmapel_id=kelompok_select)
            )
    return redirect(url_for("views.beranda"))


@views.route("/handle_delete_mapel/<int:mapel_id>", methods=["GET"])
@login_required
def handle_delete_mapel(mapel_id):
    todelete_mapel = models.Mapel.query.get(int(mapel_id))
    if todelete_mapel:
        db.session.delete(todelete_mapel)
        db.session.commit()

        flash(f"Berhasil menghapus mapel: {todelete_mapel.name}", category="success")
        return redirect(url_for("views.beranda"))

    flash("Gagal, mapel tidak ditemukan.", category="error")
    return redirect(url_for("views.beranda"))


@views.route(
    "/handle_delete_mapel_perkelompok/<int:mapel_id>/<int:kelmapel_id>", methods=["GET"]
)
@login_required
def handle_delete_mapel_perkelompok(
    mapel_id, kelmapel_id
):  # MAPEL PERKELOMPOK MAPEL DELETE HANDLER
    todelete_mapel = models.Mapel.query.get(int(mapel_id))

    if todelete_mapel:
        db.session.delete(todelete_mapel)
        db.session.commit()

        flash(f"Berhasil menghapus mapel: {todelete_mapel.name}", category="success")
        return redirect(
            url_for("views.data_mapel_perkelompok", kelmapel_id=kelmapel_id)
        )

    flash("Gagal, mapel tidak ditemukan.", category="error")
    return redirect(url_for("views.data_mapel_perkelompok", kelmapel_id=kelmapel_id))


# BERANDA MAPEL HANDLERS END #


# CAPAIAN KOMPETENSI #
@views.route("/ck/<int:mapel_id>", methods=["GET"])
@login_required
def capaian(mapel_id):
    current_th = models.TahunAjaran.query.filter(
        models.TahunAjaran.selected == True
    ).first()
    current_sm = models.Semester.query.filter(models.Semester.selected == True).first()
    mapel = models.Mapel.query.get(mapel_id)
    mapel_ck = models.CapaianKompetensi.query.filter(
        models.CapaianKompetensi.mapel_id == mapel.id,
        models.CapaianKompetensi.th_id == current_th.id,
        models.CapaianKompetensi.sm_id == current_sm.id,
    ).all()

    return render_template(
        "views/capaian_kompetensi.html",
        mapel=mapel,
        mapel_ck=mapel_ck,
        current_th=current_th,
        current_sm=current_sm,
    )


@login_required
@views.route("/handle_ck/<int:mapel_id>", methods=["POST"])
def handle_ck(mapel_id):
    current_th = models.TahunAjaran.query.filter(
        models.TahunAjaran.selected == True
    ).first()
    current_sm = models.Semester.query.filter(models.Semester.selected == True).first()
    mapel = models.Mapel.query.get(int(mapel_id))

    if request.method == "POST":
        ck_input = request.form.get("ck-input")
        ck_id = request.form.get("ck-id")
        mapel_id = mapel_id if mapel_id else request.form.get("mapel-id")

        if ck_input:
            if not ck_id:
                new_ck = models.CapaianKompetensi(
                    desc=ck_input, th_id=current_th.id, sm_id=current_sm.id
                )
                db.session.add(new_ck)
                db.session.commit()
                mapel.capaian_kompetensi.append(new_ck)
                db.session.commit()
                flash(
                    f"Berhasil menambahkan Capaian Kompetensi ke mapel {mapel.name}",
                    category="success",
                )
            else:
                to_edit_ck = models.CapaianKompetensi.query.get(int(ck_id))
                to_edit_ck.desc = ck_input
                db.session.commit()
                flash(f"Berhasil mengedit Capaian Kompetensi", category="success")
            return redirect(url_for("views.capaian", mapel_id=mapel_id))
        flash(f"Gagal, pastikan semua form terisi.", category="warning")
        return redirect(url_for("views.capaian", mapel_id=mapel_id))

    return redirect(url_for("views.capaian", mapel_id=mapel_id))


@login_required
@views.route("/handle_delete_ck/<int:mapel_id>/<int:ck_id>", methods=["GET"])
def handle_delete_ck(mapel_id, ck_id):
    to_delete_ck = models.CapaianKompetensi.query.get(int(ck_id))

    if to_delete_ck:
        db.session.delete(to_delete_ck)
        db.session.commit()
        flash("Berhasil menghapus Capaian Kompetensi", category="success")
        return redirect(url_for("views.capaian", mapel_id=mapel_id))
    flash("Capaian kompetensi tidak ditemukan", category="error")
    return redirect(url_for("views.capaian", mapel_id=mapel_id))


# CAPAIAN KOMPETENSI END #


# KOMPETENSI DASAR #
@login_required
@views.route("/kd/<int:mapel_id>/<int:ck_id>", methods=["GET"])
def kompetensi_dasar(mapel_id, ck_id):
    current_th = models.TahunAjaran.query.filter(
        models.TahunAjaran.selected == True
    ).first()
    current_sm = models.Semester.query.filter(models.Semester.selected == True).first()
    mapel = models.Mapel.query.get(mapel_id)
    ck = models.CapaianKompetensi.query.get(ck_id)
    ck_kd = models.KompetensiDasar.query.filter(
        models.KompetensiDasar.mapel_id == mapel.id,
        models.KompetensiDasar.th_id == current_th.id,
        models.KompetensiDasar.sm_id == current_sm.id,
        models.KompetensiDasar.ck_id == ck_id,
    ).all()

    return render_template(
        "views/kompetensi_dasar.html",
        current_th=current_th,
        current_sm=current_sm,
        mapel=mapel,
        ck=ck,
        ck_kd=ck_kd,
    )


@login_required
@views.route("/handle_kd/<int:mapel_id>/<int:ck_id>", methods=["POST"])
def handle_kd(mapel_id, ck_id):
    current_th = models.TahunAjaran.query.filter(
        models.TahunAjaran.selected == True
    ).first()
    current_sm = models.Semester.query.filter(models.Semester.selected == True).first()
    ck = models.CapaianKompetensi.query.get(ck_id)

    if request.method == "POST":
        kd_input = request.form.get("kd-input")
        kd_id = request.form.get("kd-id")

        if not kd_id:
            new_kd = models.KompetensiDasar(
                desc=kd_input,
                mapel_id=mapel_id,
                th_id=current_th.id,
                sm_id=current_sm.id,
            )
            db.session.add(new_kd)
            db.session.commit()
            ck.kompetensi_dasar.append(new_kd)
            db.session.commit()
            flash(
                "Berhasil menambahkan Kompetensi Dasar ke Capaian Kompetensi",
                category="success",
            )
            return redirect(
                url_for("views.kompetensi_dasar", mapel_id=mapel_id, ck_id=ck_id)
            )
        else:
            to_edit_kd = models.KompetensiDasar.query.get(kd_id)
            to_edit_kd.desc = kd_input
            db.session.commit()
            flash("Berhasil mengedit Kompetensi Dasar.", category="success")
            return redirect(
                url_for("views.kompetensi_dasar", mapel_id=mapel_id, ck_id=ck_id)
            )
        flash("Gagal, pastikan semua form terisi", category="error")
        return redirect(
            url_for("views.kompetensi_dasar", mapel_id=mapel_id, ck_id=ck_id)
        )


@login_required
@views.route(
    "/handle_delete_kd/<int:mapel_id>/<int:ck_id>/<int:kd_id>", methods=["GET"]
)
def handle_delete_kd(mapel_id, ck_id, kd_id):
    to_delete_kd = models.KompetensiDasar.query.get(int(kd_id))

    if to_delete_kd:
        db.session.delete(to_delete_kd)
        db.session.commit()
        flash("Berhasil menghapus Kompetensi dasar.", category="success")
        return redirect(
            url_for("views.kompetensi_dasar", mapel_id=mapel_id, ck_id=ck_id)
        )
    flash("Gagal, kompetensi dasar tidak ditemukan.", category="error")
    return redirect(url_for("views.kompetensi_dasar", mapel_id=mapel_id, ck_id=ck_id))


# BAGIAN DATA #
# DATA SISWA HANDLERS #
@login_required
@views.route("/data_siswa", methods=["GET"])
def data_siswa():
    # general data
    current_th = models.TahunAjaran.query.filter(
        models.TahunAjaran.selected == True
    ).first()
    current_sm = models.Semester.query.filter(models.Semester.selected == True).first()
    all_siswa = models.Siswa.query.all()

    # Siswa Data
    all_kelas = models.Kelas.query.all()
    all_tingkat = models.Tingkat.query.all()

    return render_template(
        "views/data_siswa.html",
        current_th=current_th,
        current_sm=current_sm,
        all_siswa=all_siswa,
        all_kelas=all_kelas,
        all_tingkat=all_tingkat,
    )


@login_required
@views.route("/data_siswa/<int:kelas_id>", methods=["GET"])
def data_siswa_perkelas(kelas_id):
    # general data
    current_th = models.TahunAjaran.query.filter(
        models.TahunAjaran.selected == True
    ).first()
    current_sm = models.Semester.query.filter(models.Semester.selected == True).first()

    # specific data
    all_siswa_kelas = models.Siswa.query.filter(models.Siswa.kelas_id == kelas_id)
    kelas = models.Kelas.query.get(kelas_id)

    return render_template(
        "views/data_siswa_perkelas.html",
        current_th=current_th,
        current_sm=current_sm,
        kelas=kelas,
        all_siswa_kelas=all_siswa_kelas,
    )


@login_required
@views.route("/handle_siswa", methods=["POST"])
def handle_siswa():
    if request.method == "POST":
        fullname_input = request.form.get("fullname-input")
        nis_input = request.form.get("nis-input")
        nisn_input = request.form.get("nisn-input")
        tempatlahir_input = request.form.get("tempatlahir-input")
        ttl_input = request.form.get("ttl-input")
        alamat_input = request.form.get("alamat-input")
        gender_select = request.form.get("gender-select")
        agama_select = request.form.get("agama-select")
        nayah_input = request.form.get("nayah-input")
        nibu_input = request.form.get("nibu-input")
        payah_input = request.form.get("payah-input")
        pibu_input = request.form.get("pibu-input")
        # check for values in var below
        tingkat_select = request.form.get("tingkat-select")
        kelas_select = request.form.get("kelas-select")
        siswa_id = request.form.get("siswa-id")
        # redirect var
        to = request.form.get("to")
        kelas_id = request.form.get("kelas-id")

        if not siswa_id:
            chk_siswa = models.Siswa.query.filter(
                models.Siswa.nisn == nisn_input
            ).first()
            if chk_siswa:
                flash("Siswa dengan NISN tersebut sudah ada", category="error")
                return redirect(url_for("views.data_siswa"))

            if tingkat_select and kelas_select:
                new_siswa = models.Siswa(
                    full_name=fullname_input,
                    nis=nis_input,
                    nisn=nisn_input,
                    tempat_lahir=tempatlahir_input,
                    tgl_lahir=ttl_input,
                    alamat=alamat_input,
                    jenis_kelamin=gender_select,
                    agama=agama_select,
                    nama_ayah=nayah_input,
                    nama_ibu=nibu_input,
                    pekerjaan_ayah=payah_input,
                    pekerjaan_ibu=pibu_input,
                )
                db.session.add(new_siswa)
                db.session.commit()

                tingkat = models.Tingkat.query.get(int(tingkat_select))
                kelas = models.Kelas.query.get(int(kelas_select))
                tingkat.murid_tingkat.append(new_siswa)
                kelas.anggota_kelas.append(new_siswa)
                db.session.commit()
                flash(
                    f"Berhasil menambah data siswa {new_siswa.full_name}",
                    category="success",
                )
                if to == "perkelas":
                    return redirect(
                        url_for("views.data_siswa_perkelas", kelas_id=kelas_id)
                    )
                return redirect(url_for("views.data_siswa"))
        else:
            to_edit_siswa = models.Siswa.query.get(int(siswa_id))
            to_edit_siswa.full_name = fullname_input
            to_edit_siswa.nis = nis_input
            to_edit_siswa.nisn = nisn_input
            to_edit_siswa.tempat_lahir = tempatlahir_input
            to_edit_siswa.tgl_lahir = ttl_input
            to_edit_siswa.alamat = alamat_input
            to_edit_siswa.jenis_kelamin = gender_select
            to_edit_siswa.agama = agama_select
            to_edit_siswa.nama_ayah = nayah_input
            to_edit_siswa.nama_ibu = nibu_input
            to_edit_siswa.pekerjaan_ayah = payah_input
            to_edit_siswa.pekerjaan_ibu = pibu_input
            to_edit_siswa.tingkat_kelas_id = int(tingkat_select)
            to_edit_siswa.kelas_id = int(kelas_select)
            db.session.commit()
            flash(
                f"Berhasil mengedit data siswa {to_edit_siswa.full_name}",
                category="success",
            )
            if to == "perkelas":
                return redirect(url_for("views.data_siswa_perkelas", kelas_id=kelas_id))
            return redirect(url_for("views.data_siswa"))
    flash(f"Gagal, pastikan seluruh form terisi", category="error")
    if to == "perkelas":
        return redirect(url_for("views.data_siswa_perkelas", kelas_id=kelas_id))
    return redirect(url_for("views.data_siswa"))


@login_required
@views.route(
    "/handle_delete_siswa/<int:siswa_id>/<int:kelas_id>/<string:dest>", methods=["GET"]
)
def handle_delete_siswa(siswa_id, kelas_id, dest):
    to_delete_siswa = models.Siswa.query.get(siswa_id)

    if to_delete_siswa:
        db.session.delete(to_delete_siswa)
        db.session.commit()
        flash(
            f"Berhasil menghapus siswa {to_delete_siswa.full_name}", category="success"
        )
        if dest == "perkelas":
            return redirect(url_for("views.data_siswa_perkelas", kelas_id=kelas_id))
        return redirect(url_for("views.data_siswa"))
    flash("Gagal, siswa tidak ditemukan", category="error")
    if dest == "perkelas":
        return redirect(url_for("views.data_siswa_perkelas", kelas_id=kelas_id))
    return redirect(url_for("views.data_siswa"))


# DATA KELAS HANDLERS #
@login_required
@views.route("/data_kelas", methods=["GET"])
def data_kelas():
    # general data
    current_th = models.TahunAjaran.query.filter(
        models.TahunAjaran.selected == True
    ).first()
    current_sm = models.Semester.query.filter(models.Semester.selected == True).first()
    all_kelas = models.Kelas.query.all()

    all_tingkat = models.Tingkat.query.all()

    return render_template(
        "views/data_kelas.html",
        current_th=current_th,
        current_sm=current_sm,
        all_kelas=all_kelas,
        all_tingkat=all_tingkat,
    )


@login_required
@views.route("/handle_kelas", methods=["POST"])
def handle_kelas():
    if request.method == "POST":
        kelasname_input = request.form.get("kelasname-input")
        walas_input = request.form.get("walas-input")
        tingkat_select = request.form.get("tingkat-select")
        kelas_id = request.form.get("kelas-id")

        if not kelas_id:
            new_kelas = models.Kelas(name=kelasname_input, wali_kelas=walas_input)
            db.session.add(new_kelas)
            db.session.commit()
            tingkat = models.Tingkat.query.get(int(tingkat_select))
            tingkat.anggota_tingkat.append(new_kelas)
            db.session.commit()
            flash(f"Berhasil menambah kelas {new_kelas.name}", category="success")
            return redirect(url_for("views.data_kelas"))
        else:
            to_edit_kelas = models.Kelas.query.get(kelas_id)
            if to_edit_kelas:
                to_edit_kelas.name = kelasname_input
                to_edit_kelas.wali_kelas = walas_input
                to_edit_kelas.tingkat_id = int(tingkat_select)
                db.session.commit()
                flash(
                    f"Berhasil mengedit kelas {to_edit_kelas.name}", category="success"
                )
            return redirect(url_for("views.data_kelas"))
            flash("Gagal, pastikan semua form terisi", category="error")
    return redirect(url_for("views.data_kelas"))


@login_required
@views.route("/handle_delete_kelas/<int:kelas_id>", methods=["GET"])
def handle_delete_kelas(kelas_id):
    to_delete_kelas = models.Kelas.query.get(kelas_id)
    if to_delete_kelas:
        db.session.delete(to_delete_kelas)
        db.session.commit()
        flash(
            f"Berhasil menghapus kelas {to_delete_kelas.tingkat.value}-{to_delete_kelas.name}",
            category="success",
        )
        return redirect(url_for("views.data_kelas"))
    flash("Gagal, data kelas tidak ditemukan", category="error")
    return redirect(url_for("views.data_kelas"))


# DATA KELOMPOK MAPEL ###
@login_required
@views.route("/data_kelompok_mapel", methods=["GET"])
def data_kelompok_mapel():
    # general data
    current_th = models.TahunAjaran.query.filter(
        models.TahunAjaran.selected == True
    ).first()
    current_sm = models.Semester.query.filter(models.Semester.selected == True).first()
    all_kelompok = models.KelompokMapel.query.all()

    return render_template(
        "views/data_kelompok_mapel.html",
        current_sm=current_sm,
        current_th=current_th,
        all_kelompok=all_kelompok,
    )


@login_required
@views.route("/handle_kelompok_mapel", methods=["POST"])
def handle_kelompok_mapel():
    if request.method == "POST":
        kelname_input = request.form.get("kelname-input")
        category_input = request.form.get("category-input")
        kelmapel_id = request.form.get("kelmapel-id")

        if not kelmapel_id:
            new_kelmapel = models.KelompokMapel(
                name=kelname_input, category=category_input
            )
            db.session.add(new_kelmapel)
            db.session.commit()
            flash(
                f"Berhasil menambah kelompok mapel: {new_kelmapel.name}",
                category="success",
            )
        else:
            to_edit_kelmapel = models.KelompokMapel.query.get(int(kelmapel_id))
            if to_edit_kelmapel:
                to_edit_kelmapel.name = kelname_input
                to_edit_kelmapel.category = category_input
                db.session.commit()
                flash(
                    f"Berhasil mengedit kelompok mapel: {to_edit_kelmapel.name}",
                    category="success",
                )
            else:
                flash(f"Gagal, kelompok mapel tidak ditemukan", category="error")
        return redirect(url_for("views.data_kelompok_mapel"))

    return redirect(url_for("views.data_kelompok_mapel"))


@login_required
@views.route("/handle_delete_kelompok_mapel/<int:kelmapel_id>", methods=["GET"])
def handle_delete_kelompok_mapel(kelmapel_id):
    to_delete_kelmapel = models.KelompokMapel.query.get(kelmapel_id)

    if to_delete_kelmapel:
        db.session.delete(to_delete_kelmapel)
        db.session.commit()
        flash(
            f"Berhasil menghapus kelompok mapel: {to_delete_kelmapel.name}",
            category="success",
        )
        return redirect(url_for("views.data_kelompok_mapel"))

    flash(f"Gagal, kelompok mapel tidak ditemukan", category="error")
    return redirect(url_for("views.data_kelompok_mapel"))


# DATA NILAI ###
# BOBOT PENILAIAN ###
@login_required
@views.route("/bobot_penilaian", methods=["GET"])
def bobot_penilaian():
    # general data
    current_th = models.TahunAjaran.query.filter(
        models.TahunAjaran.selected == True
    ).first()
    current_sm = models.Semester.query.filter(models.Semester.selected == True).first()

    all_mapel = models.Mapel.query.all()

    return render_template(
        "views/bobot_penilaian.html",
        current_th=current_th,
        current_sm=current_sm,
        all_mapel=all_mapel,
    )


@login_required
@views.route("/handle_bobot_penilaian", methods=["POST"])
def handle_bobot_penilaian():
    # general data
    current_th = models.TahunAjaran.query.filter(
        models.TahunAjaran.selected == True
    ).first()
    current_sm = models.Semester.query.filter(models.Semester.selected == True).first()

    if request.method == "POST":
        mapel_id = request.form.get("mapel-id")
        bobotmateri_input_p = request.form.get("bobotmateri-input-p")
        bobotmateri_input_k = request.form.get("bobotmateri-input-k")
        bobottengah_input = request.form.get("bobottengah-input")
        bobotakhir_input = request.form.get("bobotakhir-input")

        bobot = models.BobotPenilaian.query.filter(
            models.BobotPenilaian.mapel_id == int(mapel_id)
        ).first()

        if not bobot:
            new_bobot = models.BobotPenilaian(
                bobot_materi_p=bobotmateri_input_p,
                bobot_materi_k=bobotmateri_input_k,
                bobot_tengah=bobottengah_input,
                bobot_akhir=bobotakhir_input,
                mapel_id=mapel_id,
                th_id=current_th.id,
                sm_id=current_sm.id,
            )
            db.session.add(new_bobot)
            db.session.commit()
            flash(
                f"Berhasil menambahkan bobot penilaian pada mapel: {new_bobot.mapel_terkait.name}",
                category="success",
            )
            return redirect(url_for("views.bobot_penilaian"))
        else:
            to_edit_bobot = models.BobotPenilaian.query.filter(
                models.BobotPenilaian.mapel_id == mapel_id
            ).first()
            to_edit_bobot.bobot_materi_p = bobotmateri_input_p
            to_edit_bobot.bobot_materi_k = bobotmateri_input_k
            to_edit_bobot.bobot_tengah = bobottengah_input
            to_edit_bobot.bobot_akhir = bobotakhir_input
            db.session.commit()
            flash(
                f"Berhasil mengedit bobot penilaian mapel: {to_edit_bobot.mapel_terkait.name}",
                category="success",
            )
            return redirect(url_for("views.bobot_penilaian"))

    flash("Unknown fatal error has occured, please contact developer", category="error")
    return redirect(url_for("views.bobot_penilaian"))


# FORM AWAL PENILAIAN ###
@login_required
@views.route("/nilai_start1", methods=["GET"])
def nilai_start1():
    # general data
    current_th = models.TahunAjaran.query.filter(
        models.TahunAjaran.selected == True
    ).first()
    current_sm = models.Semester.query.filter(models.Semester.selected == True).first()

    # specific data
    all_kelas = models.Kelas.query.all()

    return render_template(
        "views/nilai_start1.html",
        current_th=current_th,
        current_sm=current_sm,
        all_kelas=all_kelas,
    )


@login_required
@views.route("/nilai_start2/<int:kelas_id>", methods=["GET"])
def nilai_start2(kelas_id):
    # general data
    current_th = models.TahunAjaran.query.filter(
        models.TahunAjaran.selected == True
    ).first()
    current_sm = models.Semester.query.filter(models.Semester.selected == True).first()

    # specific data
    kelas = models.Kelas.query.get(kelas_id)
    mapel_perkelas = kelas.mapel_kelas

    if not mapel_perkelas:
        flash(
            f"Belum ada mapel yang di ajarkan di kelas {kelas.name}, silahkan tambah mapel di beranda terlebih dahulu",
            category="warning",
        )
        return redirect(url_for("views.nilai_start1"))

    return render_template(
        "views/nilai_start2.html",
        current_th=current_th,
        current_sm=current_sm,
        kelas=kelas,
        mapel_perkelas=mapel_perkelas,
    )


@login_required
@views.route("/nilai_start3/<int:mapel_id>/<int:kelas_id>/<int:tipe>", methods=["GET"])
def nilai_start3(mapel_id, kelas_id, tipe):
    # general data
    current_th = models.TahunAjaran.query.filter(
        models.TahunAjaran.selected == True
    ).first()
    current_sm = models.Semester.query.filter(models.Semester.selected == True).first()

    all_th = models.TahunAjaran.query.all()
    all_sm = models.Semester.query.all()

    return render_template(
        "views/nilai_start3.html",
        current_th=current_th,
        current_sm=current_sm,
        all_th=all_th,
        all_sm=all_sm,
        kelas_id=kelas_id,
        tipe=tipe,
        mapel_id=mapel_id,
    )


# TODO add sm and th into mapel, ck, kd
@login_required
@views.route("/handle_nilai_start", methods=["POST"])
def handle_nilai_start():
    if request.method == "POST":
        th_select = request.form.get("th-select")
        sm_select = request.form.get("sm-select")
        mapel_id = request.form.get("mapel-id")
        kelas_id = request.form.get("kelas-id")
        tipe = request.form.get("tipe")

        if tipe == "1":
            return redirect(
                url_for(
                    "views.nilai_lingkupmateri",
                    th=th_select,
                    sm=sm_select,
                    mapel_id=mapel_id,
                    kelas_id=kelas_id,
                    tipe=tipe,
                )
            )
        if tipe == "2":
            return redirect(
                url_for(
                    "views.nilai_tengah",
                    th=th_select,
                    sm=sm_select,
                    mapel_id=mapel_id,
                    kelas_id=kelas_id,
                    tipe=tipe,
                )
            )
        if tipe == "3":
            return redirect(
                url_for(
                    "views.nilai_akhir",
                    th=th_select,
                    sm=sm_select,
                    mapel_id=mapel_id,
                    kelas_id=kelas_id,
                    tipe=tipe,
                )
            )

    return redirect(
        url_for("views.nilai_start3", mapel_id=mapel_id, kelas_id=kelas_id, tipe=tipe)
    )


# NILAI LINGKUP MATERI ###
@login_required
@views.route(
    "/nilai_lingkupmateri/<int:th>/<int:sm>/<int:mapel_id>/<int:kelas_id>/<int:tipe>",
    methods=["GET"],
)
def nilai_lingkupmateri(th, sm, mapel_id, kelas_id, tipe):
    # general data
    current_th = models.TahunAjaran.query.filter(
        models.TahunAjaran.selected == True
    ).first()
    current_sm = models.Semester.query.filter(models.Semester.selected == True).first()

    # specific data
    th_obj = models.TahunAjaran.query.get(th)
    sm_obj = models.Semester.query.get(sm)
    kelas = models.Kelas.query.get(kelas_id)
    mapel = models.Mapel.query.get(mapel_id)
    lingkup_kd = models.KompetensiDasar.query.filter(
        models.KompetensiDasar.th_id == th_obj.id,
        models.KompetensiDasar.sm_id == sm_obj.id,
        models.KompetensiDasar.mapel_id == mapel.id,
    ).all()

    # TODO Remove before production
    for siswa in kelas.anggota_kelas:
        for kd in lingkup_kd:
            for nlk in kd.nilai:
                if nlk.tipe_nilai == "p":
                    if nlk.value and nlk.siswa_id == siswa.id:
                        print("input nilai for siswa P: ", nlk.value, siswa.full_name)
                    elif not nlk.value and nlk.siswa_id == siswa.id:
                        print("input nilai for siswa P: ", siswa.full_name)
                if nlk.tipe_nilai == "k":
                    if nlk.value and nlk.siswa_id == siswa.id:
                        print("input nilai for siswa k: ", nlk.value, siswa.full_name)
                    elif not nlk.value and nlk.siswa_id == siswa.id:
                        print("input nilai for siswa k: ", siswa.full_name)
            if not siswa.nilai_lingkup_materi:
                print("input nilai for siswa P: ", siswa.full_name)
                print("input nilai for siswa k: ", siswa.full_name)

    return render_template(
        "views/nilai_lingkupmateri.html",
        current_th=current_th,
        current_sm=current_sm,
        th_obj=th_obj,
        sm_obj=sm_obj,
        kelas=kelas,
        mapel=mapel,
        mapel_id=mapel_id,
        tipe=tipe,
        lingkup_kd=lingkup_kd,
    )


@login_required
@views.route(
    "/handle_lingkupmateri",
    methods=["POST"],
)
def handle_lingkupmateri():
    if request.method == "POST":
        th = request.form.get("th")
        sm = request.form.get("sm")
        mapel_id = request.form.get("mapel-id")
        kelas_id = request.form.get("kelas-id")
        tipe = request.form.get("tipe")

        mapel = models.Mapel.query.get(mapel_id)
        kd_permapel = models.KompetensiDasar.query.filter(
            models.KompetensiDasar.mapel_id == mapel_id
        )
        kelas = models.Kelas.query.get(kelas_id)
        siswa_perkelas = kelas.anggota_kelas
        lingkup_kd = models.KompetensiDasar.query.filter(
            models.KompetensiDasar.th_id == th,
            models.KompetensiDasar.sm_id == sm,
            models.KompetensiDasar.mapel_id == mapel.id,
        ).all()

        # bobot penilaian readyness check
        bobot = models.BobotPenilaian.query.filter(
            models.BobotPenilaian.mapel_id == mapel.id,
            models.BobotPenilaian.th_id == th,
            models.BobotPenilaian.sm_id == sm,
        ).first()

        if bobot:
            if not bobot.bobot_materi_p:
                flash(
                    "Bobot penilaian belum ter-isi lengkap! silahkan isi dahulu sebelum penilaian tengah dan akhir semester",
                    category="error",
                )
                return redirect(
                    url_for(
                        "views.nilai_lingkupmateri",
                        th=th,
                        sm=sm,
                        mapel_id=mapel_id,
                        kelas_id=kelas_id,
                        tipe=tipe,
                    )
                )
            if not bobot.bobot_materi_k:
                flash(
                    "Bobot penilaian belum ter-isi lengkap! silahkan isi dahulu sebelum penilaian tengah dan akhir semester",
                    category="error",
                )
                return redirect(
                    url_for(
                        "views.nilai_lingkupmateri",
                        th=th,
                        sm=sm,
                        mapel_id=mapel_id,
                        kelas_id=kelas_id,
                        tipe=tipe,
                    )
                )
            if not bobot.bobot_tengah:
                flash(
                    "Bobot penilaian belum ter-isi lengkap! silahkan isi dahulu sebelum penilaian tengah dan akhir semester",
                    category="error",
                )
                return redirect(
                    url_for(
                        "views.nilai_lingkupmateri",
                        th=th,
                        sm=sm,
                        mapel_id=mapel_id,
                        kelas_id=kelas_id,
                        tipe=tipe,
                    )
                )
            if not bobot.bobot_akhir:
                flash(
                    "Bobot penilaian belum ter-isi lengkap! silahkan isi dahulu sebelum penilaian tengah dan akhir semester",
                    category="error",
                )
                return redirect(
                    url_for(
                        "views.nilai_lingkupmateri",
                        th=th,
                        sm=sm,
                        mapel_id=mapel_id,
                        kelas_id=kelas_id,
                        tipe=tipe,
                    )
                )
        elif not bobot:
            flash(
                "Bobot penilaian belum ter-isi lengkap! silahkan isi dahulu sebelum penilaian tengah dan akhir semester",
                category="error",
            )
            return redirect(
                url_for(
                    "views.nilai_lingkupmateri",
                    th=th,
                    sm=sm,
                    mapel_id=mapel_id,
                    kelas_id=kelas_id,
                    tipe=tipe,
                )
            )

        for siswa in siswa_perkelas:
            for kd in lingkup_kd:
                nlk_value_p = request.form.get(f"nlk-{kd.id}-siswa-{siswa.id}-p")
                nlk_value_k = request.form.get(f"nlk-{kd.id}-siswa-{siswa.id}-k")

                chk_nlk_p = models.NilaiLingkupMateri.query.filter(
                    models.NilaiLingkupMateri.siswa_id == siswa.id,
                    models.NilaiLingkupMateri.kd_id == kd.id,
                    models.NilaiLingkupMateri.th_id == th,
                    models.NilaiLingkupMateri.sm_id == sm,
                    models.NilaiLingkupMateri.tipe_nilai == "p",
                ).first()
                chk_nlk_k = models.NilaiLingkupMateri.query.filter(
                    models.NilaiLingkupMateri.siswa_id == siswa.id,
                    models.NilaiLingkupMateri.kd_id == kd.id,
                    models.NilaiLingkupMateri.th_id == th,
                    models.NilaiLingkupMateri.sm_id == sm,
                    models.NilaiLingkupMateri.tipe_nilai == "k",
                ).first()

                # nilai lingkup tipe pengetahuan
                if not chk_nlk_p:
                    new_nlk = models.NilaiLingkupMateri(
                        value=nlk_value_p,
                        kd_id=kd.id,
                        siswa_id=siswa.id,
                        mapel_id=mapel.id,
                        kelas_id=kelas.id,
                        th_id=th,
                        sm_id=sm,
                        tipe_nilai="p",
                    )
                    db.session.add(new_nlk)
                    db.session.commit()
                else:
                    if nlk_value_p:
                        to_edit_nlk_p = models.NilaiLingkupMateri.query.filter(
                            models.NilaiLingkupMateri.siswa_id == siswa.id,
                            models.NilaiLingkupMateri.kd_id == kd.id,
                            models.NilaiLingkupMateri.th_id == th,
                            models.NilaiLingkupMateri.sm_id == sm,
                            models.NilaiLingkupMateri.tipe_nilai == "p",
                        ).first()
                        to_edit_nlk_p.value = nlk_value_p
                        db.session.commit()

                # nilai lingkup tipe keterampilan
                if not chk_nlk_k:
                    new_nlk = models.NilaiLingkupMateri(
                        value=nlk_value_k,
                        kd_id=kd.id,
                        siswa_id=siswa.id,
                        mapel_id=mapel.id,
                        kelas_id=kelas.id,
                        th_id=th,
                        sm_id=sm,
                        tipe_nilai="k",
                    )
                    db.session.add(new_nlk)
                    db.session.commit()
                else:
                    if nlk_value_k:
                        to_edit_nlk_k = models.NilaiLingkupMateri.query.filter(
                            models.NilaiLingkupMateri.siswa_id == siswa.id,
                            models.NilaiLingkupMateri.kd_id == kd.id,
                            models.NilaiLingkupMateri.th_id == th,
                            models.NilaiLingkupMateri.sm_id == sm,
                            models.NilaiLingkupMateri.tipe_nilai == "k",
                        ).first()
                        to_edit_nlk_k.value = nlk_value_k
                        db.session.commit()
        flash(f"Berhasil mengedit nilai lingkup materi", category="success")

        # calculate sumatif tengah semester
        # Rata-rata KD = ((KD1 + KD2 + KD3 + ...) / Jumlah KD) x Bobot Sumatif Lingkup Materi
        # Nilai ATS = Nilai Asesment Tengah Semester x Bobot
        # Sumatif Tengah Semester
        # Nilai Sumatif Tengah Semester = Rata-rata KD + Nilai ATS
        for siswa in kelas.anggota_kelas:
            # calc nilai sumatif lingkup materi
            temp_p = 0
            count_p = 0
            temp_k = 0
            count_k = 0
            for nlk in siswa.nilai_lingkup_materi:
                if (
                    nlk.value
                    and nlk.tipe_nilai == "p"
                    and nlk.mapel_id == mapel.id
                    and nlk.th_id == int(th)
                    and nlk.sm_id == int(sm)
                ):
                    temp_p += int(nlk.value)
                    count_p += 1
                elif (
                    nlk.value
                    and nlk.tipe_nilai == "k"
                    and nlk.mapel_id == mapel.id
                    and nlk.th_id == int(th)
                    and nlk.sm_id == int(sm)
                ):
                    temp_k += int(nlk.value)
                    count_k += 1
            try:
                calc_avg_p = round((temp_p / count_p) * (bobot.bobot_materi_p / 100))
            except Exception as e:
                print("Exception notification: handle_lingkup mater zero division", e)
                calc_avg_p = 0
            try:
                calc_avg_k = round((temp_k / count_k) * (bobot.bobot_materi_k / 100))
            except Exception as e:
                print("Exception notification: handle_lingkup mater zero division", e)
                calc_avg_k = 0
            nslk_value = calc_avg_p + calc_avg_k

            chk_nslk = models.NilaiSumatifLingkupMateri.query.filter(
                models.NilaiSumatifLingkupMateri.siswa_id == siswa.id,
                models.NilaiSumatifLingkupMateri.th_id == th,
                models.NilaiSumatifLingkupMateri.sm_id == sm,
                models.NilaiSumatifLingkupMateri.mapel_id == mapel.id,
            ).first()

            if not chk_nslk:
                new_nslk = models.NilaiSumatifLingkupMateri(
                    value=nslk_value,
                    siswa_id=siswa.id,
                    mapel_id=mapel.id,
                    kelas_id=kelas.id,
                    th_id=th,
                    sm_id=sm,
                )
                db.session.add(new_nslk)
                db.session.commit()
            else:
                to_update_nslk = models.NilaiSumatifLingkupMateri.query.filter(
                    models.NilaiSumatifLingkupMateri.siswa_id == siswa.id,
                    models.NilaiSumatifLingkupMateri.th_id == th,
                    models.NilaiSumatifLingkupMateri.sm_id == sm,
                    models.NilaiSumatifLingkupMateri.mapel_id == mapel.id,
                    models.NilaiSumatifLingkupMateri.kelas_id == kelas.id,
                ).first()
                if nslk_value:
                    to_update_nslk.value = nslk_value
                    db.session.commit()

    return redirect(
        url_for(
            "views.nilai_lingkupmateri",
            th=th,
            sm=sm,
            mapel_id=mapel_id,
            kelas_id=kelas_id,
            tipe=tipe,
        )
    )


# NILAI TENGAH SEMESTER ###
@login_required
@views.route(
    "/nilai_tengah/<int:th>/<int:sm>/<int:mapel_id>/<int:kelas_id>/<int:tipe>",
    methods=["GET"],
)
def nilai_tengah(th, sm, mapel_id, kelas_id, tipe):
    # general data
    current_th = models.TahunAjaran.query.filter(
        models.TahunAjaran.selected == True
    ).first()
    current_sm = models.Semester.query.filter(models.Semester.selected == True).first()

    # specific data
    th_obj = models.TahunAjaran.query.get(th)
    sm_obj = models.Semester.query.get(sm)
    kelas = models.Kelas.query.get(kelas_id)
    mapel = models.Mapel.query.get(mapel_id)
    lingkup_ck = models.CapaianKompetensi.query.filter(
        models.CapaianKompetensi.th_id == th_obj.id,
        models.CapaianKompetensi.sm_id == sm_obj.id,
        models.CapaianKompetensi.mapel_id == mapel.id,
    ).all()
    lingkup_kd = models.KompetensiDasar.query.filter(
        models.KompetensiDasar.th_id == th_obj.id,
        models.KompetensiDasar.sm_id == sm_obj.id,
        models.KompetensiDasar.mapel_id == mapel.id,
    ).all()
    the_nt = models.NilaiTengah.query.filter(
        models.NilaiTengah.mapel_id == mapel.id,
        models.NilaiTengah.th_id == th,
        models.NilaiTengah.sm_id == sm,
    ).all()

    # TODO delete before production
    siswa_perkelas = kelas.anggota_kelas
    for siswa in siswa_perkelas:
        if siswa.nilai_tengah:
            for nt in siswa.nilai_tengah:
                if nt.th_id == th_obj.id and nt.sm_id == sm_obj.id:
                    print("nilai tengah semester: ", siswa.full_name, nt.value)
        if not siswa.nilai_tengah:
            print("No nilai tengah for: ", siswa.full_name)

    return render_template(
        "views/nilai_tengah.html",
        current_th=current_th,
        current_sm=current_sm,
        mapel=mapel,
        kelas=kelas,
        th_obj=th_obj,
        sm_obj=sm_obj,
        th=th,
        sm=sm,
        lingkup_ck=lingkup_ck,
        lingkup_kd=lingkup_kd,
        the_nt=the_nt,
        tipe=tipe,
    )


@login_required
@views.route("/handle_nilai_tengah", methods=["POST"])
def handle_nilai_tengah():
    if request.method == "POST":
        nt_mapel = request.form.get("nt-mapel")
        th = request.form.get("th")
        sm = request.form.get("sm")
        kelas_id = request.form.get("kelas-id")
        mapel_id = request.form.get("mapel-id")
        tipe = request.form.get("tipe")

        kelas = models.Kelas.query.get(kelas_id)
        siswa_perkelas = kelas.anggota_kelas

        # pull bobot penilaian for calculation
        bobot = models.BobotPenilaian.query.filter(
            models.BobotPenilaian.mapel_id == mapel_id,
            models.BobotPenilaian.th_id == th,
            models.BobotPenilaian.sm_id == sm,
        ).first()

        # bobot penilaian readyness check
        if bobot:
            if not bobot.bobot_materi_p:
                flash(
                    "Bobot penilaian belum ter-isi lengkap! silahkan isi dahulu sebelum penilaian tengah dan akhir semester",
                    category="error",
                )
                return redirect(
                    url_for(
                        "views.nilai_tengah",
                        th=int(th),
                        sm=int(sm),
                        kelas_id=int(kelas_id),
                        mapel_id=int(mapel_id),
                        tipe=tipe,
                    )
                )
            if not bobot.bobot_materi_k:
                flash(
                    "Bobot penilaian belum ter-isi lengkap! silahkan isi dahulu sebelum penilaian tengah dan akhir semester",
                    category="error",
                )
                return redirect(
                    url_for(
                        "views.nilai_tengah",
                        th=int(th),
                        sm=int(sm),
                        kelas_id=int(kelas_id),
                        mapel_id=int(mapel_id),
                        tipe=tipe,
                    )
                )
            if not bobot.bobot_tengah:
                flash(
                    "Bobot penilaian belum ter-isi lengkap! silahkan isi dahulu sebelum penilaian tengah dan akhir semester",
                    category="error",
                )
                return redirect(
                    url_for(
                        "views.nilai_tengah",
                        th=int(th),
                        sm=int(sm),
                        kelas_id=int(kelas_id),
                        mapel_id=int(mapel_id),
                        tipe=tipe,
                    )
                )
            if not bobot.bobot_akhir:
                flash(
                    "Bobot penilaian belum ter-isi lengkap! silahkan isi dahulu sebelum penilaian tengah dan akhir semester",
                    category="error",
                )
                return redirect(
                    url_for(
                        "views.nilai_tengah",
                        th=int(th),
                        sm=int(sm),
                        kelas_id=int(kelas_id),
                        mapel_id=int(mapel_id),
                        tipe=tipe,
                    )
                )
        elif not bobot:
            flash(
                "Bobot penilaian belum ter-isi lengkap! silahkan isi dahulu sebelum penilaian tengah dan akhir semester",
                category="error",
            )
            return redirect(
                url_for(
                    "views.nilai_tengah",
                    th=int(th),
                    sm=int(sm),
                    kelas_id=int(kelas_id),
                    mapel_id=int(mapel_id),
                    tipe=tipe,
                )
            )

        # add nilai nt to db
        for siswa in siswa_perkelas:
            nat_value = request.form.get(f"nat-{siswa.id}")
            chk_nt = models.NilaiSumatifTengah.query.filter(
                models.NilaiSumatifTengah.siswa_id == siswa.id,
                models.NilaiSumatifTengah.th_id == th,
                models.NilaiSumatifTengah.sm_id == sm,
                models.NilaiSumatifTengah.mapel_id == mapel_id,
            ).first()

            # get nilai rata-rata formatif (KD avg)
            nslk_value = 0
            if siswa.nilai_sumatif_lingkup_materi:
                for nslk in siswa.nilai_sumatif_lingkup_materi:
                    if (
                        nslk.value
                        and nslk.mapel_id == int(mapel_id)
                        and nslk.th_id == int(th)
                        and nslk.sm_id == int(sm)
                    ):
                        nslk_value = nslk.value

            if nat_value:
                nst_value = nslk_value + (int(nat_value) * (bobot.bobot_tengah / 100))
                if not chk_nt:
                    new_nat = models.NilaiSumatifTengah(
                        value=nst_value,
                        nat_value=nat_value,
                        siswa_id=siswa.id,
                        mapel_id=mapel_id,
                        th_id=th,
                        sm_id=sm,
                    )
                    db.session.add(new_nat)
                    db.session.commit()
                else:
                    to_update_nat = models.NilaiSumatifTengah.query.filter(
                        models.NilaiSumatifTengah.siswa_id == siswa.id,
                        models.NilaiSumatifTengah.th_id == th,
                        models.NilaiSumatifTengah.sm_id == sm,
                        models.NilaiSumatifTengah.mapel_id == mapel_id,
                    ).first()
                    to_update_nat.value = nst_value
                    to_update_nat.nat_value = nat_value
                    db.session.commit()
        flash(f"Berhasil mengedit nilai tengah semester", category="success")

        # add nilai nst and calculate nilai akhir tengah semester value
        # calculate nilai sumatif tengah semester
        for siswa in siswa_perkelas:
            nat_value = 0
            if siswa.nilai_sumatif_tengah:
                for nat in siswa.nilai_sumatif_tengah:
                    if (
                        nat.nat_value
                        and nat.mapel_id == int(mapel_id)
                        and nat.th_id == int(th)
                        and nat.sm_id == int(sm)
                    ):
                        nat_value = nat.nat_value

            nslk_value = 0
            if siswa.nilai_sumatif_lingkup_materi:
                for nslk in siswa.nilai_sumatif_lingkup_materi:
                    if (
                        nslk.value
                        and nslk.mapel_id == int(mapel_id)
                        and nslk.th_id == int(th)
                        and nslk.sm_id == int(sm)
                    ):
                        nslk_value = nslk.value

            # Nilai Sumatif Tengah = Avg Formatif + (Nilai Asesment Tengah * (bobot tengah / 100)) * 2
            # TODO calc bobot tengah and bobot materi if bobot akhir not present
            # note: *2 at the end is to be calculated further based on availability of bobot akhir
            try:
                calc_pure_nst = nat_value * round((bobot.bobot_tengah / 100) * 2)
            except Exception as e:
                print(
                    "Exception notification: Possible division by zero in handle_nilai_tengah: ",
                    e,
                )
                calc_pure_nst = 0
            calc_pure_nslk = nslk.value * 2
            nats_value = calc_pure_nst + calc_pure_nslk

            chk_nats = models.NilaiTengah.query.filter(
                models.NilaiTengah.siswa_id == siswa.id,
                models.NilaiTengah.mapel_id == int(mapel_id),
                models.NilaiTengah.th_id == int(th),
                models.NilaiTengah.sm_id == int(sm),
            ).first()

            if nat_value:
                if not chk_nats:
                    new_nats = models.NilaiTengah(
                        value=round(nats_value),
                        siswa_id=siswa.id,
                        mapel_id=int(mapel_id),
                        th_id=int(th),
                        sm_id=int(sm),
                    )
                    db.session.add(new_nats)
                    db.session.commit()
                else:
                    if nats_value:
                        to_update_nats = models.NilaiTengah.query.filter(
                            models.NilaiTengah.siswa_id == siswa.id,
                            models.NilaiTengah.mapel_id == int(mapel_id),
                            models.NilaiTengah.th_id == int(th),
                            models.NilaiTengah.sm_id == int(sm),
                        ).first()
                        to_update_nats.value = round(nats_value)
                        db.session.commit()

        return redirect(
            url_for(
                "views.nilai_tengah",
                th=int(th),
                sm=int(sm),
                kelas_id=int(kelas_id),
                mapel_id=int(mapel_id),
                tipe=tipe,
            )
        )

    return redirect(url_for("views.nilai_tengah", th=th, sm=sm, mapel_id=mapel_id))


# NILAI AKHIR
@login_required
@views.route(
    "/nilai_akhir/<int:th>/<int:sm>/<int:mapel_id>/<int:kelas_id>/<int:tipe>",
    methods=["GET"],
)
def nilai_akhir(th, sm, mapel_id, kelas_id, tipe):
    # general data
    current_th = models.TahunAjaran.query.filter(
        models.TahunAjaran.selected == True
    ).first()
    current_sm = models.Semester.query.filter(models.Semester.selected == True).first()

    # query related data
    th_obj = models.TahunAjaran.query.get(th)
    sm_obj = models.Semester.query.get(sm)
    mapel = models.Mapel.query.get(mapel_id)
    kelas = models.Kelas.query.get(kelas_id)
    tipe = int(tipe)
    lingkup_ck = models.CapaianKompetensi.query.filter(
        models.CapaianKompetensi.th_id == th_obj.id,
        models.CapaianKompetensi.sm_id == sm_obj.id,
        models.CapaianKompetensi.mapel_id == mapel.id,
    ).all()
    lingkup_kd = models.KompetensiDasar.query.filter(
        models.KompetensiDasar.th_id == th_obj.id,
        models.KompetensiDasar.sm_id == sm_obj.id,
        models.KompetensiDasar.mapel_id == mapel.id,
    ).all()
    the_nt = models.NilaiTengah.query.filter(
        models.NilaiTengah.mapel_id == mapel.id,
        models.NilaiTengah.th_id == th,
        models.NilaiTengah.sm_id == sm,
    ).all()

    # nilai akhir related data
    nsa = 0
    na = 0
    for siswa in kelas.anggota_kelas:
        nsa = models.NilaiSumatifAkhir.query.filter(
            models.NilaiSumatifAkhir.siswa_id == siswa.id,
            models.NilaiSumatifAkhir.mapel_id == mapel.id,
            models.NilaiSumatifAkhir.th_id == th_obj.id,
            models.NilaiSumatifAkhir.sm_id == sm_obj.id,
        ).first()

        na = models.NilaiAkhir.query.filter(
            models.NilaiAkhir.siswa_id == siswa.id,
            models.NilaiAkhir.mapel_id == mapel.id,
            models.NilaiAkhir.th_id == th_obj.id,
            models.NilaiAkhir.sm_id == sm_obj.id,
        ).first()

    return render_template(
        "views/nilai_akhir.html",
        current_th=current_th,
        current_sm=current_sm,
        th_obj=th_obj,
        sm_obj=sm_obj,
        th=th,
        sm=sm,
        mapel=mapel,
        kelas=kelas,
        tipe=tipe,
        nsa=nsa,
        na=na,
        lingkup_ck=lingkup_ck,
        lingkup_kd=lingkup_kd,
        the_nt=the_nt,
    )


@login_required
@views.route("/handle_nilai_akhir", methods=["POST"])
def handle_nilai_akhir():
    if request.method == "POST":
        # form data
        th = request.form.get("th")
        sm = request.form.get("sm")
        kelas_id = request.form.get("kelas-id")
        mapel_id = request.form.get("mapel-id")
        tipe = request.form.get("tipe")

        # query data
        th_obj = models.TahunAjaran.query.get(th)
        sm_obj = models.Semester.query.get(sm)
        kelas = models.Kelas.query.get(kelas_id)
        mapel = models.Mapel.query.get(mapel_id)

        # query bobot penilaian for calculation
        bobot = models.BobotPenilaian.query.filter(
            models.BobotPenilaian.mapel_id == mapel_id,
            models.BobotPenilaian.th_id == th,
            models.BobotPenilaian.sm_id == sm,
        ).first()

        # bobot penilaian readyness check
        if bobot:
            if not bobot.bobot_materi_p:
                flash(
                    "Bobot penilaian belum ter-isi lengkap! silahkan isi dahulu sebelum penilaian tengah dan akhir semester",
                    category="error",
                )
                return redirect(
                    url_for(
                        "views.nilai_tengah",
                        th=int(th),
                        sm=int(sm),
                        kelas_id=int(kelas_id),
                        mapel_id=int(mapel_id),
                        tipe=tipe,
                    )
                )
            if not bobot.bobot_materi_k:
                flash(
                    "Bobot penilaian belum ter-isi lengkap! silahkan isi dahulu sebelum penilaian tengah dan akhir semester",
                    category="error",
                )
                return redirect(
                    url_for(
                        "views.nilai_tengah",
                        th=int(th),
                        sm=int(sm),
                        kelas_id=int(kelas_id),
                        mapel_id=int(mapel_id),
                        tipe=tipe,
                    )
                )
            if not bobot.bobot_tengah:
                flash(
                    "Bobot penilaian belum ter-isi lengkap! silahkan isi dahulu sebelum penilaian tengah dan akhir semester",
                    category="error",
                )
                return redirect(
                    url_for(
                        "views.nilai_tengah",
                        th=int(th),
                        sm=int(sm),
                        kelas_id=int(kelas_id),
                        mapel_id=int(mapel_id),
                        tipe=tipe,
                    )
                )
            if not bobot.bobot_akhir:
                flash(
                    "Bobot penilaian belum ter-isi lengkap! silahkan isi dahulu sebelum penilaian tengah dan akhir semester",
                    category="error",
                )
                return redirect(
                    url_for(
                        "views.nilai_tengah",
                        th=int(th),
                        sm=int(sm),
                        kelas_id=int(kelas_id),
                        mapel_id=int(mapel_id),
                        tipe=tipe,
                    )
                )
        elif not bobot:
            flash(
                "Bobot penilaian belum ter-isi lengkap! silahkan isi dahulu sebelum penilaian tengah dan akhir semester",
                category="error",
            )
            return redirect(
                url_for(
                    "views.nilai_tengah",
                    th=int(th),
                    sm=int(sm),
                    kelas_id=int(kelas_id),
                    mapel_id=int(mapel_id),
                    tipe=tipe,
                )
            )

        # add nsa to db
        for siswa in kelas.anggota_kelas:
            naa_value = request.form.get(f"naa-{siswa.id}")
            nst_value = 0

            # query nilai asesmen tengah siswa
            if siswa.nilai_sumatif_tengah:
                for nst in siswa.nilai_sumatif_tengah:
                    if (
                        nst.value
                        and nst.mapel_id == mapel.id
                        and nst.th_id == th_obj.id
                        and nst.sm_id == sm_obj.id
                    ):
                        nst_value = nst.value

            chk_nsa = models.NilaiSumatifAkhir.query.filter(
                models.NilaiSumatifAkhir.siswa_id == siswa.id,
                models.NilaiSumatifAkhir.mapel_id == mapel.id,
                models.NilaiSumatifAkhir.th_id == th_obj.id,
                models.NilaiSumatifAkhir.sm_id == sm_obj.id,
            ).first()

            # calc nsa
            if naa_value:
                nsa_value = 0
                try:
                    nsa_value = round(
                        nst_value + (naa_value * (bobot.bobot_akhir / 100))
                    )
                except Exception as e:
                    print(
                        "Exception notification: possible zero division erro in handle_nilai_tengah",
                        e,
                    )

                if not chk_nsa:
                    new_nsa = models.NilaiSumatifAkhir(
                        value=nsa_value,
                        naa_value=int(naa_value),
                        siswa_id=siswa.id,
                        mapel_id=mapel.id,
                        th_id=th_obj.id,
                        sm_id=sm_obj.id,
                    )
                    db.session.add(new_nsa)
                    db.session.commit()
                else:
                    if naa_value:
                        to_update_nsa = models.NilaiSumatifAkhir.query.filter(
                            models.NilaiSumatifAkhir.siswa_id == siswa.id,
                            models.NilaiSumatifAkhir.mapel_id == mapel.id,
                            models.NilaiSumatifAkhir.th_id == th_obj.id,
                            models.NilaiSumatifAkhir.sm_id == sm_obj.id,
                        ).first()
                        to_update_nsa.value = nsa_value
                        to_update_nsa.naa_value = naa_value
                        db.session.commit()
        # add na to db
        for siswa in kelas.anggota_kelas:
            nslk_value = 0
            if siswa.nilai_sumatif_lingkup_materi:
                for nslk in siswa.nilai_sumatif_lingkup_materi:
                    if (
                        nslk.value
                        and nslk.mapel_id == mapel.id
                        and nslk.th_id == th_obj.id
                        and nslk.sm_id == sm_obj.id
                    ):
                        nslk_value = nslk.value

            nst_value = 0
            if siswa.nilai_sumatif_tengah:
                for nst in siswa.nilai_sumatif_tengah:
                    if (
                        nst.nat_value
                        and nst.mapel_id == mapel.id
                        and nst.th_id == th_obj.id
                        and nst.sm_id == sm_obj.id
                    ):
                        nst_value = nst.nat_value * (bobot.bobot_tengah / 100)

            nsa_value = 0
            if siswa.nilai_sumatif_akhir:
                for nsa in siswa.nilai_sumatif_akhir:
                    if (
                        nsa.naa_value
                        and nsa.mapel_id == mapel.id
                        and nsa.th_id == th_obj.id
                        and nsa.sm_id == sm_obj.id
                    ):
                        nsa_value = nsa.naa_value * (bobot.bobot_akhir / 100)

            na_value = round(nslk_value + nst_value + nsa_value)

            chk_na = models.NilaiAkhir.query.filter(
                models.NilaiAkhir.siswa_id == siswa.id,
                models.NilaiAkhir.mapel_id == mapel.id,
                models.NilaiAkhir.th_id == th_obj.id,
                models.NilaiAkhir.sm_id == sm_obj.id,
            ).first()

            if nsa_value:
                if not chk_na:
                    new_na = models.NilaiAkhir(
                        value=na_value,
                        siswa_id=siswa.id,
                        mapel_id=mapel.id,
                        th_id=th_obj.id,
                        sm_id=sm_obj.id,
                    )
                    db.session.add(new_na)
                    db.session.commit()
                else:
                    if na_value:
                        to_update_na = models.NilaiAkhir.query.filter(
                            models.NilaiAkhir.siswa_id == siswa.id,
                            models.NilaiAkhir.mapel_id == mapel.id,
                            models.NilaiAkhir.th_id == th_obj.id,
                            models.NilaiAkhir.sm_id == sm_obj.id,
                        ).first()
                        to_update_na.value = na_value
                        db.session.commit()

        flash("Berhasil mengedit nilai akhir", category="success")
    return redirect(
        url_for(
            "views.nilai_akhir",
            th=th_obj.id,
            sm=sm_obj.id,
            mapel_id=mapel.id,
            kelas_id=kelas.id,
            tipe=tipe,
        )
    )


# EXCEL HANDLERS ###
# TODO finish excel handler, create a cetak nilai page view
@login_required
@views.route(
    "/print/<int:th_id>/<int:sm_id>/<int:siswa_id>/<int:kelas_id>/<int:tipe_nilai>",
    methods=["GET"],
)
def excel_handlers(th_id, sm_id, siswa_id, kelas_id, tipe_nilai):
    # data query
    th = models.TahunAjaran.query.get(th_id)
    sm = models.Semester.query.get(sm_id)
    siswa = models.Siswa.query.get(siswa_id)
    kelas = models.Kelas.query.get(kelas_id)
    mapel = models.Mapel.query.filter(models.Mapel.kelas_id == kelas.id)
    kelompok_mapel = models.KelompokMapel.query.all()
    tipe_nilai = tipe_nilai

    from .modules.utils.export_excel import export_to_excel

    if tipe_nilai == 1:
        export_to_excel(th, sm, mapel, kelompok_mapel, kelas, siswa, tipe_nilai=1)
        return redirect(url_for("views.nilai_lingkupmateri"))
    if tipe_nilai == 2:
        export_to_excel(th, sm, mapel, kelompok_mapel, kelas, siswa, tipe_nilai=2)
        flash(
            f"Berhasil mencetak laporan tengah semester {siswa.full_name}",
            category="success",
        )
        return redirect(
            url_for(
                "views.nilai_tengah",
                th=th.id,
                sm=sm.id,
                mapel_id=mapel.id,
                kelas_id=kelas.id,
                tipe=2,
            )
        )
    if tipe_nilai == 3:
        export_to_excel(th, sm, mapel, kelompok_mapel, kelas, siswa, tipe_nilai=3)
        return redirect(url_for("views.nilai_akhir"))

    flash("Terjadi kesalahan pada proses pencetakan excel", category="error")
    return redirect(url_for("views.beranda"))


# PROFILE HANDLERS #
@views.route("/profile", methods=["GET"])
@login_required
def profile():
    current_th = models.TahunAjaran.query.filter(
        models.TahunAjaran.selected == True
    ).first()
    current_sm = models.Semester.query.filter(models.Semester.selected == True).first()

    return render_template(
        "views/profile.html",
        current_th=current_th,
        current_sm=current_sm,
        current_user=current_user,
    )


@views.route("/handle_profile", methods=["POST"])
@login_required
def handle_profile():
    account = models.Account.query.get(int(current_user.id))

    if request.method == "POST":
        new_username = request.form.get("username_input")
        new_pass = request.form.get("password_input")
        new_repass = request.form.get("repassword_input")

        if new_username:
            account.username = new_username
            if new_pass == "" or new_repass == "":
                flash(
                    "Berhasil mengganti username, silahkan login kembali.",
                    category="success",
                )
                db.session.commit()
                return redirect(url_for("auth.logout"))
            flash("Berhasil mengganti username", category="success")
            db.session.commit()

        if new_pass:
            if new_pass == new_repass:
                account.password = generate_password_hash(new_pass)
                flash(
                    "Berhasil mengganti password silahkan login kembali",
                    category="success",
                )
                db.session.commit()
                return redirect(url_for("auth.logout"))
            else:
                flash("Password tidak sama, silahkan coba lagi", category="warning")
                return redirect(url_for("views.profile"))
    return redirect(url_for("views.profile"))


# PROFILE HANDLERS END #


# PENGATURAN HANDLERS #
@views.route("/pengaturan", methods=["GET"])
@login_required
def pengaturan():
    current_th = models.TahunAjaran.query.filter(
        models.TahunAjaran.selected == True
    ).first()
    current_sm = models.Semester.query.filter(models.Semester.selected == True).first()
    all_semester = models.Semester.query.all()
    all_th = models.TahunAjaran.query.all()

    return render_template(
        "views/pengaturan.html",
        all_th=all_th,
        current_th=current_th,
        all_semester=all_semester,
        current_sm=current_sm,
    )


@views.route("/handle_pengaturan", methods=["POST"])
@login_required
def handle_pengaturan():
    current_th = models.TahunAjaran.query.filter(
        models.TahunAjaran.selected == True
    ).first()
    current_sm = models.Semester.query.filter(models.Semester.selected == True).first()

    if request.method == "POST":
        new_th = request.form.get("th_input")
        new_sm = request.form.get("sm_select")
        th_select = request.form.get("th_select")

        if new_th:
            chk_th = models.TahunAjaran.query.filter(
                models.TahunAjaran.value == new_th
            ).first()
            if not chk_th:
                new_th = models.TahunAjaran(value=new_th, selected=True)
                current_th.selected = False
                db.session.add(new_th)
                db.session.commit()
                flash(
                    f"Berhasil menambah tahun ajaran {new_th.value}", category="success"
                )
        else:
            if int(th_select) != current_th.id:
                select_th = models.TahunAjaran.query.get(th_select)
                current_th.selected = False
                select_th.selected = True
                db.session.commit()
                flash(
                    f"Berhasil mengubah tahun ajaran menjadi {select_th.value}",
                    category="success",
                )

        if int(new_sm) != current_sm.id:
            current_sm.selected = False
            selected_sm = models.Semester.query.get(int(new_sm))
            selected_sm.selected = True
            flash("Berhasil mengubah semester.", category="success")

        db.session.commit()
        return redirect(url_for("views.pengaturan"))
    return redirect(url_for("views.pengaturan"))


# PENGATURAN HANDLERS END #
