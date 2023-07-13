from string import ascii_uppercase as letters
from constructs import Construct
from aws_cdk.aws_elasticloadbalancingv2 import NetworkLoadBalancer
from aws_cdk.aws_ec2 import SubnetSelection, Vpc, CfnEIP
from aws_cdk.aws_lambda import Function, Runtime, Code
from aws_cdk import (
    Duration,
    Stack,
)

from main.elastic_ip import ElasticIpForNLB
from main.wait_for_eip_dissociation import WaitForEipDissociation  # noqa


class Main(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.vpc = Vpc.from_lookup(self, "default", vpc_name="Default")
        self.load_balancer: NetworkLoadBalancer = NetworkLoadBalancer(
            self,
            "loadbalancer",
            internet_facing=True,
            vpc=self.vpc,
            vpc_subnets=SubnetSelection(subnets=self.vpc.public_subnets),
        )

        wait_For_eip_lambda: Function = Function(  # noqa
            self, 'custom-resource-handler',
            runtime=Runtime.PYTHON_3_7,
            code=Code.from_asset('main/lambda'),
            handler='main.handler',
            timeout=Duration.seconds(60),
        )

        for i, subnet in enumerate(self.vpc.public_subnets):
            elastic_ip = CfnEIP(self, f"eip-{letters[i]}")

            # attach EIP to NLB
            ElasticIpForNLB(
                self,
                f"eip-attach-{letters[i]}",
                subnet=subnet,
                network_load_balancer=self.load_balancer,
                elastic_ip=elastic_ip,
            )

            ## Uncomment this to add DependsOn to the load balancer resource  # noqa
            # wait_for_dissociation = WaitForEipDissociation(
            #     self,
            #     f"custom-resource-{letters[i]}",
            #     service_token=wait_For_eip_lambda.function_arn,
            #     elastic_ip=elastic_ip,
            #     target_subnet=subnet,
            # )
            # self.load_balancer.node.add_dependency(wait_for_dissociation)
