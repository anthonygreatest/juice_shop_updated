import os
from pathlib import Path
from typing import Self

from pydantic import HttpUrl
from pydantic_extra_types.path import ResolvedDirectoryPath
from pydantic_settings import BaseSettings, SettingsConfigDict


class SettingsUI(BaseSettings):

    #
    # model_config = SettingsConfigDict(
    #     env_file=str(Path(__file__).parent / ".env_ui"),
    #     env_file_encoding='utf-8'
    # )

    app_url: HttpUrl
    headless: bool
    slow_mo: int = 0
    videos_dir: ResolvedDirectoryPath = ResolvedDirectoryPath('./videos')
    # tracing_dir: DirectoryPath
    expect_timeout: float

    @classmethod
    def initialize(cls) -> Self:

        videos_path = Path(os.getenv("VIDEOS_PATH", "videos"))
        videos_path.mkdir(exist_ok=True, parents=True)

        return cls(videos_dir=videos_path)
