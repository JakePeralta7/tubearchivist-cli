import logging
import requests
from urllib.parse import urljoin
import urllib3
from tubearchivist_cli.cli.config import Config
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class TubeArchivistAPI:
    def __init__(self):
        config = Config()
        if config.is_configured():
            config = config.config_table.get_config()
            self.base_url, self.api_key = config[0]
            self.headers = {
                'Authorization': f'Token {self.api_key}',
                'Content-Type': 'application/json'
            }
            self.session = requests.Session()
            self.session.verify = False
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            self.session.headers.update(self.headers)
        else:
            raise ValueError("API not configured")
    
    def test_connection(self) -> bool:
        """Test API connection"""
        try:
            response = self.session.get(urljoin(self.base_url, '/api/video/'))
            response.raise_for_status()
            logger.info("Successfully connected to TubeArchivist API")
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to connect to TubeArchivist API: {e}")
            return False

    def get_videos(self, page: int = 1, page_size: int = 25) -> Optional[Dict]:
        """Get videos from TubeArchivist"""
        try:
            params = {'page': page, 'page_size': page_size}
            response = self.session.get(
                urljoin(self.base_url, '/api/video/'),
                params=params,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get videos: {e}")
            return None
    
    def get_all_videos(self) -> List[Dict]:
        """Get all videos from TubeArchivist"""
        all_videos = []
        page = 1
        
        while True:
            logger.info(f"Fetching page {page}...")
            data = self.get_videos(page=page, page_size=50)
            
            if not data or 'data' not in data:
                logger.warning(f"No data received for page {page}")
                break
            
            videos = data['data']
            if not videos:
                logger.info(f"No videos found on page {page}")
                break
            
            all_videos.extend(videos)
            logger.info(f"Page {page}: Retrieved {len(videos)} videos (total so far: {len(all_videos)})")
            
            # Check pagination info
            paginate = data.get('paginate', {})
            logger.debug(f"Pagination info: {paginate}")
            
            # Check if this is the last page - fixed logic
            current_page = paginate.get('current_page', page)
            last_page = paginate.get('last_page')
            
            # If current page equals last page number, we're done
            if isinstance(last_page, int) and current_page >= last_page:
                logger.info(f"Reached last page ({current_page}/{last_page})")
                break
            # Fallback: if no next pages listed, we're done    
            elif not paginate.get('next_pages'):
                logger.info("No more pages available")
                break
            
            page += 1
        
        logger.info(f"Retrieved {len(all_videos)} total videos")
        return all_videos
    
    def redownload_video(self, video_id: str) -> bool:
        """Trigger redownload of a specific video"""
        try:
            # Use the correct API format as shown in browser dev tools
            data = {
                "data": [
                    {
                        "youtube_id": video_id,
                        "status": "pending"
                    }
                ]
            }
            response = self.session.post(
                urljoin(self.base_url, '/api/download/?autostart=true&force=true'),
                json=data
            )
            response.raise_for_status()
            logger.info(f"Successfully queued video {video_id} for redownload")
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to queue video {video_id} for redownload: {e}")
            return False

    def get_playlists(self, page: int = 1, page_size: int = 25) -> Optional[Dict]:
        """Get playlists from TubeArchivist"""
        try:
            params = {'page': page, 'page_size': page_size}
            response = self.session.get(
                urljoin(self.base_url, '/api/playlist/'),
                params=params,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get playlists: {e}")
            return None

    def get_all_playlists(self) -> List[Dict]:
        """Get all playlists from TubeArchivist"""
        all_playlists = []
        page = 1
        
        while True:
            logger.info(f"Fetching playlists page {page}...")
            data = self.get_playlists(page=page, page_size=50)
            
            if not data or 'data' not in data:
                logger.warning(f"No playlist data received for page {page}")
                break
            
            playlists = data['data']
            if not playlists:
                logger.info(f"No playlists found on page {page}")
                break
            
            all_playlists.extend(playlists)
            logger.info(f"Page {page}: Retrieved {len(playlists)} playlists (total so far: {len(all_playlists)})")
            
            # Check pagination info
            paginate = data.get('paginate', {})
            logger.debug(f"Pagination info: {paginate}")
            
            # Check if this is the last page
            current_page = paginate.get('current_page', page)
            last_page = paginate.get('last_page')
            
            if isinstance(last_page, int) and current_page >= last_page:
                logger.info(f"Reached last page ({current_page}/{last_page})")
                break
            elif not paginate.get('next_pages'):
                logger.info("No more pages available")
                break
            
            page += 1
        
        logger.info(f"Retrieved {len(all_playlists)} total playlists")
        return all_playlists

    def get_channels(self, page: int = 1, page_size: int = 25) -> Optional[Dict]:
        """Get channels from TubeArchivist"""
        try:
            params = {'page': page, 'page_size': page_size}
            response = self.session.get(
                urljoin(self.base_url, '/api/channel/'),
                params=params,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get channels: {e}")
            return None

    def get_all_channels(self) -> List[Dict]:
        """Get all channels from TubeArchivist"""
        all_channels = []
        page = 1
        
        while True:
            logger.info(f"Fetching channels page {page}...")
            data = self.get_channels(page=page, page_size=50)
            
            if not data or 'data' not in data:
                logger.warning(f"No channel data received for page {page}")
                break
            
            channels = data['data']
            if not channels:
                logger.info(f"No channels found on page {page}")
                break
            
            all_channels.extend(channels)
            logger.info(f"Page {page}: Retrieved {len(channels)} channels (total so far: {len(all_channels)})")
            
            # Check pagination info
            paginate = data.get('paginate', {})
            logger.debug(f"Pagination info: {paginate}")
            
            # Check if this is the last page
            current_page = paginate.get('current_page', page)
            last_page = paginate.get('last_page')
            
            if isinstance(last_page, int) and current_page >= last_page:
                logger.info(f"Reached last page ({current_page}/{last_page})")
                break
            elif not paginate.get('next_pages'):
                logger.info("No more pages available")
                break
            
            page += 1
        
        logger.info(f"Retrieved {len(all_channels)} total channels")
        return all_channels
