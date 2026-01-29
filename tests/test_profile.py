import json

from kingshot_helper.models.profile import UserProfile


def test_profile_create_save_load(tmp_path):
    p = UserProfile(name="test", town_center_level=20)
    path = p.save(tmp_path / "test.json")
    assert path.exists()

    loaded = UserProfile.load(path)
    assert loaded.name == "test"
    assert loaded.town_center_level == 20


def test_profile_json_roundtrip(tmp_path):
    p = UserProfile(name="roundtrip", town_center_level=25)
    path = p.save(tmp_path / "rt.json")
    data = json.loads(path.read_text())
    assert data["name"] == "roundtrip"
    assert data["town_center_level"] == 25


def test_profile_defaults():
    p = UserProfile()
    assert p.name == "default"
    assert p.town_center_level == 1
    assert p.heroes == []
    assert p.resources.bread == 0


def test_profile_with_heroes(mid_game_profile):
    assert len(mid_game_profile.heroes) == 2
    assert mid_game_profile.heroes[0].name == "Howard"
    assert mid_game_profile.heroes[0].stars == 3
