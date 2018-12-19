import sys, os
print(os.getcwd())
code_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, code_path + '/../gsadjust')
sys.path.insert(0, code_path)

from test_fixture_pyqt import test_channellist_fixture, test_twostations_fixture, test_threestations_fixture
from data_objects import Delta
import pytest



@pytest.mark.parametrize('test_channellist_fixture, mean_g, station_length, station_subset_length',[
                         ('./tests/channellist_burris_single.p', 3092327.454, 11, 10),
                         ('./tests/channellist_scintrex.p', 2639321.583, 2096, 11)
                         ], indirect=['test_channellist_fixture'])
def test_channellist(test_channellist_fixture, mean_g, station_length, station_subset_length):
    assert len(test_channellist_fixture.raw_grav) == station_length
    test_data1 = test_channellist_fixture.extract_subset_idx(0, station_subset_length)
    assert len(test_data1.raw_grav) - 1 == station_subset_length
    mean = sum(test_data1.raw_grav) / len(test_data1.raw_grav)
    assert abs(mean - mean_g) < 0.001


@pytest.mark.parametrize('test_twostations_fixture, true_delta_g, true_sd',[
                         ('./tests/channellist_scintrex.p', 2159.339, 11.94092),
                         ('./tests/channellist_burris.p', -3205.8182, 3.8052),
                         ], indirect=['test_twostations_fixture'])
def test_delta_normal(test_twostations_fixture, true_delta_g, true_sd):
    sta1 = test_twostations_fixture[0]
    sta2 = test_twostations_fixture[1]
    # Test that delta with default values is the same as one with defaults specified
    d1 = Delta(sta1, sta2, driftcorr=0., ls_drift=None, delta_type='normal', checked=2,adj_sd=999)
    d2 = Delta(sta1, sta2)
    assert d1.__dict__ == d2.__dict__
    assert abs(d1.dg - true_delta_g) < 0.001
    assert abs(d1.sd - true_sd) < 0.001


@pytest.mark.parametrize('test_threestations_fixture, true_delta_g, true_sd, true_sta1_t',[
                         (('./tests/channellist_scintrex.p', [0, 1, 8]), -2142.9737, 3.0, 735126.287),
                         (('./tests/channellist_burris.p', [1, 2, 5]), -462.8575, 3.0, 736807.9041),
                         ], indirect=['test_threestations_fixture'])
def test_delta_threepoint(test_threestations_fixture, true_delta_g, true_sd, true_sta1_t):
    sta1a = test_threestations_fixture[0]
    sta2 = test_threestations_fixture[1]
    sta1b = test_threestations_fixture[2]
    d1 = Delta(sta2, [sta1a, sta1b], driftcorr=0., ls_drift=None, delta_type='three_point', checked=2, adj_sd=999)
    assert abs(d1.dg - true_delta_g) < 0.001
    assert abs(d1.sd - true_sd) < 0.001
    assert abs(d1.sta1_t - true_sta1_t) < 0.001
