
from app.screener2 import mkt_cap_format, vol_format, convert_modtime_to_date 


def test_mkt_cap_format():
    result = mkt_cap_format(700000000)
    assert result == '$700.0M'

def test_vol_format():
    result = vol_format(100000000)
    assert result == '100.0M'


#def test_convert_modtime_to_date():
    #print("ok")