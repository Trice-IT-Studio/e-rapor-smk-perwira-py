from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment
import os


def export_to_excel(
    th_obj, sm_obj, mapel_obj, kel_mapel_obj, kelas_obj, siswa_obj, **kwargs
):
    """
    create a report of nilai siswa (Tengah semester & akhir semester)
    and save it as an excel formated file.

    th_id           tahun ajaran object
    sm_id           semester object
    mapel_obj       mata pelajaran object
    kelas_obj       kelas object
    siswa_obj       siswa object
    """
    wb = Workbook()
    ws = wb.active

    # keyword argumetns
    tipe_nilai = kwargs.get("tipe_nilai", None)

    th_value = "".join(th_obj.value.split("/"))

    if not os.path.isdir("data_nilai"):
        os.makedirs("data_nilai")

    # SAVE NILAI LINGKUP MATER TO EXCEL
    if tipe_nilai == 1:
        pass

    # SAVE NILAI PTS TO EXCEL ###
    if tipe_nilai == 2:
        # PREPARE TITLE
        ws.merge_cells("A1:F1")
        title_cell = ws["A1"]
        title_cell.value = "LAPORAN HASIL BELAJAR\nSUMATIF TENGAH SEMESTER\n(RAPOR)"
        title_cell.alignment = Alignment(
            horizontal="center", vertical="center", wrap_text=True
        )

        # STUDENTS INFORMATION
        ws.column_dimensions["B"].width = 20
        ws.column_dimensions["C"].width = 5
        ws.column_dimensions["D"].width = 15
        ws.column_dimensions["E"].width = 20
        ws.column_dimensions["f"].width = 20

        active_cell = ws["B2"]
        active_cell.value = "Nama Peserta Didik"
        ws.merge_cells("C2:D2")
        active_cell = ws["C2"]
        active_cell.value = f": {siswa_obj.full_name}"

        active_cell = ws["B3"]
        active_cell.value = "NISN"
        ws.merge_cells("C3:D3")
        active_cell = ws["C3"]
        active_cell.value = f": {siswa_obj.nisn}"

        active_cell = ws["B4"]
        active_cell.value = "Sekolah"
        ws.merge_cells("C4:D4")
        active_cell = ws["C4"]
        active_cell.value = ": SMK Perwira Jakarta"

        active_cell = ws["B5"]
        active_cell.value = f"Alamat"
        ws.merge_cells("C5:D5")
        active_cell = ws["C5"]
        active_cell.value = f": {siswa_obj.alamat}"

        active_cell = ws["E2"]
        active_cell.value = "Kelas"
        active_cell = ws["F2"]
        active_cell.value = f": {kelas_obj.name}"

        active_cell = ws["E3"]
        active_cell.value = "Fase"
        active_cell = ws["F3"]
        active_cell.value = ": E"

        active_cell = ws["E4"]
        active_cell.value = "Semester"
        active_cell = ws["F4"]
        active_cell.value = f": {sm_obj.value}"

        active_cell = ws["E5"]
        active_cell.value = "Tahun Ajaran"
        active_cell = ws["F5"]
        active_cell.value = f": {th_obj.value}"

        # NILAI SECTION
        kel_mapel = [kel_mapel.category for kel_mapel in kel_mapel_obj]

        for index, kel_mapel in enumerate(kel_mapel):
            # INDEX COL
            active_cell = ws[f"A{6+index}"]
            active_cell.value = chr(65 + index)

            # VALUE COL
            ws.merge_cells(f"B{6+index}:F{6+index}")
            active_cell = ws[f"B{6+index}"]
            active_cell.value = f"Kelompok Mata Pelajaran {kel_mapel}"
            for mapel in mapel_obj:
                if mapel.kelas_id == kelas_obj.id:
                    ws.append([index, mapel.name])

        # EXPORT EXCEL
        wb.save(
            f"data_nilai/PTS_{th_value}-{sm_obj.value}_{kelas_obj.name}_{siswa_obj.full_name}.xlsx"
        )
        return

    # SAVE NILAI AKHIR TO EXCEL ###
    if tipe_nilai == 3:
        pass

    return Exception("No tipe nilai provided or not implemented")
