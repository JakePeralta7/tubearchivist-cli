# TubeArchivist CLI

A command-line interface for [TubeArchivist](https://github.com/tubearchivist/tubearchivist).

## Quick Start

1. **Install:**
   ```bash
   git clone https://github.com/JakePeralta7/tubearchivist-cli.git
   cd tubearchivist-cli
   pip install requests
   ```

2. **Configure:**
   ```bash
   python tube.py config set
   ```

3. **Sync data:**
   ```bash
   python tube.py sync all
   ```

4. **View stats:**
   ```bash
   python tube.py stats
   ```

## Commands

### Configuration
- `config set` - Configure TubeArchivist connection
- `config get` - Display current configuration

### Data Synchronization
- `sync all` - Download all data to local cache
- `sync videos` - Sync only videos
- `sync channels` - Sync only channels  
- `sync playlists` - Sync only playlists

### Search Content
- `search all <query>` - Search across all content types (videos, channels, playlists)
- `search videos <query>` - Search videos by title, description, or tags
- `search channels <query>` - Search channels by name or description
- `search playlists <query>` - Search playlists by name or description
- `search <query>` - Shortcut for searching all content

### Statistics
- `stats` - View overview statistics
- `stats videos` - Detailed video statistics
- `stats channels` - Detailed channel statistics
- `stats playlists` - Detailed playlist statistics
- `stats database` - Database file information

### Redownload Videos
- `redownload resolution <resolution>` - Redownload all videos with specific resolution (e.g., 360, 720, 1080)
- `redownload failed` - Redownload videos that previously failed to download

### Help
- `help` - Show all available commands
- `help <command>` - Show help for specific command

## License

GPL-3.0
