from typing import Literal, TypedDict
from typing_extensions import TypeAlias

import numpy as np
import numpy.typing as npt

from .coco import COCO

_NDFloatArray: TypeAlias = npt.NDArray[np.float64]
_TIOU: TypeAlias = Literal["segm", "bbox", "keypoints"]

class _ImageEvaluationResult(TypedDict):
    image_id: int
    category_id: int
    aRng: list[int]
    maxDet: int
    dtIds: list[int]
    gtIds: list[int]
    dtMatches: _NDFloatArray
    gtMatches: _NDFloatArray
    dtScores: list[float]
    gtIgnore: _NDFloatArray
    dtIgnore: _NDFloatArray

class _EvaluationResult(TypedDict):
    params: Params
    counts: list[int]
    date: str
    precision: _NDFloatArray
    recall: _NDFloatArray
    scores: _NDFloatArray

class COCOeval:
    cocoGt: COCO
    cocoDt: COCO
    evalImgs: list[_ImageEvaluationResult]
    eval: _EvaluationResult
    params: Params
    stats: _NDFloatArray
    ious: dict[tuple[int, int], list[float]]
    def __init__(self, cocoGt: COCO | None = None, cocoDt: COCO | None = None, iouType: _TIOU = "segm") -> None:
        """
        Initialize CocoEval using coco APIs for gt and dt
        :param cocoGt: coco object with ground truth annotations
        :param cocoDt: coco object with detection results
        :return: None
        """

    def evaluate(self) -> None:
        """
        Run per image evaluation on given images and store results (a list of dict) in self.evalImgs
        :return: None
        """

    def computeIoU(self, imgId: int, catId: int) -> list[float]: ...
    def computeOks(self, imgId: int, catId: int) -> _NDFloatArray: ...
    def evaluateImg(self, imgId: int, catId: int, aRng: list[int], maxDet: int) -> _ImageEvaluationResult:
        """
        perform evaluation for single category and image
        :return: dict (single image results)
        """

    def accumulate(self, p: Params | None = None) -> None:
        """
        Accumulate per image evaluation results and store the result in self.eval
        :param p: input params for evaluation
        :return: None
        """

    def summarize(self) -> None:
        """
        Compute and display summary metrics for evaluation results.
        Note this functin can *only* be applied on the default parameter setting
        """

class Params:
    """
    Params for coco evaluation api
    """

    imgIds: list[int]
    catIds: list[int]
    iouThrs: _NDFloatArray
    recThrs: _NDFloatArray
    maxDets: list[int]
    areaRng: list[list[float]]
    areaRngLbl: list[str]
    useCats: int
    kpt_oks_sigmas: _NDFloatArray
    iouType: _TIOU
    useSegm: int | None
    def __init__(self, iouType: _TIOU = "segm") -> None: ...
    def setDetParams(self) -> None: ...
    def setKpParams(self) -> None: ...
