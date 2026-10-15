import pytest
from cache import LRUCache
from predictor import FrequencyPredictor


def test_lru_hits_misses_eviction_and_ratio():
    cache = LRUCache(2)
    assert cache.get(1) is None
    cache.put(1); cache.put(2)
    assert cache.get(1) == 1
    cache.put(3)
    assert cache.get(2) is None
    assert cache.hits == 1 and cache.misses == 2
    assert cache.hit_ratio == pytest.approx(1 / 3)


def test_predicted_entry_is_not_normal_hit():
    cache = LRUCache(2)
    cache.preload(7)
    assert cache.get(7) == 7
    assert cache.hits == 0 and cache.prediction_hits == 1


def test_transition_predictor_learns_and_scores_prediction():
    model = FrequencyPredictor()
    for block in [1, 2, 1, 2]:
        model.observe(block)
    assert model.predict([1]) == [2]
    model.observe(2)
    assert model.correct_predictions == 1
    assert model.accuracy == 1
