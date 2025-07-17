from storages.backends.s3boto3 import S3Boto3Storage
import os

class SupabasePublicMediaStorage(S3Boto3Storage):
    default_acl = 'public-read'
    custom_domain = f"{os.getenv('SUPABASE_MEDIA_URL')}/{os.getenv('SUPABASE_S3_BUCKET_NAME')}"
    def url(self, name):
        return f"{self.custom_domain}/{name}"
