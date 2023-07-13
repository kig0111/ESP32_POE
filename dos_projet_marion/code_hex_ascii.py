#
# This file is part of the BIOM_AID distribution (https://bitbucket.org/kig13/dem/).
# Copyright (c) 2023 Romuald Kliglich, Marion Normand, Loic Degrugilliers.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

import codecs

fichier = open("C:/Users/drbstag/Desktop/dos_projet_marion/data_incubateur.txt", "r")
fichierW = open("C:/Users/drbstag/Desktop/dos_projet_marion/data_incubateur.bin", "wb")
res = fichier.read()
print("res   " + res)

res = codecs.decode(res, "hex")
print(str(res,'utf-8'))
print("ascii :   " + str(res))

fichierW.write(res)

fichier.close() 
fichierW.close() 
