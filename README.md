# e-rapor-smk-perwira-py
E-Rapor SMK Perwira, perangkat lunak untuk membantu manajemen penilaian siswa dan laporan belajar siswa.
## Run Locally

Make sure python version ^3.12 is installed on your system, python version older than specified are not tested and not guaranteed to work as intended.

Clone the project

```bash
  git clone https://github.com/Trice-IT-Studio/e-rapor-smk-perwira-py.git
```

Go to the project directory

```bash
  cd /path/to/e-rapor-smk-perwira-py
```

Create and activate python venv in project directory

```bash
  pip install virtualenv
  python -m venv env
```
Activate venv on windows

```bash
  ./env/Scripts/activate
```

Activate venv on linux

```bash
  source /env/bin/activate
```

Install dependencies

```bash
  make install
```

Run as web server

```bash
  make runweb
```

Make sure to watch tailwindcss when the server is running to make sure the UI is  updated
```bash
  npx tailwindcss -i /src/static/input.css -o /src/static/dist/css/out.css --watch
```

Run as desktop application

```bash
  make rundesk
```
## Installation

First make sure all dependencies are installed correctly, then run:
```bash
  make build
```

After running the command above, the compiled exe will be located 1 level outside the project file, if your project file are located as follow:

```bash
  /home/Documents/Project/e-rapor-smk-perwira-py/...
```

Then the compiled exe will be in:
```bash
  /home/Documents/Project/erapor_release/...
```
## Features

Implemented features:
- Input Tahun Ajaran dan Semester (Ganjil, Genap)
- Input Kelompok Mata Pelajaran
- Input Kelas
- Input Siswa dan Manajemen Siswa
- Input Mata Pelajaran, Capaian Kompetensi dan Kompetensi Dasar
- Input Bobot Penilaian Lingkup Materi, Sumatif Tengah Semester dan Akhir Semester

Not yet Implemented:
- Pencetakan dalam bentuk Excel


## License

This software is made for internal use of SMK Perwira Jakarta, and not for public usage. any use outside of this is illegal and unauthorized.

