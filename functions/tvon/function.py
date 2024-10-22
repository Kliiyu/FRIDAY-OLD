import time
import pychromecast
from pychromecast.controllers.youtube import YouTubeController
import zeroconf

YOUTUBE_VIDEO_ID = "JFKrq4MSzIE"
PLAYER = "AdrianCC#01"

def main():
    chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=[PLAYER])
    
    try:
        cast = chromecasts[0]
        cast.wait()
        print(f"Connected to {cast.cast_info.friendly_name}")
        
        yt = pychromecast.controllers.youtube.YouTubeController()
        cast.register_handler(yt)
        yt.play_video(YOUTUBE_VIDEO_ID)
        
        pychromecast.discovery.stop_discovery(browser)
    except IndexError:
        print("No Chromecast with name 'AdrianCC#01' found")
    except pychromecast.error.NotConnected:
        print("Chromecast disconnected during setup")
    except pychromecast.error.ProtocolError:
        print("Got a protocol error")
    except zeroconf.BadStateError:
        print("Zeroconf got a bad state error")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()