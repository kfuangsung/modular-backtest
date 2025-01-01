from talib._ta_lib import MA_Type

class BBANDS:
    def __init__(
        self,
        *,
        timeperiod: int = 5,
        nbdevup: int = 2,
        nbdevdn: int = 2,
        matype: MA_Type = MA_Type.SMA,
    ) -> None: ...
