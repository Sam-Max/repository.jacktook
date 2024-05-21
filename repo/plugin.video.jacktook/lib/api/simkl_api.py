import json
import requests

class SIMKLAPI:
    def __init__(self):
        self.ClientID = (
            "59dfdc579d244e1edf6f89874d521d37a69a95a1abd349910cb056a1872ba2c8"
        )
        self.base_url = "https://api.simkl.com/"
        self.imagePath = "https://wsrv.nl/?url=https://simkl.in/episodes/%s_w.webp"

    def _to_url(self, url=""):
        if url.startswith("/"):
            url = url[1:]
        return "%s/%s" % (self.baseUrl[:-1], url)

    def make_request(self, endpoint, params):
        res = requests.get(
            f"{self.base_url}{endpoint}",
            params=params,
        )
        if res.status_code == 200:
            return json.loads(res.text)
        else:
            raise Exception(f"Simkl Error::{res.text}")

    def get_anime_info(self, anilist_id):
        _, simkl_id = self.get_simkl_id("anilist", anilist_id)
        params = {"extended": "full", "client_id": self.ClientID}
        return self.make_request("anime/" + str(simkl_id), params=params)

    def get_anilist_episodes(self, mal_id):
        _, simkl_id = self.get_simkl_id("mal", mal_id)
        params = {
            "extended": "full",
        }
        return self.make_request("anime/episodes/" + str(simkl_id), params=params)

    def get_simkl_id(self, send_id, anime_id):
        params = {
            send_id: anime_id,
            "client_id": self.ClientID,
        }
        res = self.make_request("search/id", params=params)
        simkl = res[0]["ids"]["simkl"]
        return simkl

    def get_mapping_ids(self, send_id, anime_id):
        simkl_id = self.get_simkl_id(send_id, anime_id)
        params = {"extended": "full", "client_id": self.ClientID}
        res = self.make_request("anime/" + str(simkl_id), params=params)
        return res["ids"]
