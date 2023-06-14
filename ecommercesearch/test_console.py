import subprocess
import pathlib
import tempfile
import dataclasses
import json

TEST_CONSOLE_FILE_NAME = 'Bizzkit.EcommerceSearch.TestConsole.exe'

@dataclasses.dataclass
class TestConsoleConfiguration:
    source_path: pathlib.Path | None = None
    binaries_path: pathlib.Path | None = None

    def __post_init__(self):
        if isinstance(self.source_path, str):
            self.source_path = pathlib.Path(self.source_path)

        if isinstance(self.binaries_path, str):
            self.binaries_path = pathlib.Path(self.binaries_path)

    @staticmethod
    def load(path: str | pathlib.Path):
        with open(path, 'r') as f:
            content = json.load(f)

        return TestConsoleConfiguration(**content)
    
    def store(self, path: str | pathlib.Path):
        with open(path, 'w') as f:
            json.dump(self, f)

class TestConsole:
    process: subprocess.Popen | None = None

    def __init__(self, config: TestConsoleConfiguration, auto_build: bool = True, auto_start: bool = True):
        self.config = config

        if auto_build:
            self.build()

        if auto_start:
            self.start()

    def build(self):
        if not self.config.source_path:
            raise ValueError('Source file directory has not been specified.')

        if not self.config.binaries_path:
            self.config.binaries_path = pathlib.Path(tempfile.gettempdir()) / 'TestConsole'

        command = ["dotnet", "build", self.config.source_path, "-o", self.config.binaries_path]

        subprocess.run(command, check=True)

    def start(self):
        if not self.config.binaries_path:
            raise ValueError('Binaries have not been built yet.')

        if self.process:
            raise ValueError('Process is already running.')
        
        command = [str(self.config.binaries_path / TEST_CONSOLE_FILE_NAME), ]

        self.process = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

    
    def write_line(self, line: str):
        self.process.stdin.writelines([ line ])

    def read_line(self):
        output: str = self.process.stdout.readline()
        return output

