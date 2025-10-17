import dagger
from dagger import dag, function, object_type


@object_type
class Book:
    @function
    def env(self, source: dagger.Directory) -> dagger.Container:
        """Returns a container with the FastAPI environment set up"""
        return (
            dag.container()
            .from_("python:3.11")
            .with_exec(["sh", "-c", "apt-get update && apt-get install -y libpq-dev"])
            .with_directory("/app", source)
            .with_workdir("/app")
            .with_exec(["pip", "install", "-r", "requirements.txt"])
            .with_exposed_port(8000)
            .with_entrypoint(["fastapi", "run", "main.py", "--port", "8000"])
        )

    @function
    def container_echo(self, string_arg: str) -> dagger.Container:
        """Returns a container that echoes whatever string argument is provided"""
        return dag.container().from_("alpine:latest").with_exec(["echo", string_arg])

    @function
    async def grep_dir(self, directory_arg: dagger.Directory, pattern: str) -> str:
        """Returns lines that match a pattern in the files of the provided Directory"""
        return await (
            dag.container()
            .from_("alpine:latest")
            .with_mounted_directory("/mnt", directory_arg)
            .with_workdir("/mnt")
            .with_exec(["grep", "-R", pattern, "."])
            .stdout()
        )
