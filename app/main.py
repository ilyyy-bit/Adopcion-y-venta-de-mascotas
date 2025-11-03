
from app.config import ensure_data_files
from app.repositories.personas_file_repo import PersonasFileRepo
from app.repositories.mascotas_file_repo import MascotasFileRepo
from app.repositories.registros_file_repo import RegistrosFileRepo
from app.repositories.alianzas_file_repo import AlianzasFileRepo
from app.repositories.banners_file_repo import BannersFileRepo
from app.services.plataforma import Plataforma
def main():
    ensure_data_files()
    Plataforma(
        personas=PersonasFileRepo(),
        mascotas=MascotasFileRepo(),
        registros=RegistrosFileRepo(),
        alianzas=AlianzasFileRepo(),
        banners=BannersFileRepo(),
    )
    print("Prototipo listo")
if __name__ == "__main__":
    main()
