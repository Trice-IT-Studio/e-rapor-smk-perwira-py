from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from flask_login import LoginManager

import os
import sys
import platform

db = SQLAlchemy()
DB_NAME = "data.db"


def App(root_dir):
    # BASIC CONFIG
    app = Flask(__name__, static_folder="./static", template_folder="./templates")
    app.config["SECRET_KEY"] = "secret"
    app.config["DEBUG"] = True
    if platform.system() == "Windows":
        app.config["SQLALCHEMY_DATABASE_URI"] = (
            f"sqlite:///{root_dir}\\instance\\{DB_NAME}"
        )
    elif platform.system() == "Linux":
        app.config["SQLALCHEMY_DATABASE_URI"] = (
            f"sqlite:////{root_dir}/instance/{DB_NAME}"
        )
    db.init_app(app)

    # BLUEPRINTS
    from .auth import auth
    from .views import views

    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(views, url_prefix="/dashboard")

    # LOGIN MANAGER
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Silahkan login dahulu."

    @login_manager.user_loader
    def load_user(user_id):
        with app.app_context():
            from .models import Account

            return Account.query.get(int(user_id))

    # DATABASE INIT
    from . import models

    init_db(app, root_dir)
    create_default_user(app)
    create_default_semester(app)
    create_default_tahunajar(app)
    create_default_tingkat(app)

    # TEST DUMMY DATA
    try:
        from .testing_modules.generate_dummy_data import (  # type: ignore
            generate_dummy_mapel,
            generate_dummy_kelas,
            generate_dummy_kelompok_mapel,
            generate_dummy_capaiankom,
            generate_dummy_kompetensidas,
            generate_dummy_siswa,
        )

        generate_dummy_mapel(app)
        generate_dummy_kelas(app)
        generate_dummy_kelompok_mapel(app)
        generate_dummy_capaiankom(app)
        generate_dummy_kompetensidas(app)
        generate_dummy_siswa(app)
    except Exception as e:
        print("INFO: Possible testing modules is missing. ", e)

    return app


def init_db(app, root_dir):
    # GENERATE DB FILE
    if not os.path.isdir(f"{root_dir}/instance"):
        print(f'INFO: db dir "{root_dir}/instance" not found, creating dir...')
        os.makedirs(f"{root_dir}/instance")
        print("INFO: Dir generated.")

    if not os.path.isfile(f"{root_dir}/instance/data.db"):
        print("[!] No DB file found, creating db file...")
        with app.app_context():
            db.create_all()
            print("[+] DB successfully created.")
            return
    print("DB alredy exist")


def create_default_user(app):
    with app.app_context():
        from .models import Account

        check_user = Account.query.filter(Account.id == 1).first()
        if not check_user:
            print("[!] default user not found, creating default user account...")
            new_user = Account(
                username="guru",
                # TODO REMOVE PUBLIC PASSWORD!!!
                password=generate_password_hash("password"),
            )
            db.session.add(new_user)
            db.session.commit()
            print("[+] default user successfully created.")
        print("[-] default user already exists.")


def create_default_semester(app):
    with app.app_context():
        from .models import Semester

        ganjil = Semester.query.filter(Semester.value == "Ganjil").first()
        genap = Semester.query.filter(Semester.value == "Genap").first()
        if not ganjil:
            new_sm = Semester(value="Ganjil", selected=True)
            db.session.add(new_sm)
            db.session.commit()
            print("[+] Semester Ganjil generated.")
        if not genap:
            new_sm = Semester(value="Genap", selected=False)
            db.session.add(new_sm)
            db.session.commit()
            print("[+] Semester Genap generated.")
        print("[-] Both Semester already exists.")


def create_default_tahunajar(app):
    with app.app_context():
        from .models import TahunAjaran
        import datetime

        check_th = TahunAjaran.query.filter(TahunAjaran.id == 1).first()
        if not check_th:
            current_year = datetime.date.today().year
            print(
                f"[!] Tahun ajaran not found, generating current: {int(current_year) - 1}/{int(current_year)}"
            )
            new_th = TahunAjaran(
                value=f"{int(current_year) - 1}/{int(current_year)}", selected=True
            )
            db.session.add(new_th)
            db.session.commit()
            print(
                f"[+] Tahun ajaran {int(current_year) - 1}/{int(current_year)} generated."
            )
        print("[-] Tahun ajaran already exists.")


def create_default_tingkat(app):
    with app.app_context():
        from .models import Tingkat, Kelas

        chk_tngkt = Tingkat.query.get(1)

        if not chk_tngkt:
            print("[!] No tingkat found, generating...")
            for tngkt in ["10", "11", "12"]:
                new_tngkt = Tingkat(value=tngkt)
                db.session.add(new_tngkt)
                db.session.commit()
            print("[+] Tingkat generated.")
        print("[-] Tingkat already exists.")
