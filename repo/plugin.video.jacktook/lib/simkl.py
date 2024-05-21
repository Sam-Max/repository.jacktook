import os
import re
from lib.api.fma_api import FindMyAnime, extract_season
from lib.api.jacktook.kodi import kodilog
from lib.api.simkl_api import SIMKLAPI
from lib.utils.kodi import ADDON_PATH, get_kodi_version, url_for
from lib.utils.utils import (
    get_cached,
    set_cached,
    set_video_info,
    set_video_infotag,
)
from xbmcgui import ListItem
from xbmcplugin import addDirectoryItem, endOfDirectory


IMAGE_PATH = "https://wsrv.nl/?url=https://simkl.in/episodes/%s_w.webp"


def search_simkl_episodes(title, anilist_id, mal_id, plugin):
    fma = FindMyAnime()
    data = fma.get_anime_data(anilist_id, "Anilist")
    s_id = extract_season(data[0]) if data else ""
    season = s_id[0] if s_id else 1
    try:
        res = search_simkl_api(mal_id)
        simkl_parse_show_results(res, title, season, plugin)
    except Exception as e:
        kodilog(e)


def search_simkl_api(mal_id):
    cached_results = get_cached(type, params=(mal_id))
    if cached_results:
        return cached_results

    simkl = SIMKLAPI()
    res = simkl.get_anilist_episodes(mal_id)

    set_cached(res, type, params=(mal_id))
    return res


def simkl_parse_show_results(response, title, season, plugin):
    for res in response:
        if res["type"] == "episode":
            episode = res["episode"]
            ep_name = res.get("title")
            if ep_name:
                ep_name = f"{season}x{episode} {ep_name}"
            else:
                ep_name = f"Episode {episode}"
            
            description = res.get("description", "")

            date = res.get("date", "")
            match = re.search(r"\d{4}-\d{2}-\d{2}", date)
            if match:
                date = match.group()

            poster = IMAGE_PATH % res.get("img", "")

            list_item = ListItem(label=ep_name)
            list_item.setArt(
                {
                    "poster": poster,
                    "icon": os.path.join(
                        ADDON_PATH, "resources", "img", "trending.png"
                    ),
                    "fanart": poster,
                }
            )
            list_item.setProperty("IsPlayable", "false")

            if get_kodi_version() >= 20:
                set_video_infotag(
                    list_item,
                    mode="tv",
                    name=ep_name,
                    overview=description,
                    ep_name=ep_name,
                    air_date=date,
                )
            else:
                set_video_info(
                    list_item,
                    mode="tv",
                    name=ep_name,
                    overview=description,
                    ep_name=ep_name,
                    air_date=date,
                )

            addDirectoryItem(
                plugin.handle,
                url_for(
                    name="search",
                    mode="anime",
                    query=title,
                    ids=f"{-1}, {-1}, {-1}",
                    tv_data=f"{ep_name}(^){episode}(^){season}",
                ),
                list_item,
                isFolder=True,
            )

    endOfDirectory(plugin.handle)
