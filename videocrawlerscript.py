import os
import scrapy
from scrapy.crawler import CrawlerProcess
from yt_dlp import YoutubeDL

class WebSpider(scrapy.Spider):
    name = "web_crawler"
    start_urls = ['https://example.com']  # Replace with your target website

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.video_found = False  # Flag to stop after finding one video

    def parse(self, response):
        # Check if a video has already been found and downloaded
        if self.video_found:
            return

        # Look for links with video file extensions or streaming formats
        video_urls = response.xpath("//a[contains(@href, '.mp4') or contains(@href, '.avi') or contains(@href, '.mkv') or contains(@href, '.mov') or contains(@href, '.m3u8')]/@href").getall()

        # Process the first video link found, if any
        if video_urls:
            video_url = response.urljoin(video_urls[0])
            print(f"Found video: {video_url}")
            self.download_video(video_url)  # Call yt-dlp to handle the download
            self.video_found = True  # Stop further crawling after downloading the first video

        # Continue following links if no video has been found yet
        if not self.video_found:
            for next_page in response.xpath('//a/@href').getall():
                absolute_url = response.urljoin(next_page)
                if absolute_url.startswith("http://") or absolute_url.startswith("https://"):
                    yield response.follow(absolute_url, self.parse)

    def download_video(self, url):
        """Download the video using yt-dlp."""
        ydl_opts = {
            'outtmpl': '%(title)s.%(ext)s',  # Save with video title as filename
            'format': 'best',                # Download the best available quality
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4'      # Convert to mp4 format if needed
            }]
        }
        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            print("Video downloaded successfully.")
        except Exception as e:
            print(f"Failed to download video: {e}")

def run_spider():
    process = CrawlerProcess(settings={
        'USER_AGENT': 'Mozilla/5.0',
        'ROBOTSTXT_OBEY': True,
        'DEPTH_LIMIT': 5,
        'LOG_LEVEL': 'ERROR'
    })
    process.crawl(WebSpider)
    process.start()

if __name__ == "__main__":
    run_spider()
