"""
A stack to create/reference
 * an AWS CodeCommit repository
 * AWS Codepipeline to build and deploy an application stack
 * approval template with association to the repo created
"""
# !/usr/bin/env python3

from aws_cdk import core as cdk
from aws_cdk.aws_codebuild import BuildEnvironment
from aws_cdk.aws_codecommit import Repository
from aws_cdk.aws_codepipeline import Artifact
#from aws_cdk.aws_codepipeline_actions import CodeCommitSourceAction
from aws_cdk.aws_codepipeline_actions import GitHubSourceAction
from aws_cdk import aws_codepipeline_actions as codepipeline_actions
from aws_cdk.core import Stack, Construct, Environment
from aws_cdk.pipelines import SimpleSynthAction, CdkPipeline

#from .application_stage import ApplicationStage
from .utilities import get_build_env

class PipelineStack(Stack):
    """
    Extends the stack to create a pipeline for CDK applications.

    Methods:
    -----------
        create_pipeline
            creates a CDK pipeline for the app stack
        create_src_action
            returns a source action for cloning the branch from the repo
        create_synth_action
            creates a synth action which builds and synthesizes the cdk app
    """

    def __init__(self, scope: Construct,
                 construct_id: str, context: str,
                 stage: str,env_data: Environment, **kwargs) -> None:
        """
        Parameters
        ----------
        context: str
            a string value referencing the parent element in cdk.json for this stack
        stage: str
            string value defining the stage where infrastructure is deployed
        repo: Repository
            References an existing repo from CIstack
        env_data: Environment
            environment specs for target deployment
        """

        super().__init__(scope, construct_id, **kwargs)

        cloud_assembly_artifact = Artifact("CloudArtifact")
        pipeline_context = dict(self.node.try_get_context(context))
        src_artifact = Artifact("SourceArtifact")
        context = dict(self.node.try_get_context(context))
#        repo = Repository.from_repository_name(self, context["repo_name"],
#                                               repository_name=context["repo_name"])

        build_env = get_build_env()

#        src_action = self.create_src_action(
#            pipeline_context, src_artifact, repo)
        src_action = codepipeline_actions.GitHubSourceAction(
            action_name="Source",
            branch="main",
            owner="jasonmlehman",
            repo="github-awscodepipeline",
            oauth_token=cdk.SecretValue.secrets_manager('github2'),
#            oauth_token = cdk.SecretValue.secrets_manager('github', json_field = 'github' ),
            output=src_artifact,
        )
        synth_action = self.create_synth_action(pipeline_context, src_artifact,
                                                cloud_assembly_artifact, build_env,
                                                stage)

        pipeline = self.create_pipeline(cloud_assembly_artifact, src_action,
                                        synth_action, pipeline_context, stage)
        if stage.lower() == "prod":
            approvalneeded = True
        else:
            approvalneeded = False
#        pipeline.add_application_stage(ApplicationStage(self, f"DeployTo{stage}",
#                                                        stage, env=env_data),
#                                       manual_approvals=approvalneeded)

    def create_pipeline(self, cloud_artifact: Artifact,
                        src_action: GitHubSourceAction, synth_action: SimpleSynthAction,
                        context: dict, stage:str ) -> CdkPipeline:
        """ Returns a codepipeline instance with user inputs from the context file"""
        return CdkPipeline(
            self,
            context["pipeline_name"]+f"{stage}",
            cloud_assembly_artifact=cloud_artifact,
            cdk_cli_version=context["cdk_cli_version"],
            pipeline_name=context["pipeline_name"]+f"-{stage}",
            self_mutating=(context["self_mutating"].lower() == "true"),
            source_action=src_action,
            synth_action=synth_action
        )

    @staticmethod
    def create_synth_action(context: dict, source_artifact: Artifact,
                            cloud_assembly_artifact: Artifact,
                            build_env: BuildEnvironment, stage:str) -> SimpleSynthAction:
        """
        Returns a Synth action reference from user inputs
        Build & install commands are referenced from the user inputs in cdk.json
        Note : The CodeBuild environment provided by AWS doesn't include cdk cli
        """

        return SimpleSynthAction(
            synth_command=context["synth_command"],
            build_commands=context["build_commands"],
            install_commands=context["install_commands"],
            source_artifact=source_artifact,
            cloud_assembly_artifact=cloud_assembly_artifact,
            action_name="BuildAndInstall",
            project_name=f"CodeBuildSynth-{stage}",
            environment=build_env
        )
