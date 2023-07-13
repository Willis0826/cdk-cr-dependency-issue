from __future__ import annotations

from aws_cdk import CustomResource
from aws_cdk.aws_ec2 import CfnEIP, ISubnet
from constructs import Construct


class WaitForEipDissociation(Construct):
    """Custom resource that waits for an EIP to dissociate, freeing
    it up for deletion.
    """

    def __init__(
        self,
        scope: Construct,
        id: str,
        *,
        service_token: str,
        elastic_ip: CfnEIP,
        target_subnet: ISubnet,
        **kwargs,
    ):
        super().__init__(
            scope,
            id,
            **kwargs,
        )

        self.resource = CustomResource(
            self,
            id,
            service_token=service_token,
            properties={
                "ElasticIp": elastic_ip.ref,
                "TargetSubnet": target_subnet.subnet_id,
            },
        )
