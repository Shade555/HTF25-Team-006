import os
import boto3
from botocore.exceptions import BotoCoreError, ClientError


class PollyAdapter:
    def __init__(self, region_name=None):
        region = region_name or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"
        self.client = boto3.client("polly", region_name=region)

    def list_voices(self, language_code=None):
        params = {}
        if language_code:
            params["LanguageCode"] = language_code
        resp = self.client.describe_voices(**params)
        return resp.get("Voices", [])

    def synthesize(self, text, voice=None, voice_id="Joanna", engine="neural", output_format="mp3", text_type="text"):
        """
        Synthesize speech using Amazon Polly.

        Accepts either `voice` (preferred when using a provider-agnostic interface)
        or `voice_id` for backward compatibility. Returns raw audio bytes or None.
        """
        # prefer explicit `voice` param if provided
        vid = voice if voice else voice_id
        try:
            response = self.client.synthesize_speech(
                Text=text,
                VoiceId=vid,
                Engine=engine,
                OutputFormat=output_format,
                TextType=text_type,
            )
            stream = response.get("AudioStream")
            if stream:
                data = stream.read()
                stream.close()
                return data
            return None
        except (BotoCoreError, ClientError) as e:
            # Let caller handle/log exception
            raise
