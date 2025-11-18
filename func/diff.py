from func.convert import *


def isASimilarFormat(filePathOrg: str) -> bool:
    listPath = filePathOrg.split("/")
    getFname = str("".join(listPath[-1]))[::-1].split(".", 1)[1][::-1]

    for ext, codec in lossyFormat.items():
        outputPath = os.path.join("processing", f"{getFname}.{ext}")
        if (diff(filePathOrg, outputPath) > 0.98):  # TODO Armand find this constant
            return True

    return False


def diff(filePathOrg: str, filePathConverted: str) -> float:
    """Takes two filepath (relative or absolute), reads both, put it into 2 arrays (sf.read())
    Then calculates the pourcentage of difference between two arrays.
    :return float: pourcentage of difference between two arrays"""

    # TODO /Doc/diff().jpeg
    # TODO Armand

    return 0.0
