from pydantic import Field

from configuration.base import Config


class InfrastructureIdentityConfig(Config):
    id: str
    name: str
    environment: str = "production"


class InfrastructureMetadataConfig(Config):
    version: str = "1.0"
    tags: list[str] = Field(default_factory=list)


class NodeEndpointConfig(Config):
    type: str
    address: str


class NodeConfig(Config):
    id: str
    name: str
    description: str = ""
    endpoint: NodeEndpointConfig


class ServiceConfig(Config):
    id: str
    name: str
    type: str
    node: str
    port: int | None = None


class InfrastructureConfig(Config):
    infrastructure: InfrastructureIdentityConfig
    metadata: InfrastructureMetadataConfig = Field(
        default_factory=InfrastructureMetadataConfig
    )
    nodes: list[NodeConfig] = Field(default_factory=list)
    services: list[ServiceConfig] = Field(default_factory=list)