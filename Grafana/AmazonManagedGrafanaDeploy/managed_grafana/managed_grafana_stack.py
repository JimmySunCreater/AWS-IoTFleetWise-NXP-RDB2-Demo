import json
import random
from constructs import Construct

from aws_cdk import Stack, aws_ec2 as ec2, aws_iam as iam
from aws_cdk.aws_s3_assets import Asset
from aws_cdk.custom_resources import (
    AwsCustomResource,
    AwsCustomResourcePolicy,
    AwsSdkCall,
    PhysicalResourceId,
)



unique_id = str(random.randint(0, 1000000))


class ManagedGrafanaStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # vpc = ec2.Vpc(
        #     self,
        #     f"AMG-VPC",
        # )

        lambda_role = iam.Role(
            self,
            f"Lambda-Role-{unique_id}",
            role_name= f"lambda_role-{unique_id}",
            inline_policies={
                "grafana-lambda-policy": iam.PolicyDocument(
                    statements=[
                        iam.PolicyStatement(
                            actions=["iam:PassRole","sso:*"],
                            resources=["*"]
                        )
                    ]
                )
            },
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com")
        )

        # ec2_role = iam.Role(
        #     self,
        #     "EC2-Role",
        #     role_name="ec2_role",
        #     managed_policies=[
        #         iam.ManagedPolicy.from_aws_managed_policy_name(
        #             "AWSGrafanaConsoleReadOnlyAccess"
        #         ),
        #     ],
        #     inline_policies={
        #         "keycloak-ec2-policy": iam.PolicyDocument(
        #             statements=[
        #                 iam.PolicyStatement(
        #                     actions=[                
        #                         "grafana:UpdateWorkspaceAuthentication",
        #                         "grafana:UpdateWorkspace",
        #                         "ec2:Describe*",

        #                     ],
        #                     resources=["*"]
        #                 )                                            
        #             ]
        #         )
        #     },
        #     assumed_by=iam.ServicePrincipal("ec2.amazonaws.com")
        # )

        AwsCustomResource(
            self,
            f"amgworkspace-{unique_id}",
            on_create=self.create(),
            policy=AwsCustomResourcePolicy.from_sdk_calls(
                resources=AwsCustomResourcePolicy.ANY_RESOURCE
            ),
            role=lambda_role
        )

        # security_group = ec2.SecurityGroup(self, "Keycloak-Security-Group", vpc=vpc)
        # security_group.add_ingress_rule(
        #     peer=ec2.Peer.any_ipv4(),
        #     connection=ec2.Port.tcp(80)
        # )

        # instance = ec2.Instance(self, "Keycloak-Instance",
        #     vpc=vpc,
        #     vpc_subnets=ec2.SubnetSelection(
        #         subnet_type=ec2.SubnetType.PUBLIC
        #     ),            
        #     instance_type=ec2.InstanceType("t3.small"),
        #     machine_image=ec2.AmazonLinuxImage(
        #         generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2
        #     ),
        #     role=ec2_role,
        #     security_group=security_group
        # )
        # with open ("./bootstrap.sh", "r") as myfile:
        #     data=myfile.read()
        # instance.add_user_data(data)

    def create(self):
        grafana_role = iam.Role(
            self,
            f"Grafana-Role-{unique_id}",
            role_name=f"Grafana-Role-{unique_id}",
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "AWSXrayReadOnlyAccess",
                ),
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "AWSIoTSiteWiseReadOnlyAccess",
                ),
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "AmazonTimestreamReadOnlyAccess"
                )
            ],
            inline_policies={
                "grafana-policy": iam.PolicyDocument(
                    statements=[
                        iam.PolicyStatement(
                            actions=[
                                "sns:Publish",
                                "aps:ListWorkspaces",
                                "aps:DescribeWorkspace",
                                "aps:QueryMetrics",
                                "aps:GetLabels",
                                "aps:GetSeries",
                                "aps:GetMetricMetadata",
                                "cloudwatch:DescribeAlarmsForMetric",
                                "cloudwatch:DescribeAlarmHistory",
                                "cloudwatch:DescribeAlarms",
                                "cloudwatch:ListMetrics",
                                "cloudwatch:GetMetricStatistics",
                                "cloudwatch:GetMetricData",
                                "logs:DescribeLogGroups",
                                "logs:GetLogGroupFields",
                                "logs:StartQuery",
                                "logs:StopQuery",
                                "logs:GetQueryResults",
                                "logs:GetLogEvents",
                                "ec2:DescribeTags",
                                "ec2:DescribeInstances",
                                "ec2:DescribeRegions",
                                "tag:GetResources",
                                "es:ESHttpGet",
                                "es:DescribeElasticsearchDomains",
                                "es:ListDomainNames"

                            ],
                            resources=["*"],
                        )
                    ]
                )
            },
            assumed_by=iam.ServicePrincipal("grafana.amazonaws.com"),
        )

        return AwsSdkCall(
                service="Grafana",
                action="createWorkspace",
                parameters={
                    "accountAccessType": "CURRENT_ACCOUNT",
                    "authenticationProviders": ["AWS_SSO"],
                    "permissionType": "SERVICE_MANAGED",
                    "workspaceDataSources": [
                        "PROMETHEUS",
                        "XRAY",
                        "TIMESTREAM",
                        "SITEWISE",
                        "AMAZON_OPENSEARCH_SERVICE",
                        "CLOUDWATCH"
                    ],
                    "workspaceName": "fleetwise-demo-workspace",
                    "workspaceNotificationDestinations": ["SNS"],
                    "workspaceRoleArn": grafana_role.role_arn,
                },
                physical_resource_id=PhysicalResourceId.of("AmgCustomResource"),
        )