from aws_cdk import (
    Stack,
    NestedStack,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
    aws_logs as logs,
    aws_iam as iam,
    aws_cloudwatch as cw,
    aws_cloudwatch_actions as cw_actions,
    RemovalPolicy,
    CfnOutput,
    aws_logs_destinations as destinations,
)
from constructs import Construct

# Notification email address
email = "eivistamos@gmail.com"

class CoreStack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        account_id = Stack.of(self).account

        #1 SNS Topic for Notifications
        self.notification_topic = sns.Topic(
            self,
            "DeploymentNotifications",
            display_name="Deployment Notifications",
            topic_name="deployment-notifications",
        )

        self.notification_topic.add_subscription(
            subs.EmailSubscription(email)
        )        

        #3 IAM Roles

        #-DevOps Role
        self.devops_role = iam.Role(
            self,
            "DevOpsRole",
            assumed_by=iam.AccountRootPrincipal(),
            role_name="DevOpsRole",
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess")
            ],
        )

        #-ReadOnly Role
        self.read_only_role = iam.Role(
            self,
            "ReadOnlyRole",
            assumed_by=iam.AccountRootPrincipal(),
            role_name="ReadOnlyRole",
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("ReadOnlyAccess")
            ],
        )        

        #2 CloudWatch Log Group
        self.log_group = logs.LogGroup(
            self,
            "CoreLogGroup",
            log_group_name="/cdk/core-stack",
            retention=logs.RetentionDays.ONE_WEEK,
            removal_policy=RemovalPolicy.DESTROY
        )

        #2.3 Cloudwatch Metric Filter - for logs with ERROR
        self.error_metric = logs.MetricFilter(
            self,
            "ErrorMetricFilter",
            log_group=self.log_group,
            metric_namespace="LandingZone/Core",
            metric_name="ErrorCount",
            filter_pattern=logs.FilterPattern.literal("ERROR"),
            metric_value="1",
        )

        #2.4 Cloudwatch Alarm - for ERROR logs
        self.error_alarm = cw.Alarm(
            self,
            "ErrorAlarm",
            metric=self.error_metric.metric(),
            threshold=1,
            evaluation_periods=1,
            alarm_description="Alarm if an ERROR is detected in logs",
            alarm_name="LandingZoneErrorAlarm"
        )

        #2.5 Send Notification to SNS
        self.error_alarm.add_alarm_action(cw_actions.SnsAction(self.notification_topic))


        self.output_arns()

        #5 Output ARNS
    
    def output_arns(self):
        CfnOutput(self, "SNSTopicARN", value=self.notification_topic.topic_arn)
        CfnOutput(self, "CloudWatchLogGroupName", value=self.log_group.log_group_name)
        CfnOutput(self, "DevOpsRoleARN", value=self.devops_role.role_arn)
        CfnOutput(self, "ReadOnlyRoleARN", value=self.read_only_role.role_arn)    


        
