from collections.abc import Collection, Sequence
from pathlib import Path
from typing import Generic, Literal, TypedDict, TypeVar, overload
from typing_extensions import TypeAlias

import numpy as np
import numpy.typing as npt

from . import _EncodedRLE

PYTHON_VERSION: int

class _Image(TypedDict):
    id: int
    width: int
    height: int
    file_name: str

_TPolygonSegmentation: TypeAlias = list[list[float]]

class _RLE(TypedDict):
    size: list[int]
    counts: list[int]

class _Annotation(TypedDict):
    id: int
    image_id: int
    category_id: int
    segmentation: _TPolygonSegmentation | _RLE | _EncodedRLE
    area: float
    bbox: list[float]
    iscrowd: int

_TSeg = TypeVar("_TSeg", _TPolygonSegmentation, _RLE, _EncodedRLE)

class _AnnotationG(TypedDict, Generic[_TSeg]):
    id: int
    image_id: int
    category_id: int
    segmentation: _TSeg
    area: float
    bbox: list[float]
    iscrowd: int

class _Category(TypedDict):
    id: int
    name: str
    supercategory: str

class _Dataset(TypedDict):
    images: list[_Image]
    annotations: list[_Annotation]
    categories: list[_Category]

class COCO:
    anns: dict[int, _Annotation]
    dataset: _Dataset
    cats: dict[int, _Category]
    imgs: dict[int, _Image]
    imgToAnns: dict[int, list[_Annotation]]
    catToImgs: dict[int, list[int]]
    def __init__(self, annotation_file: str | Path | None = None) -> None:
        """
        Constructor of Microsoft COCO helper class for reading and visualizing annotations.
        :param annotation_file (str): location of annotation file
        :param image_folder (str): location to the folder that hosts images.
        :return:
        """

    def createIndex(self) -> None: ...
    def info(self) -> None:
        """
        Print information about the annotation file.
        :return:
        """

    def getAnnIds(
        self,
        imgIds: Collection[int] | int = [],
        catIds: Collection[int] | int = [],
        areaRng: Sequence[float] = [],
        iscrowd: bool | None = None,
    ) -> list[int]:
        """
        Get ann ids that satisfy given filter conditions. default skips that filter
        :param imgIds  (int array)     : get anns for given imgs
               catIds  (int array)     : get anns for given cats
               areaRng (float array)   : get anns for given area range (e.g. [0 inf])
               iscrowd (boolean)       : get anns for given crowd label (False or True)
        :return: ids (int array)       : integer array of ann ids
        """

    def getCatIds(
        self, catNms: Collection[str] | str = [], supNms: Collection[str] | str = [], catIds: Collection[int] | int = []
    ) -> list[int]:
        """
        filtering parameters. default skips that filter.
        :param catNms (str array)  : get cats for given cat names
        :param supNms (str array)  : get cats for given supercategory names
        :param catIds (int array)  : get cats for given cat ids
        :return: ids (int array)   : integer array of cat ids
        """

    def getImgIds(self, imgIds: Collection[int] | int = [], catIds: list[int] | int = []) -> list[int]:
        """
        Get img ids that satisfy given filter conditions.
        :param imgIds (int array) : get imgs for given ids
        :param catIds (int array) : get imgs with all given cats
        :return: ids (int array)  : integer array of img ids
        """

    def loadAnns(self, ids: Collection[int] | int = []) -> list[_Annotation]:
        """
        Load anns with the specified ids.
        :param ids (int array)       : integer ids specifying anns
        :return: anns (object array) : loaded ann objects
        """

    def loadCats(self, ids: Collection[int] | int = []) -> list[_Category]:
        """
        Load cats with the specified ids.
        :param ids (int array)       : integer ids specifying cats
        :return: cats (object array) : loaded cat objects
        """

    def loadImgs(self, ids: Collection[int] | int = []) -> list[_Image]:
        """
        Load anns with the specified ids.
        :param ids (int array)       : integer ids specifying img
        :return: imgs (object array) : loaded img objects
        """

    def showAnns(self, anns: Sequence[_Annotation], draw_bbox: bool = False) -> None:
        """
        Display the specified annotations.
        :param anns (array of object): annotations to display
        :return: None
        """

    def loadRes(self, resFile: str) -> COCO:
        """
        Load result file and return a result api object.
        :param   resFile (str)     : file name of result file
        :return: res (obj)         : result api object
        """

    def download(self, tarDir: str | None = None, imgIds: Collection[int] = []) -> Literal[-1] | None:
        """
        Download COCO images from mscoco.org server.
        :param tarDir (str): COCO results directory name
               imgIds (list): images to be downloaded
        :return:
        """

    def loadNumpyAnnotations(self, data: npt.NDArray[np.float64]) -> list[_Annotation]:
        """
        Convert result data from a numpy array [Nx7] where each row contains {imageID,x1,y1,w,h,score,class}
        :param  data (numpy.ndarray)
        :return: annotations (python nested list)
        """

    @overload
    def annToRLE(self, ann: _AnnotationG[_RLE]) -> _RLE:
        """
        Convert annotation which can be polygons, uncompressed RLE to RLE.
        :return: binary mask (numpy 2D array)
        """

    @overload
    def annToRLE(self, ann: _AnnotationG[_EncodedRLE]) -> _EncodedRLE: ...
    @overload
    def annToRLE(self, ann: _AnnotationG[_TPolygonSegmentation]) -> _EncodedRLE: ...
    def annToMask(self, ann: _Annotation) -> npt.NDArray[np.uint8]:
        """
        Convert annotation which can be polygons, uncompressed RLE, or RLE to binary mask.
        :return: binary mask (numpy 2D array)
        """
