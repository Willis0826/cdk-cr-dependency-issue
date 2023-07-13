from __future__ import annotations

from aws_cdk import aws_ec2 as ec2
from aws_cdk.aws_ec2 import CfnEIP
from aws_cdk.aws_elasticloadbalancingv2 import (
    CfnLoadBalancer,
    NetworkLoadBalancer,
)
from constructs import Construct


class ElasticIpForNLB(Construct):
    """Attaching elastic ip to a network load balancer"""

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        subnet: ec2.ISubnet,
        network_load_balancer: NetworkLoadBalancer,
        elastic_ip: CfnEIP,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        cfn_load_balancer = network_load_balancer.node.default_child
        cfn_load_balancer.subnets = None

        subnet_mapping = CfnLoadBalancer.SubnetMappingProperty(
            subnet_id=subnet.subnet_id,
            allocation_id=elastic_ip.attr_allocation_id,
        )

        if cfn_load_balancer.subnet_mappings:
            old_mappings = cfn_load_balancer.subnet_mappings
            old_mappings.append(subnet_mapping)
            cfn_load_balancer.subnet_mappings = old_mappings
        else:
            cfn_load_balancer.subnet_mappings = [subnet_mapping]
