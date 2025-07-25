__all__ = ["tqdm_pandas"]

def tqdm_pandas(tclass, **tqdm_kwargs) -> None:
    """
    Registers the given `tqdm` instance with
    `pandas.core.groupby.DataFrameGroupBy.progress_apply`.
    """
