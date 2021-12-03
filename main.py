# FUNCION PARA COLAGE
from colageImg import opacidadImagenes
contador = 101
# PATHS
PathImagOri = r"./MosaicoPython/public/rel"
PathImagenesRe = r"./MosaicoPython/public/Img"
PathImagenAgua = r"./MosaicoPython/fondo.jpg"

# PONERLO EN EL METODO GET
opacidadImagenes(PathImagOri, PathImagenesRe, PathImagenAgua, contador)