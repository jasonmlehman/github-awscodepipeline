"""
Common utilities which can be used across some constructs
"""
from aws_cdk.aws_codebuild import BuildEnvironment, LinuxBuildImage, ComputeType
from aws_cdk.aws_logs import RetentionDays
from aws_cdk.core import RemovalPolicy


def get_log_retention_days(key: str) -> RetentionDays:
    """returns the log retention enum based on the input key"""
    log_retention_days = {
        "one_day": RetentionDays.ONE_DAY,
        "three_days": RetentionDays.THREE_DAYS,
        "five_days": RetentionDays.FIVE_DAYS,
        "one_week": RetentionDays.ONE_WEEK,
        "two_weeks": RetentionDays.TWO_WEEKS,
        "one_month": RetentionDays.ONE_MONTH,
        "two_months": RetentionDays.TWO_MONTHS,
        "three_months": RetentionDays.THREE_MONTHS,
        "four_months": RetentionDays.FOUR_MONTHS,
        "five_months": RetentionDays.FIVE_MONTHS,
        "six_months": RetentionDays.SIX_MONTHS,
        "one_year": RetentionDays.ONE_YEAR,
        "thirteen_months": RetentionDays.THIRTEEN_MONTHS,
        "eighteen_months": RetentionDays.EIGHTEEN_MONTHS,
        "two_years": RetentionDays.TWO_YEARS,
        "five_years": RetentionDays.FIVE_YEARS,
        "ten_years": RetentionDays.TEN_YEARS,
        "infinite": RetentionDays.INFINITE
    }
    return log_retention_days[key]


def get_removal_policy(removal_policy: str) -> RemovalPolicy:
    """ returns the removal policy based on user inputs"""
    return RemovalPolicy.DESTROY if removal_policy.lower() == "destroy" \
        else RemovalPolicy.RETAIN


def get_build_env() -> BuildEnvironment:
    """ returns a Build environment configuration for CodeBuild containers"""
    return BuildEnvironment(
        build_image=LinuxBuildImage.STANDARD_5_0,
        compute_type=ComputeType.LARGE,
        privileged=False,
    )
