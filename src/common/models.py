from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class EC2Instance:
    env: str
    name: str
    instance_id: str
    state: str
    launch_time: str
    owner: str
    suggested_action: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)
